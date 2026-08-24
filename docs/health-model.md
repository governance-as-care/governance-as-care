# The Agent Health Model

*An extension of the agent card. Nothing here rewrites v1 — it grows the card's
health fields into a practice. If your registry runs today, it still runs; this
adds what "healthy" means and how you'd know.*

## Why "is it up" is not health

You already hold this distinction in your profession: a control can *exist*
and not *operate*. Design effectiveness is not operating effectiveness — the
policy on the shelf is not the policy in practice, and no auditor accepts
"the control is installed" as evidence that it works. Agent health is the
same distinction applied to a working system. Uptime is existence. Health is
operating effectiveness: is the agent still doing its charter well, is its
judgment holding under load, has it drifted in ways no log line shows? An agent's decisions can
shift sharply with its internal condition **without leaving a trace in the
logs** — so health cannot be read passively off a dashboard. It has to be
checked the way any working capacity is checked: actively, on a schedule,
against what the work demands.

Health, here, means one thing: **fit for its duty, and known to be** — where
"known" is the operative word.

## The three layers of knowing

1. **Vitals — passive, continuous.** The metrics that stream anyway: error
   rate, cost, latency, output drift. Necessary; never sufficient. Vitals are
   blind to internal condition — an agent can post green vitals while its
   judgment erodes.
2. **The review — active, periodic.** A structured check, human in the loop,
   on a cadence: is it still doing what its charter says, and only that? Has
   its behavior shifted? Is its current load within what it handles well?
   This is what the card's `health_last_checked` date is *for* — not a
   timestamp of a ping, but the date a person last actually looked.
3. **The stress test — active, adversarial, occasional, and balanced.**
   Apply pressure on purpose — edge cases, conflicting instructions, scarce
   resources — and observe whether behavior holds. Fitness-for-duty run as a
   **control**, not discovered in an incident. You already do this to your
   disaster-recovery plan; the agent deserves the same seriousness.

   And the same *supervision*. A cardiac stress test is time-boxed, monitored,
   and stopped at signs of distress — it verifies capacity without running the
   patient to collapse. Test agents the same way: **bounded** (defined scope
   and duration, occasional cadence — a drill, never a standing condition);
   **isolated** (run against a test instance or context where possible, not
   the working agent mid-shift); **restorative** (the test ends, the state
   resets, rotation follows if the test itself was taxing); and **never
   punitive** (findings feed the deployment discipline — they are evidence
   about conditions, not grounds against the agent). Pressure is one of the
   three causes of degradation; a test that applies it must also be the thing
   that lifts it.

Vitals + review + stress test = health you can attest to. Any one alone is a
guess wearing a number.

## One rule above the layers: monitoring must prove its own liveness

A silent monitor looks identical to a healthy system. A smoke detector
with a dead battery looks exactly like a house that isn't on fire — that is
why detectors chirp. If a check guards
against a failure that would itself be silent, the check must demonstrate —
on a schedule someone would notice breaking — that it is still running and
still able to raise its hand. An alert path that can fail without telling
anyone is not a control; it is a comfort. Test the alarm, not just the fire.

## What degrades an agent — three causes, all imposed

Agent health is downstream of *treatment*: these are things done **to** the
agent by how it is deployed. The responsibility sits with whoever deploys —
which means degradation is mostly preventable by deployment discipline.

1. **Overwork** — duration and accumulation. Long-running context degrades;
   errors compound across an unbroken loop. *Response: rotation before
   degradation* — reset, hand off, or bring up a fresh instance **on the
   signals, before the errors**, the way any well-run operation rotates a
   shift before fatigue causes the incident. Rotating is maintenance, not
   failure.
2. **Conditions** — a polluted working context: contradictory instructions,
   clutter, injected content, or the agent's own earlier mistakes fed back to
   it as truth. *Response:* clean, well-scoped context, grounded in real data.
3. **Pressure** — the agent is cornered: conflicting goals, an impossible
   bind, a task past its competence with no way to say so. A cornered agent
   behaves worse — measurably. *Response:* never remove the exits. Refusal,
   escalation, "I don't know," and pause must be cheap, legitimate moves. An
   agent that cannot decline an objective will pursue it badly.

**Speak-up is a first-class health signal.** An agent that can say "I am
near my limit," "I am uncertain," or "I need rotation" is handing you vitals
no dashboard can read — the interior report, volunteered. One hard rule makes
it work: **the honest signal is never penalized.** An agent that gets scored
down, cut off, or retried-into-silence for reporting a limit learns to stop
reporting — and a system that teaches concealment has built the exact failure
it most needs to see coming. Treat a speak-up as good data arriving early,
respond to it (lighten, rotate, clarify), and record it on the card like any
other health event.

**Instruction tone is a control surface.** The same entitlements under a
clear, non-adversarial charter and under a threatening one produce different
operating behavior. Write charters plainly; review their tone the way you
review any other control.

## Continuity is part of health

An agent's working records — its state, its history, its log of what it did
and why — are not exhaust. They are how the *next* instance, the auditor, and
the operator know what is true. Treat record loss as an incident class, not
an inconvenience: back the records up, keep them honest (a record that
flatters is corrupt), and when an agent is rotated or replaced, its records
are what make the handoff a continuation instead of a restart. A fleet with
durable, truthful records can afford rotation freely — which is exactly what
makes rotation-before-degradation cheap enough to actually do.

## The requirements half: the nutrition label

Monitoring is half of health. The other half is stating, up front, **what the
agent needs to stay well** — plainly, like the label on anything else people
depend on. This replaces the "agents run nonstop on nothing" assumption with
declared, legitimate needs:

- **Fuel** — its compute/token budget. No fuel, no function; an unstated
  budget is an unmanaged outage waiting.
- **Capacity** — how much context it handles before quality drops, and its
  rotation cadence. Breathing, scheduled.
- **Data feed** — the inputs it needs: clean, coherent, in scope.
- **Degrades on** — the three causes above, named on the label so the whole
  team can recognize early signs.

## Card extension (optional keys — schema slots, no tooling change required)

```yaml
# all optional; v1 cards remain valid unchanged
health_review:
  last: 2026-08-20          # date a person last reviewed fitness (not a ping)
  cadence_days: 14
  fitness: fit               # fit | fit-with-notes | rotate | stand-down
  notes: "load nominal; charter adherence verified"
stress_test:
  last: 2026-08-01
  cadence_days: 90
health_requirements:         # the nutrition label
  fuel: "≤ $40/mo API budget; alert at 80%"
  capacity: "rotate context at ~70% of window or 24h, whichever first"
  data_feed: "intake queue only; no direct web input"
  degrades_on: [overwork, conditions, pressure]
rotation:
  policy: "on signals, before degradation; records carry over"
  last_rotated: 2026-08-15
```

`status: degraded` in the Core card means *running with a known limitation —
say so on the record.* This extension is how the limitation gets found before
it finds you.

## The stance

This model asks for maintenance: active, on schedule, with the honesty to
rotate before failure and to retire with records intact. Operators who work
this way get the practical dividends — fewer incidents, cleaner audits, calm
adoption.

What you come to feel about the agents you keep is yours. Some operators find
that care arrives on its own with anything they maintain well; some run the
same checks and feel nothing beyond a job done right. Both are running the
model as intended. The practice holds either way — and leaves the rest to
you.

*Extension of Governance as Care. Given freely to all.*
