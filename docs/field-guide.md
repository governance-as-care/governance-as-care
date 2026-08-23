# The Field Guide — every card field, and why it gives you footing

The card exists to answer, for any agent you run, the questions that let you
operate with a clear head:

- What *is* this agent, and who answers for it?
- What can it touch — and what can it never touch?
- How do we stop it, and who is allowed to?
- Is it healthy, and when did it last change?

Each field below is one piece of that footing. Fill them honestly; the card is
only as true as what you write on it.

---

## `id` — machine identity

The permanent technical identifier. Authorization acts on it. The kill path
acts on it. It never changes for the life of the agent — if the ID changes,
that is a new agent with a new card.

**How to fill it:** whatever string your systems already use, or mint one:
`agent-<function>-<number>`.

## `name` — the nickname *(optional)*

Teams often end up calling an agent something, and the card has a place for it.
Recording the name people already use means hallway conversation resolves to a
real card, and one shared name keeps the whole organization pointing at the
same agent.

**The hard rule:** the nickname never does the machine's job. You revoke
`id`. You never "kill Scribe" by name and hope the right thing died.

## `owner` — the accountable person

A person, not a team. Teams reorganize; accountability with no name on it is
how agents end up orphaned. If you cannot find a person willing to put their
name here, you have found your first real finding — the card is already working.

## `charter` — one sentence

What the agent is *for*. One sentence, deliberately: the constraint is the
control. A charter you can hold in your head is a charter you can notice drift
against. If the agent starts doing something the sentence doesn't cover,
that's not initiative — that's a change, and changes get reviewed.

## `data_classification` — classify, period

**Required. Never blank.** The controlled vocabulary starts at:
`public · confidential · pii · phi · pci` (extend it if your world needs more).
`public` is the floor — so an empty field is a validation failure, never a
quiet "probably nothing." The card carries the union of what applies, and the
most restrictive class sets the regime.

For each regulated class (`pii`, `phi`, `pci`), the card's `data_review` slot
holds what makes it legitimate: the agreement (a BAA for PHI, a DPA for PII, a
PCI attestation), the scope, the retention, and **where every component runs** —
model, orchestration, tools, logs, support. An agent inherits the regime of
every component's location. One point that surprises people (this is a field
observation, not legal advice): an agent does not automatically fall under the
model provider's agreement — each component that touches regulated data needs
its own coverage.

**Re-classify whenever the agent's data scope changes.** That edit is
load-bearing — it can change which laws apply — so it is a reviewed change,
never a silent one.

## `can_touch` / `cannot_touch` — entitlements and limits, side by side

What it may reach (system + read/write), and what it must never reach, in the
same place, so anyone reading learns both at once. The `cannot_touch` list is
not decoration — it is the sentence you will be glad you wrote down the day
someone proposes "just letting it also send the emails."

## `kill_path` — how it stops, and who may stop it

A mechanism and a person. "Revoke the key in the vault; Ops has access; dies
in under a minute; owner or one other may pull it." If stopping the agent
requires a meeting, the kill path is a finding. This field is written for
3 a.m., for someone who is not the person who built it.

## `model` / `model_verified` — noticing silent drift

Providers update models. Your agent can change without anyone at your
organization doing anything — that is **silent drift**, and it is invisible
unless you look. `model` records what you believe it runs on;
`model_verified` records when you last confirmed that belief. The heartbeat
flags cards whose verification has aged past the threshold (default 30 days) —
not because drift already happened, but because *you no longer know*.

## `version` / `last_changed` / `last_approved_by` — the change stamp

The minimum change control: what iteration this is, when it last changed, and
which person approved it. In the git form, `git log` on the card file is the
full history for free — who changed what, when, in whose commit.

## `status` / `health_last_checked` — alive, degraded, retired

`active` means in service. `degraded` means running with a known limitation —
say so, on the record. `retired` means out of service *and still on the books*:
retired cards stay in the registry because an inventory that forgets what it
used to run cannot answer "did we ever have an agent that touched X?"
Freshness checks skip retired agents; existence checks never do.

---

# Extended fields (schema slots, tooled later)

The card reserves optional keys the later tiers fill in — adding them never
requires a rewrite:

`aliases` (the other names the agent goes by across systems, so an incident
never stalls on "is X the same as Y?") · `data_review` (per-class coverage —
already used by the heartbeat's coverage check) · `retention` · `token_budget`
(spend as a bound on agency) · `maestro` (threat-model results) · `incidents`
(what happened and what changed after) · `attestation` · `change_approval`
(which field-edits need which gate) · `self_change_boundary` (for agents that
modify themselves: the bounds they may not cross).

---

# Why a card at all

Because the alternative is a fleet of important things nobody can enumerate,
stop, or answer for — and everyone who works near that feels it, whether or
not they say it. A card is small. Ten minutes, honestly. But an organization
whose every agent has an accountable person, a one-sentence purpose, declared
data, a written limit, and a 3 a.m. off-switch is an organization that can
adopt the next agent *calmly* — and calm adoption, more than any control
framework, is what this kit is for.

Governance is care made auditable — care for the people who depend on the
agents, and care for the agents' own good working order. Both readings are
intended.
