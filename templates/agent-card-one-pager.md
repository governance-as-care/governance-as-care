# Agent Card — one-page form (no tools required)

*Print it, or copy it into any document. Fill in every line. When you're ready
for the full kit, these answers drop straight into the file template at
`templates/agent-card.md` — same fields, same order. Ten minutes, honestly.*

---

**1. What is this agent's ID?**
The permanent technical identifier — the string your systems know it by.
`________________________________________`

**2. What do people call it?** *(optional, recommended)*
The hallway name. Write down what people actually say.
`________________________________________`

**3. Who is accountable for it?**
One person, by name and role. Not a team. If nobody's name fits here, that is
the first finding.
`________________________________________`

**4. What is it FOR? (one sentence)**
If you need two sentences, you may have two agents.
`________________________________________`

**5. What kinds of data does it work with?** *(circle all that apply — never leave blank)*
`public   confidential   pii   phi   pci`
For each circled item right of "confidential": what coverage makes it
legitimate (agreement, scope, retention, where the components run)?
`________________________________________`

**6. What can it touch?** *(systems + read/write)*
`________________________________________`
`________________________________________`

**7. What can it never touch?**
Write the limits down where everyone can see them.
`________________________________________`
`________________________________________`

**8. How do you stop it, and who is allowed to?**
A mechanism and a person. If stopping it requires a meeting, that is a finding.
`________________________________________`

**9. What model does it run on, and when did you last verify that?**
Providers update models. Verifying is how you notice.
Model: `__________________`  Verified on: `____ / ____ / ______`

**10. Version and health.**
Version: `______`  Last changed: `____ / ____ / ______`  Approved by: `____________`
Status (circle): `active  degraded  retired`   Health last checked: `____ / ____ / ______`

---

*If you filled every line, you have a real agent card. Keep it wherever your
team already keeps its records — a git repo, a ServiceNow or CMDB entry, a
Confluence or SharePoint page, or printed beside the desk — and update it when
the agent changes. The card is only as good as it is current.*
