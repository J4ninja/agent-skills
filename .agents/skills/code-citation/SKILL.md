---
name: code-citation
description: Finds original sources and authoritative references for code, then adds inline citation comments in the correct format for the language. Use this skill whenever the user asks to "add citations", "find references", "attribute this code", "where does this come from", "cite this function", or wants to trace the origin of a snippet — even if they don't say the word "citation" explicitly. Also trigger for phrases like "document my sources", "credit this", "what's the origin of this", "I need to attribute this", or "where did this algorithm come from".
---

# Code Citation

Find the original source or authoritative reference for a piece of code and attach it as an inline citation comment, placed directly above the function or class in the correct comment style for the language.

---

## Citation Types

Infer the right tag from context before searching:

| Tag | When to use |
|-----|-------------|
| `Source:` | Code is taken verbatim or near-verbatim from an external location |
| `Adapted from:` | Code is based on an external source but meaningfully changed |
| `Reference:` | Code is original but implements a known algorithm, paper, or pattern |

**Decision rules:**
- User says "I copied this" or code matches a well-known snippet → `Source:`
- User says "I modified" / "based on" / code has structural similarity but differs → `Adapted from:`
- Code is original but implements a named algorithm or standard → `Reference:`
- Uncertain between `Source:` and `Adapted from:` → prefer `Adapted from:` (safer attribution)
- A single function may get **multiple citation lines** (e.g., `Reference:` for the algorithm + `Adapted from:` for a repo)

---

## Bundled Resources

Before doing any research, check these files to save time:

- **`references/citation_patterns.md`** — Pre-mapped well-known algorithms → canonical papers and URLs. If the algorithm appears here, use the mapping directly and skip browser search.
- **`references/languages.md`** — Comment syntax for 50+ languages. Use this to determine the correct comment style before formatting output.
- **`scripts/format_citation.py`** — Deterministic comment formatter. Run it to produce the correctly styled citation line(s).

---

## Comment Format by Language

> **Quick rule**: always consult `references/languages.md` for the authoritative comment style. The examples below cover the most common cases.

```python
# Source: https://...
# Adapted from: https://...
# Reference: <Title> — https://...
def my_function(): ...
```

```javascript
// Source: https://...
// Reference: <Title> — https://...
function myFunction() { ... }
```

```cpp
// Source: https://...
// Reference: <Title> — https://...
void myFunction() { ... }
```

```c
/* Source: https://... */
/* Reference: <Title> — https://... */
void my_function() { ... }
```

```bash
# Source: https://...
# Reference: <Title> — https://...
my_function() { ... }
```

```sql
-- Source: https://...
-- Reference: <Title> — https://...
```

**Formatting rules:**
- Use single-line comment style unless the language requires block comments (e.g., plain C)
- For `Reference:` tags, include a short human-readable title before the `—` separator
- Use the most direct/permanent URL available — deep link to file + line on GitHub when possible
- Never truncate URLs

### Jupyter Notebooks (`.ipynb`)

Code cells use Python syntax. Place the citation at the **top of the cell** that contains the function or class definition. Do not add citations outside cell boundaries.

---

## Steps

### 1. Gather inputs

Extract from context:
- **function_name** — the name of the function or class
- **language** — the programming language (check file extension; see `references/languages.md` for ambiguous extensions)
- **domain** — problem domain or key library (e.g., `numpy`, `ROS`, `drone motion planning`)
- **core_behavior** — one sentence: what does this code do?
- **origin_hint** — any source hint from the user (e.g., "I got this from ROS", "based on VFH+")
- **code_snippet** — the actual code

### 2. Infer citation type

From the inputs and conversation context, decide the likely citation type(s) before searching. This narrows your queries and saves time.

### 3. Check `references/citation_patterns.md` first

Read `references/citation_patterns.md`. If the algorithm or pattern is listed there, use the pre-mapped citation **directly** — skip browser search. This file covers major ML papers, graph algorithms, cryptographic standards, robotics algorithms, and more.

If the algorithm is not in the file, proceed to browser search.

### 4. Formulate search queries (if needed)

```
# If copied — find the original:
Query A: "<distinctive_code_fragment>" site:github.com OR site:stackoverflow.com
Query B: "<function_name>" <language> <domain>

# If algorithm-based — find the canonical reference:
Query C: "<core_behavior>" algorithm OR paper <domain>
Query D: "<domain>" "<key_term>" site:arxiv.org OR site:wikipedia.org OR site:docs.*
```

### 5. Launch browser subagent (if needed)

Use `browser_subagent` with this task:

```
Task: Find the original source and authoritative references for this code.

Function name: <function_name>
Language: <language>
Domain: <domain>
What it does: <core_behavior>
Origin hint: <origin_hint or "none">

Steps:
1. Go to https://www.google.com
2. Search: <Query A>. Open the top 2 results. Record: exact URL (deep link if GitHub), page title, match type.
3. Search: <Query B>. Open the top 2 results. Record the same fields.
4. If no direct source found, search: <Query C>. Open top 2 results. Record: URL, title, relation (paper, docs, etc.).
5. If still needed, search: <Query D>. Open top 1–2 results.

For each result, report:
- URL (exact, deep link preferred)
- Match type: "verbatim copy" | "structural match" | "algorithm source" | "conceptual reference"
- One-sentence description

Stop after finding 1–3 high-confidence citations. Quality over quantity.
```

### 6. Map results to citation tags

| Browser result | Tag |
|----------------|-----|
| Verbatim / near-verbatim match | `Source:` |
| Structural match, code differs | `Adapted from:` |
| Algorithm paper or named pattern | `Reference:` |
| Multiple apply | Use multiple lines |

### 7. Format the output using `scripts/format_citation.py`

Run the script to produce the correctly formatted comment line(s):

```bash
# Single citation
python scripts/format_citation.py \
  --lang python \
  --type "Reference:" \
  --title "Adam: A Method for Stochastic Optimization — Kingma & Ba (2015)" \
  --url "https://arxiv.org/abs/1412.6980"

# Check comment style for an unfamiliar language
python scripts/format_citation.py --detect-style --file mycode.rs

# List all supported languages
python scripts/format_citation.py --list-languages
```

Place the output line(s) **immediately above** the function/class definition, before any existing docstring.

### 8. Return annotated code

Return the annotated code block ready to paste, with a brief note explaining why each citation type was chosen:

```python
# Reference: Adam: A Method for Stochastic Optimization — Kingma & Ba (2015) https://arxiv.org/abs/1412.6980
def adam_update(params, grads, m, v, t, lr=0.001, ...):
    ...
```

---

## Constraints

- **Never fabricate URLs.** If no real link is found, omit that citation and say so explicitly.
- Prefer deep links (file + line) over repo homepage links.
- If a function is entirely original with no traceable algorithm, return no citations and state that clearly — don't invent a citation just to have one.
- Always place citations **above** the function, not inside the docstring or inline.
- Limit browser search to 3–4 queries; stop early if high-confidence citations are found.
- Match comment style exactly to the detected language (use `references/languages.md` when in doubt).
- For Jupyter notebooks, place citations at the top of the code cell, not outside cell boundaries.
