# Language Comment Styles

Use this table to choose the correct comment syntax when inserting citation comments.
Single-line style is preferred where available. Fall back to block style only when marked.

## Quick Lookup

| Language | Extension(s) | Single-line | Block | Citation format |
|----------|--------------|-------------|-------|-----------------|
| Python | `.py`, `.pyw` | `#` | `"""..."""` | `# Source: ...` |
| JavaScript | `.js`, `.mjs`, `.cjs` | `//` | `/* */` | `// Source: ...` |
| TypeScript | `.ts`, `.tsx` | `//` | `/* */` | `// Source: ...` |
| JSX | `.jsx` | `//` | `/* */` | `// Source: ...` |
| C | `.c`, `.h` | ❌ (use block) | `/* */` | `/* Source: ... */` |
| C++ | `.cpp`, `.cc`, `.cxx`, `.hpp` | `//` | `/* */` | `// Source: ...` |
| C# | `.cs` | `//` | `/* */` | `// Source: ...` |
| Java | `.java` | `//` | `/* */` | `// Source: ...` |
| Kotlin | `.kt`, `.kts` | `//` | `/* */` | `// Source: ...` |
| Swift | `.swift` | `//` | `/* */` | `// Source: ...` |
| Go | `.go` | `//` | `/* */` | `// Source: ...` |
| Rust | `.rs` | `//` | `/* */` | `// Source: ...` |
| Ruby | `.rb` | `#` | `=begin...=end` | `# Source: ...` |
| Perl | `.pl`, `.pm` | `#` | `=pod...=cut` | `# Source: ...` |
| PHP | `.php` | `//` | `/* */` | `// Source: ...` |
| Bash / Shell | `.sh`, `.bash`, `.zsh` | `#` | ❌ | `# Source: ...` |
| PowerShell | `.ps1`, `.psm1` | `#` | `<# #>` | `# Source: ...` |
| Fish | `.fish` | `#` | ❌ | `# Source: ...` |
| SQL | `.sql` | `--` | `/* */` | `-- Source: ...` |
| MySQL / PostgreSQL | `.sql` | `--` | `/* */` | `-- Source: ...` |
| R | `.r`, `.R` | `#` | ❌ | `# Source: ...` |
| MATLAB | `.m` | `%` | `%{...%}` | `% Source: ...` |
| Julia | `.jl` | `#` | `#=...=#` | `# Source: ...` |
| Scala | `.scala` | `//` | `/* */` | `// Source: ...` |
| Haskell | `.hs`, `.lhs` | `--` | `{- -}` | `-- Source: ...` |
| Elixir | `.ex`, `.exs` | `#` | ❌ | `# Source: ...` |
| Erlang | `.erl`, `.hrl` | `%` | ❌ | `% Source: ...` |
| Clojure | `.clj`, `.cljs` | `;;` | ❌ | `;; Source: ...` |
| Lisp | `.lisp`, `.el` | `;` | ❌ | `; Source: ...` |
| Lua | `.lua` | `--` | `--[[ ]]` | `-- Source: ...` |
| Dart | `.dart` | `//` | `/* */` | `// Source: ...` |
| YAML | `.yaml`, `.yml` | `#` | ❌ | `# Source: ...` |
| TOML | `.toml` | `#` | ❌ | `# Source: ...` |
| Dockerfile | `Dockerfile` | `#` | ❌ | `# Source: ...` |
| Makefile | `Makefile` | `#` | ❌ | `# Source: ...` |
| HCL / Terraform | `.tf`, `.hcl` | `#` | `/* */` | `# Source: ...` |
| Nix | `.nix` | `#` | `/* */` | `# Source: ...` |
| Vim script | `.vim` | `"` | ❌ | `" Source: ...` |
| HTML | `.html`, `.htm` | ❌ | `<!-- -->` | `<!-- Source: ... -->` |
| CSS | `.css` | ❌ | `/* */` | `/* Source: ... */` |
| SCSS / Sass | `.scss`, `.sass` | `//` | `/* */` | `// Source: ...` |
| Less | `.less` | `//` | `/* */` | `// Source: ...` |
| Assembly (x86/ARM) | `.asm`, `.s` | `;` or `#` | ❌ | `; Source: ...` |
| Fortran (modern) | `.f90`, `.f95` | `!` | ❌ | `! Source: ...` |
| Ada | `.ada`, `.ads` | `--` | ❌ | `-- Source: ...` |
| COBOL | `.cob`, `.cbl` | `*>` | ❌ | `*> Source: ...` |
| Jupyter Notebook | `.ipynb` | `#` (in code cells) | ❌ | `# Source: ...` |
| Markdown | `.md` | ❌ | `<!-- -->` | `<!-- Source: ... -->` |
| LaTeX | `.tex` | `%` | ❌ | `% Source: ...` |
| Prolog | `.pl`, `.pro` | `%` | `/* */` | `% Source: ...` |
| OCaml | `.ml`, `.mli` | ❌ | `(* *)` | `(* Source: ... *)` |
| F# | `.fs`, `.fsi` | `//` | `(* *)` | `// Source: ...` |
| Solidity | `.sol` | `//` | `/* */` | `// Source: ...` |
| WebAssembly (WAT) | `.wat` | `;;` | ❌ | `;; Source: ...` |

---

## Multi-line Reference Format

When a `Reference:` tag needs a title, always use the `—` em dash separator:

```python
# Reference: Algorithm Name — Author(s) (Year) https://url
```

```javascript
// Reference: Algorithm Name — Author(s) (Year) https://url
```

```sql
-- Reference: Algorithm Name — Author(s) (Year) https://url
```

For block-only languages (C, HTML, CSS, OCaml):

```c
/* Reference: Algorithm Name — Author(s) (Year) https://url */
```

---

## Jupyter Notebook Special Cases

Notebooks (`.ipynb`) contain Python code cells — use `#` prefix. Place the citation at the **top of the cell** containing the function/class, not outside the cell boundaries.

If the function spans multiple cells (split definition), cite the first cell where the definition begins.

---

## Ambiguous Extensions

Some extensions are shared (e.g., `.pl` is Perl and Prolog, `.m` is MATLAB and Objective-C). Resolve by:
1. Looking at the shebang line (`#!/usr/bin/env perl`)
2. Looking at imports/keywords in the file
3. Asking the user if still unclear
