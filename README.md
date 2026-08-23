# Governance as Care

*An agent card and registry for anyone who runs AI agents — solo builder,
clinic, agency, enterprise. Free, forkable, no dependencies, no service, no
account. Governance is care made auditable.*

---

## The four questions

For every agent you run, this kit answers:

1. **What is it, and who answers for it?**
2. **What can it touch — and what can it never touch?**
3. **How do we stop it, and who is allowed to?**
4. **Is it healthy, and when did it last change?**

If you can answer those for every agent, you can adopt the next one calmly.
If you can't, no framework binder will make you feel otherwise.

## What's in the box

```
├── check.py                     # the heartbeat — index + six fleet checks, stdlib only
├── agents/                      # one card per agent — the folder IS the inventory
│   └── example-intake-summarizer-01.md
├── REGISTRY.md                  # generated index (never hand-edited)
├── templates/
│   ├── agent-card.md            # blank card (git form)
│   └── agent-card-one-pager.md  # printable form — no tools required
├── tests/test_check.py          # the heartbeat proves its own liveness
└── docs/field-guide.md          # every field: what it means, why it gives footing
```

## Quickstart (under 30 minutes, honestly)

1. **Fork or copy this repo.** No install, no account, no dependency —
   `check.py` is standard-library Python.
2. **Copy `templates/agent-card.md` into `agents/`,** one file per agent, and
   fill it in. Ten minutes per card. (No git in your life? Print
   `templates/agent-card-one-pager.md` and fill it by hand — same fields; the
   answers drop into the file form whenever you're ready.)
3. **Run the heartbeat:**

   ```
   python3 check.py
   ```

   You get `REGISTRY.md` (the fleet at a glance) and the board:

   ```
   Agent Registry Heartbeat — 3 agents
     ✗ refill-reminder-03: NO OWNER (orphaned)
     ✗ refill-reminder-03: no kill_path defined
     ⚠ vendor-triage-02: model unverified 34d (silent-drift risk)
   Board: 2 blockers, 1 warning.
   ```

   Non-zero exit on blockers, so it can gate CI whenever you're ready.

## The six checks

| # | Check | Severity |
|---|---|---|
| 1 | Orphan — card with no accountable person | blocker |
| 2 | No kill path | blocker |
| 3 | Health check overdue (default 14d) | warning |
| 4 | Model unverified (default 30d — silent-drift risk) | warning |
| 5 | No charter | blocker |
| 6 | Data unclassified, or regulated class with no coverage | blocker |

Thresholds: `python3 check.py --health-days 14 --model-days 30`

## The card in one paragraph

A card is a Markdown file with YAML frontmatter: a machine `id` (what
authorization and the kill path act on), an optional human `name` (what the
team calls it — the name never does the machine's job), an accountable
**person**, a **one-sentence charter** (drift is visible against one sentence),
**can-touch and can't-touch side by side**, a **declared data classification**
(never blank — `public` is the floor, and regulated classes carry their
coverage), a **kill path written for 3 a.m.**, and a **version stamp** with
`git log` as the change history for free. The full walk-through of every
field — and why each one gives you footing — is
[`docs/field-guide.md`](docs/field-guide.md).

## What this is not

No web UI, no database, no login, no hosted service, no vendor, no platform
integration, no telemetry. Nothing here phones home. It's a folder of honest
files and one script — which is precisely why it can run anywhere, from a
two-person clinic to a fleet of thousands, unchanged.

## An honest caveat

The heartbeat is only as true as the cards. A card written once and never
updated will produce false calm — keep cards born when agents are born, and
current when agents change. The registry is a discipline wearing a folder as
a costume.

## Roadmap

The card is the atom. Everything later attaches to it without rewriting it:
intake ("request an agent" as a paved road), threat-model passes, the fleet
graph, governance patterns, and the health and lifecycle layer. Each arrives
as an extension — if a later tier would force a rewrite of the card, the
design is wrong.

## License

Code (`check.py`, `tests/`): MIT. Documents (everything else): CC0 — public
domain, no conditions. See [`LICENSE`](LICENSE). Copies of this kit may live
anywhere; the genuine, current version lives at its home repository — check
the well.

---

*Given freely to all.*
