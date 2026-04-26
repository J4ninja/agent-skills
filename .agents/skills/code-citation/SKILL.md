---
name: code-citation
description: Finds original sources and authoritative references for code, then adds inline citation comments in the correct format for the language. Use this skill whenever the user asks to "add citations", "find references", "attribute this code", "where does this come from", "cite this function", or wants to trace the origin of a snippet — even if they don't say the word "citation" explicitly.
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

## Comment Format by Language

Place citation comments **immediately above** the function/class definition, before any existing docstring.

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

---

## Steps

### 1. Gather inputs

Extract from context:
- **function_name** — the name of the function or class
- **language** — the programming language
- **domain** — problem domain or key library (e.g., `numpy`, `ROS`, `drone motion planning`)
- **core_behavior** — one sentence: what does this code do?
- **origin_hint** — any source hint from the user (e.g., "I got this from ROS", "based on VFH+")
- **code_snippet** — the actual code

### 2. Infer citation type

From the inputs and conversation context, decide the likely citation type(s) before searching. This narrows your queries and saves time.

### 3. Formulate search queries

```
# If copied — find the original:
Query A: "<distinctive_code_fragment>" site:github.com OR site:stackoverflow.com
Query B: "<function_name>" <language> <domain>

# If algorithm-based — find the canonical reference:
Query C: "<core_behavior>" algorithm OR paper <domain>
Query D: "<domain>" "<key_term>" site:arxiv.org OR site:wikipedia.org OR site:docs.*
```

### 4. Launch browser subagent

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

### 5. Map results to citation tags

| Browser result | Tag |
|----------------|-----|
| Verbatim / near-verbatim match | `Source:` |
| Structural match, code differs | `Adapted from:` |
| Algorithm paper or named pattern | `Reference:` |
| Multiple apply | Use multiple lines |

### 6. Output

Return the annotated code block ready to paste, with a brief note explaining why each citation type was chosen:

```python
# Reference: VFH+ (Vector Field Histogram Plus) — Ulrich & Borenstein (1998) https://ieeexplore.ieee.org/document/704402
# Adapted from: https://github.com/ros-planning/navigation/blob/noetic-devel/navfn/src/navfn.cpp
def generate_steering_candidates(heading, step_angle, max_angle, distances):
    """Generate (angle, distance) candidate pairs for drone obstacle avoidance."""
    ...
```

---

## Constraints

- **Never fabricate URLs.** If no real link is found, omit that citation and say so explicitly.
- Prefer deep links (file + line) over repo homepage links.
- If a function is entirely original with no traceable algorithm, return no citations and state that.
- Always place citations **above** the function, not inside the docstring or inline.
- Limit browser search to 3–4 queries; stop early if high-confidence citations are found.
- Match comment style exactly to the detected language.
