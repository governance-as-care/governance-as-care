#!/usr/bin/env python3
"""Tests for check.py — the registry heartbeat. Standard library only."""
import os, shutil, subprocess, sys, tempfile, textwrap, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CHECK = os.path.join(ROOT, "check.py")

GOOD = """\
---
id: agent-good-01
name: Scribe
owner: Dana Ruiz (Clinical Ops Lead)
charter: "Draft a clinician-facing summary from a patient intake form. Nothing else."
data_classification: [public]
model: claude-sonnet-4.5
model_verified: {model_verified}
version: 1.0
last_changed: 2026-08-01
last_approved_by: Dana Ruiz
status: active
health_last_checked: {health}
can_touch:
  - intake-forms (read)
cannot_touch:
  - outbound email
kill_path: "Revoke its API key in the vault. Owner or one other may pull it."
---

# Good Agent
Body text.
"""


def write_card(dirpath, fname, text):
    with open(os.path.join(dirpath, "agents", fname), "w") as f:
        f.write(text)


def run_check(dirpath, *args):
    return subprocess.run([sys.executable, CHECK, *args], cwd=dirpath,
                          capture_output=True, text=True)


def today():
    import datetime
    return datetime.date.today().isoformat()


class CheckTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.dir, "agents"))

    def tearDown(self):
        shutil.rmtree(self.dir)

    def good_card(self):
        return GOOD.format(model_verified=today(), health=today())

    # -- parsing & happy path ------------------------------------------------
    def test_clean_registry_exits_zero(self):
        write_card(self.dir, "good.md", self.good_card())
        r = run_check(self.dir)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("0 blockers", r.stdout)

    def test_registry_md_generated(self):
        write_card(self.dir, "good.md", self.good_card())
        run_check(self.dir)
        reg = open(os.path.join(self.dir, "REGISTRY.md")).read()
        self.assertIn("agent-good-01", reg)
        self.assertIn("Scribe", reg)
        self.assertIn("generated", reg.lower())

    # -- the six checks ------------------------------------------------------
    def test_orphan_is_blocker(self):
        card = self.good_card().replace("owner: Dana Ruiz (Clinical Ops Lead)\n", "")
        write_card(self.dir, "orphan.md", card)
        r = run_check(self.dir)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("owner", r.stdout.lower())

    def test_missing_kill_path_is_blocker(self):
        card = self.good_card().replace(
            'kill_path: "Revoke its API key in the vault. Owner or one other may pull it."\n', "")
        write_card(self.dir, "nokill.md", card)
        r = run_check(self.dir)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("kill_path", r.stdout)

    def test_health_overdue_is_warning(self):
        card = GOOD.format(model_verified=today(), health="2026-01-01")
        write_card(self.dir, "stale.md", card)
        r = run_check(self.dir)
        self.assertEqual(r.returncode, 0)          # warning, not blocker
        self.assertIn("health", r.stdout.lower())

    def test_model_drift_is_warning(self):
        card = GOOD.format(model_verified="2026-01-01", health=today())
        write_card(self.dir, "drift.md", card)
        r = run_check(self.dir)
        self.assertEqual(r.returncode, 0)
        self.assertIn("unverified", r.stdout.lower())

    def test_missing_charter_is_blocker(self):
        card = self.good_card().replace(
            'charter: "Draft a clinician-facing summary from a patient intake form. Nothing else."\n', "")
        write_card(self.dir, "nocharter.md", card)
        r = run_check(self.dir)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("charter", r.stdout.lower())

    def test_unclassified_data_is_blocker(self):
        card = self.good_card().replace("data_classification: [public]\n", "")
        write_card(self.dir, "unclass.md", card)
        r = run_check(self.dir)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("classif", r.stdout.lower())

    def test_regulated_class_without_coverage_is_blocker(self):
        card = self.good_card().replace("data_classification: [public]",
                                        "data_classification: [phi, pii]")
        write_card(self.dir, "phi.md", card)
        r = run_check(self.dir)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("coverage", r.stdout.lower())

    def test_regulated_class_with_coverage_passes(self):
        card = self.good_card().replace(
            "data_classification: [public]",
            "data_classification: [phi]\ndata_review:\n  phi: \"BAA with provider, signed 2026-07-01; minimum-necessary scope documented\"")
        write_card(self.dir, "phi_ok.md", card)
        r = run_check(self.dir)
        self.assertEqual(r.returncode, 0, r.stdout)

    # -- robustness ----------------------------------------------------------
    def test_malformed_card_reported_not_crash(self):
        write_card(self.dir, "broken.md", "no frontmatter at all\n")
        write_card(self.dir, "good.md", self.good_card())
        r = run_check(self.dir)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("malformed", r.stdout.lower())
        self.assertIn("agent-good-01", open(os.path.join(self.dir, "REGISTRY.md")).read())

    def test_thresholds_configurable(self):
        card = GOOD.format(model_verified="2026-01-01", health=today())
        write_card(self.dir, "drift.md", card)
        r = run_check(self.dir, "--model-days", "100000")
        self.assertNotIn("unverified", r.stdout.lower())

    def test_retired_agents_skip_freshness_checks(self):
        card = self.good_card().replace("status: active", "status: retired")
        card = card.replace(f"health_last_checked: {today()}", "health_last_checked: 2026-01-01")
        write_card(self.dir, "retired.md", card)
        r = run_check(self.dir)
        self.assertEqual(r.returncode, 0, r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
