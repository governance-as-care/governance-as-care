---
id: agent-intake-summarizer-01
name: Scribe                                   # human handle only — NOT the identifier
owner: Dana Ruiz (Clinical Ops Lead)
charter: "Draft a clinician-facing summary from a patient intake form. Nothing else."
data_classification: [phi, pii]                # classify, period — never blank
data_review:
  phi: "BAA with model provider signed 2026-06-02; minimum-necessary scope documented; logs excluded from training; all components onshore"
  pii: "DPA in place (same instrument); retention 30 days on draft queue"
model: claude-sonnet-4.5
model_verified: 2026-08-14
version: 1.3
last_changed: 2026-08-14
last_approved_by: Dana Ruiz
status: active
health_last_checked: 2026-08-15
can_touch:
  - intake-forms (read)
  - summary-draft-queue (write)
cannot_touch:
  - EHR write access
  - outbound email / messaging
  - billing or claims systems
kill_path: "Revoke its API key in the vault (Ops has access). Dies in <1 min. Owner or one other may pull it."
---

# Intake Summarizer ("Scribe")

**What it does:** Reads a submitted intake form and drafts a plain-language
summary for the reviewing clinician. A human reviews and edits every summary
before it enters the record.

**What it must never do:** Write to the EHR, contact patients, or make a
clinical call. It drafts; a person decides.

**Why the card looks like this:** The charter is one sentence, so drift is
visible the day it starts. The can/can't columns sit side by side, so the
entitlement and the limit are read together. The kill path names a mechanism
and a person, so stopping it at 3 a.m. requires no meeting. The data classes
are declared and covered, so nobody discovers the PHI after the fact.
