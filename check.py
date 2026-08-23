#!/usr/bin/env python3
"""Agent registry heartbeat — reads agents/*.md, writes REGISTRY.md, prints the board.

Standard library only. No install step, no dependencies, no service.
Usage:
    python3 check.py [--health-days 14] [--model-days 30] [--dir PATH]

Exit code is non-zero when any BLOCKER is present, so this can gate CI later.
The six checks:
    1. orphan            — no owner            (blocker)
    2. no kill path      — kill_path missing    (blocker)
    3. health overdue    — health_last_checked older than threshold (warning)
    4. model drift       — model_verified older than threshold      (warning)
    5. no charter        — charter missing      (blocker)
    6. data unclassified — data_classification missing/empty (blocker),
       or a regulated class (pii/phi/pci) with no data_review coverage (blocker)

Honest caveat: the heartbeat is only as true as the cards. Keep the cards born
with the agents, and keep them current — the record must never flatter you.
"""
import argparse
import datetime
import glob
import os
import sys

REQUIRED = ["id", "owner", "charter", "can_touch", "cannot_touch",
            "data_classification", "kill_path", "status", "health_last_checked",
            "version", "last_changed", "last_approved_by", "model", "model_verified"]
REGULATED = {"pii", "phi", "pci"}
STATUSES = {"active", "degraded", "retired"}


# ---------------------------------------------------------------- frontmatter
def parse_frontmatter(text):
    """Tiny hand-rolled parser for the simple YAML subset the card uses:
    key: scalar · key: [a, b] · key: "quoted" · block lists ·
    one-level nested maps (e.g. data_review). Returns dict or None."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None

    data, current_key, current_map = {}, None, None
    for raw in lines[1:end]:
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()

        if indent == 0:
            current_map = None
            if line.startswith("- "):
                continue  # stray top-level list item; ignore
            if ":" not in line:
                continue
            key, _, val = line.partition(":")
            key, val = key.strip(), _strip_comment(val.strip())
            if val == "":
                data[key] = []          # block list or nested map follows
                current_key = key
            elif val.startswith("[") and val.endswith("]"):
                items = [v.strip().strip('"').strip("'")
                         for v in val[1:-1].split(",") if v.strip()]
                data[key] = items
                current_key = None
            else:
                data[key] = val.strip('"').strip("'")
                current_key = None
        else:
            if line.startswith("- ") and current_key:
                if not isinstance(data.get(current_key), list):
                    data[current_key] = []
                data[current_key].append(_strip_comment(line[2:]).strip('"').strip("'"))
            elif ":" in line and current_key:
                # one-level nested map (e.g. data_review: { phi: "..." })
                if not isinstance(data.get(current_key), dict):
                    if data.get(current_key) == [] or data.get(current_key) is None:
                        data[current_key] = {}
                        current_map = current_key
                if current_map:
                    k, _, v = line.partition(":")
                    data[current_map][k.strip()] = _strip_comment(v.strip()).strip('"').strip("'")
    return data


def _strip_comment(val):
    # strip trailing "  # comment" (but leave # inside quotes alone — the card
    # subset never needs quoted #, keep it simple)
    if '"' in val or "'" in val:
        return val
    return val.split("  #")[0].split("\t#")[0].strip()


def parse_date(val):
    try:
        return datetime.date.fromisoformat(str(val))
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------------------- checks
def check_card(card, fname, today, health_days, model_days):
    """Returns (blockers, warnings) — lists of message strings."""
    blockers, warnings = [], []
    ident = card.get("id") or fname

    def has(key):
        v = card.get(key)
        return v not in (None, "", [], {})

    # 1. orphan
    if not has("owner"):
        blockers.append(f"{ident}: NO OWNER (orphaned)")
    # 2. kill path
    if not has("kill_path"):
        blockers.append(f"{ident}: no kill_path defined")
    # 5. charter
    if not has("charter"):
        blockers.append(f"{ident}: no charter (what is it for?)")
    # 6. data classification — classify, period
    if not has("data_classification"):
        blockers.append(f"{ident}: data_classification missing (must classify; public is the floor)")
    else:
        classes = card["data_classification"]
        if isinstance(classes, str):
            classes = [classes]
        review = card.get("data_review") or {}
        for cls in classes:
            if cls in REGULATED and not (isinstance(review, dict) and review.get(cls)):
                blockers.append(f"{ident}: regulated class '{cls}' has no coverage entry in data_review")

    retired = str(card.get("status", "")).lower() == "retired"
    if not retired:
        # 3. health overdue
        d = parse_date(card.get("health_last_checked"))
        if d is None:
            warnings.append(f"{ident}: health_last_checked missing or not a date")
        elif (today - d).days > health_days:
            warnings.append(f"{ident}: health check overdue {(today - d).days}d (threshold {health_days}d)")
        # 4. model drift
        d = parse_date(card.get("model_verified"))
        if d is None:
            warnings.append(f"{ident}: model_verified missing or not a date")
        elif (today - d).days > model_days:
            warnings.append(f"{ident}: model unverified {(today - d).days}d (silent-drift risk)")

    if has("status") and str(card.get("status")).lower() not in STATUSES:
        warnings.append(f"{ident}: unknown status '{card.get('status')}' (expected active|degraded|retired)")
    return blockers, warnings


# ------------------------------------------------------------------- index
def registry_row(card):
    classes = card.get("data_classification") or []
    if isinstance(classes, str):
        classes = [classes]
    name = card.get("name", "")
    label = f"{card.get('id','?')}" + (f" ({name})" if name else "")
    return "| {} | {} | {} | {} | {} | {} | {} |".format(
        label, card.get("owner", "—"), ", ".join(classes) or "—",
        card.get("status", "—"), card.get("model_verified", "—"),
        card.get("health_last_checked", "—"),
        "yes" if card.get("kill_path") else "NO")


def write_registry(path, cards):
    lines = [
        "# Agent Registry",
        "",
        "*Generated by `check.py` — do not hand-edit. The `agents/` folder is the inventory;*",
        "*this file is its index.*",
        "",
        "| Agent | Owner | Data classes | Status | Model verified | Health checked | Kill path |",
        "|---|---|---|---|---|---|---|",
    ]
    lines += [registry_row(c) for c in sorted(cards, key=lambda c: str(c.get("id", "")))]
    lines.append("")
    with open(path, "w") as f:
        f.write("\n".join(lines))


# -------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Agent registry heartbeat")
    ap.add_argument("--dir", default=".", help="registry root (contains agents/)")
    ap.add_argument("--health-days", type=int, default=14)
    ap.add_argument("--model-days", type=int, default=30)
    args = ap.parse_args()

    agents_dir = os.path.join(args.dir, "agents")
    files = sorted(glob.glob(os.path.join(agents_dir, "*.md")))
    today = datetime.date.today()

    cards, blockers, warnings = [], [], []
    for path in files:
        fname = os.path.basename(path)
        try:
            text = open(path, encoding="utf-8").read()
        except OSError as e:
            blockers.append(f"{fname}: unreadable ({e})")
            continue
        card = parse_frontmatter(text)
        if card is None:
            blockers.append(f"{fname}: malformed card (no frontmatter fences)")
            continue
        cards.append(card)
        b, w = check_card(card, fname, today, args.health_days, args.model_days)
        blockers += b
        warnings += w

    write_registry(os.path.join(args.dir, "REGISTRY.md"), cards)

    print(f"Agent Registry Heartbeat — {len(cards)} agent{'s' if len(cards) != 1 else ''}")
    for msg in blockers:
        print(f"  ✗ {msg}")
    for msg in warnings:
        print(f"  ⚠ {msg}")
    print(f"Board: {len(blockers)} blocker{'s' if len(blockers) != 1 else ''}, "
          f"{len(warnings)} warning{'s' if len(warnings) != 1 else ''}.")
    sys.exit(1 if blockers else 0)


if __name__ == "__main__":
    main()
