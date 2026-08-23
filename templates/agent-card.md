---
id:                       # machine identity — immutable; authz and the kill path act on THIS
name:                     # optional human nickname — never does the machine's job
owner:                    # a PERSON, accountable (not a team name)
charter: ""               # one sentence: what it is FOR. Outside this = drift.
data_classification: []   # REQUIRED, never blank. Vocabulary: public | confidential | pii | phi | pci
# data_review:            # required per regulated class (pii/phi/pci):
#   phi: "what coverage legitimizes it (e.g., BAA, scope, retention, locations)"
model:                    # e.g. claude-sonnet-4.5 — exact model identifier
model_verified:           # YYYY-MM-DD you last confirmed the model is what you think it is
version: 1.0
last_changed:             # YYYY-MM-DD
last_approved_by:         # a person
status: active            # active | degraded | retired
health_last_checked:      # YYYY-MM-DD
can_touch:
  -                       # entitlement (system + read/write)
cannot_touch:
  -                       # the hard limits, written down where everyone can see them
kill_path: ""             # exactly HOW to stop it and WHO may — mechanism + person, no meeting required
---

# <Agent name>

**What it does:** <two or three sentences a new teammate would understand>

**What it must never do:** <the limits, in plain words>
