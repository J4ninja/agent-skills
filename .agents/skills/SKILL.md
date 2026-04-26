---
name: skills-index
description: Index of all available skills in this workspace. Consult this when you're unsure which skill to use or want to discover available capabilities.
---

# Skills Index

Each skill lives in its own subdirectory and is self-contained. Read its `SKILL.md` for full instructions.

| Skill | Directory | What it does |
|-------|-----------|--------------|
| Code Citation | `code-citation/` | Finds original sources and authoritative references for code, then attaches inline citation comments in the correct language format. |
| Skill Creator | `skill-creator/` | Create new skills, improve existing ones, run evaluations, and optimize skill descriptions for better triggering. |

---

## How skills are loaded

When you start a task, check whether any skill in this index applies. If one does, read that skill's `SKILL.md` and follow its instructions.

Skills use progressive disclosure:
1. **This index** — always in context, minimal overhead
2. **SKILL.md body** — loaded when skill is invoked
3. **Bundled resources** (scripts, references) — loaded or executed as needed
