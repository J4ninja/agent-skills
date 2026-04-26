---
name: skills-index
description: Index of all available skills in this workspace. Consult this when you're unsure which skill to use or want to discover available capabilities.
---

# Skills Index

Each skill lives in its own subdirectory and is self-contained. Read its `SKILL.md` for full instructions.

## Locally-owned skills

These are tracked in git and maintained in this repo:

| Skill | Directory | What it does |
|-------|-----------|--------------|
| Code Citation | `code-citation/` | Finds original sources and authoritative references for code, then attaches inline citation comments in the correct language format. |

## Third-party skills (installed via `npx skills add`)

These are **not tracked in git** (see `.gitignore`) and **do not need a manual entry here** — agents discover them automatically by scanning subdirectories. Reinstall them with:

```bash
npx skills add <registry-url> --skill <skill-name>
```

Currently installed third-party skills may include: `skill-creator`, `find-skills`, `vercel-react-best-practices`, and others. Run `ls .agents/skills/` to see what's present locally.

---

## How skills are loaded

Agents scan all subdirectories in `skills/` and read each `SKILL.md` frontmatter (`name` + `description`) automatically — **no manual registration required**. This index exists only as a human-readable reference for skills you own and maintain.

Skills use progressive disclosure:
1. **This index** — always in context, minimal overhead
2. **SKILL.md body** — loaded when skill is invoked
3. **Bundled resources** (scripts, references) — loaded or executed as needed
