#!/usr/bin/env python3
"""
format_citation.py — Deterministic citation comment formatter for code-citation skill.

Usage:
    python format_citation.py \
        --lang python \
        --type "Reference:" \
        --title "Attention Is All You Need — Vaswani et al. (2017)" \
        --url "https://arxiv.org/abs/1706.03762"

    python format_citation.py \
        --lang javascript \
        --type "Source:" \
        --url "https://github.com/example/repo/blob/main/src/utils.js#L42"

    python format_citation.py --detect-style --file mycode.py

Output:
    Prints the correctly formatted citation comment line(s) to stdout.
    The agent pastes this directly above the function/class definition.
"""

import argparse
import sys
import os

# ---------------------------------------------------------------------------
# Comment style table
# Single-line prefix is preferred; block_open/block_close used when no single
# ---------------------------------------------------------------------------
COMMENT_STYLES = {
    # single-line styles
    "python":     {"single": "#",  "block_open": None,   "block_close": None},
    "ruby":       {"single": "#",  "block_open": None,   "block_close": None},
    "r":          {"single": "#",  "block_open": None,   "block_close": None},
    "julia":      {"single": "#",  "block_open": None,   "block_close": None},
    "elixir":     {"single": "#",  "block_open": None,   "block_close": None},
    "perl":       {"single": "#",  "block_open": None,   "block_close": None},
    "bash":       {"single": "#",  "block_open": None,   "block_close": None},
    "shell":      {"single": "#",  "block_open": None,   "block_close": None},
    "zsh":        {"single": "#",  "block_open": None,   "block_close": None},
    "fish":       {"single": "#",  "block_open": None,   "block_close": None},
    "powershell": {"single": "#",  "block_open": None,   "block_close": None},
    "yaml":       {"single": "#",  "block_open": None,   "block_close": None},
    "toml":       {"single": "#",  "block_open": None,   "block_close": None},
    "dockerfile": {"single": "#",  "block_open": None,   "block_close": None},
    "makefile":   {"single": "#",  "block_open": None,   "block_close": None},
    "hcl":        {"single": "#",  "block_open": None,   "block_close": None},
    "terraform":  {"single": "#",  "block_open": None,   "block_close": None},
    "nix":        {"single": "#",  "block_open": None,   "block_close": None},
    "coffeescript": {"single": "#","block_open": None,   "block_close": None},
    "javascript": {"single": "//", "block_open": None,   "block_close": None},
    "typescript": {"single": "//", "block_open": None,   "block_close": None},
    "jsx":        {"single": "//", "block_open": None,   "block_close": None},
    "tsx":        {"single": "//", "block_open": None,   "block_close": None},
    "java":       {"single": "//", "block_open": None,   "block_close": None},
    "kotlin":     {"single": "//", "block_open": None,   "block_close": None},
    "swift":      {"single": "//", "block_open": None,   "block_close": None},
    "go":         {"single": "//", "block_open": None,   "block_close": None},
    "rust":       {"single": "//", "block_open": None,   "block_close": None},
    "cpp":        {"single": "//", "block_open": None,   "block_close": None},
    "cxx":        {"single": "//", "block_open": None,   "block_close": None},
    "csharp":     {"single": "//", "block_open": None,   "block_close": None},
    "cs":         {"single": "//", "block_open": None,   "block_close": None},
    "php":        {"single": "//", "block_open": None,   "block_close": None},
    "scala":      {"single": "//", "block_open": None,   "block_close": None},
    "dart":       {"single": "//", "block_open": None,   "block_close": None},
    "groovy":     {"single": "//", "block_open": None,   "block_close": None},
    "fsharp":     {"single": "//", "block_open": None,   "block_close": None},
    "solidity":   {"single": "//", "block_open": None,   "block_close": None},
    "scss":       {"single": "//", "block_open": None,   "block_close": None},
    "less":       {"single": "//", "block_open": None,   "block_close": None},
    "sql":        {"single": "--", "block_open": None,   "block_close": None},
    "haskell":    {"single": "--", "block_open": None,   "block_close": None},
    "lua":        {"single": "--", "block_open": None,   "block_close": None},
    "ada":        {"single": "--", "block_open": None,   "block_close": None},
    "matlab":     {"single": "%",  "block_open": None,   "block_close": None},
    "octave":     {"single": "%",  "block_open": None,   "block_close": None},
    "erlang":     {"single": "%",  "block_open": None,   "block_close": None},
    "latex":      {"single": "%",  "block_open": None,   "block_close": None},
    "prolog":     {"single": "%",  "block_open": None,   "block_close": None},
    "fortran":    {"single": "!",  "block_open": None,   "block_close": None},
    "vimscript":  {"single": '"',  "block_open": None,   "block_close": None},
    "clojure":    {"single": ";;", "block_open": None,   "block_close": None},
    "lisp":       {"single": ";",  "block_open": None,   "block_close": None},
    "scheme":     {"single": ";",  "block_open": None,   "block_close": None},
    "asm":        {"single": ";",  "block_open": None,   "block_close": None},
    "wasm":       {"single": ";;", "block_open": None,   "block_close": None},
    "cobol":      {"single": "*>", "block_open": None,   "block_close": None},
    # block-only styles
    "c":          {"single": None, "block_open": "/*",   "block_close": "*/"},
    "css":        {"single": None, "block_open": "/*",   "block_close": "*/"},
    "html":       {"single": None, "block_open": "<!--", "block_close": "-->"},
    "xml":        {"single": None, "block_open": "<!--", "block_close": "-->"},
    "markdown":   {"single": None, "block_open": "<!--", "block_close": "-->"},
    "ocaml":      {"single": None, "block_open": "(*",   "block_close": "*)"},
}

# Extension → language name
EXT_MAP = {
    ".py": "python", ".pyw": "python",
    ".rb": "ruby",
    ".r": "r", ".R": "r",
    ".jl": "julia",
    ".ex": "elixir", ".exs": "elixir",
    ".pl": "perl", ".pm": "perl",
    ".sh": "bash", ".bash": "bash", ".zsh": "zsh", ".fish": "fish",
    ".ps1": "powershell", ".psm1": "powershell",
    ".yaml": "yaml", ".yml": "yaml",
    ".toml": "toml",
    ".js": "javascript", ".mjs": "javascript", ".cjs": "javascript",
    ".ts": "typescript",
    ".jsx": "jsx", ".tsx": "tsx",
    ".java": "java",
    ".kt": "kotlin", ".kts": "kotlin",
    ".swift": "swift",
    ".go": "go",
    ".rs": "rust",
    ".cpp": "cpp", ".cc": "cpp", ".cxx": "cxx", ".hpp": "cpp",
    ".cs": "csharp",
    ".php": "php",
    ".scala": "scala",
    ".dart": "dart",
    ".groovy": "groovy",
    ".fs": "fsharp", ".fsi": "fsharp",
    ".sol": "solidity",
    ".scss": "scss", ".sass": "scss",
    ".less": "less",
    ".sql": "sql",
    ".hs": "haskell", ".lhs": "haskell",
    ".lua": "lua",
    ".ada": "ada", ".ads": "ada",
    ".m": "matlab",  # NOTE: also Objective-C; resolve by context
    ".erl": "erlang", ".hrl": "erlang",
    ".tex": "latex",
    ".f90": "fortran", ".f95": "fortran", ".f": "fortran",
    ".vim": "vimscript",
    ".clj": "clojure", ".cljs": "clojure",
    ".lisp": "lisp", ".el": "lisp",
    ".scm": "scheme",
    ".asm": "asm", ".s": "asm",
    ".wat": "wasm",
    ".cob": "cobol", ".cbl": "cobol",
    ".c": "c", ".h": "c",
    ".css": "css",
    ".html": "html", ".htm": "html",
    ".xml": "xml",
    ".md": "markdown",
    ".ml": "ocaml", ".mli": "ocaml",
    ".tf": "terraform", ".hcl": "hcl",
    ".nix": "nix",
    ".ipynb": "python",  # Jupyter cells use Python comments
}

VALID_TAGS = {"Source:", "Adapted from:", "Reference:"}


def detect_language(filepath: str) -> str | None:
    """Return language name from file extension, or None if unknown."""
    _, ext = os.path.splitext(filepath)
    return EXT_MAP.get(ext)


def format_citation(lang: str, tag: str, url: str, title: str = "") -> str:
    """
    Return a single formatted citation comment line for the given language.

    Args:
        lang:  Language identifier (e.g. "python", "javascript", "c")
        tag:   One of "Source:", "Adapted from:", "Reference:"
        url:   The citation URL (never truncated)
        title: Human-readable title for Reference: tags (optional for others)

    Returns:
        A ready-to-paste comment string (no trailing newline).

    Raises:
        ValueError: If the language is unknown or the tag is invalid.
    """
    lang = lang.lower().strip()
    if lang not in COMMENT_STYLES:
        raise ValueError(
            f"Unknown language: {lang!r}. "
            f"Add it to COMMENT_STYLES or use --detect-style with a file path."
        )

    if tag not in VALID_TAGS:
        raise ValueError(
            f"Invalid tag: {tag!r}. Must be one of: {', '.join(VALID_TAGS)}"
        )

    style = COMMENT_STYLES[lang]

    # Build the body of the citation line
    if tag == "Reference:" and title:
        body = f"Reference: {title} {url}"
    elif tag == "Reference:":
        body = f"Reference: {url}"
    elif tag == "Adapted from:":
        body = f"Adapted from: {url}"
    else:
        body = f"Source: {url}"

    # Apply comment syntax
    if style["single"]:
        return f"{style['single']} {body}"
    else:
        open_tok = style["block_open"]
        close_tok = style["block_close"]
        return f"{open_tok} {body} {close_tok}"


def format_citations_block(citations: list[dict], lang: str) -> str:
    """
    Format multiple citation lines as a ready-to-paste block.

    Each dict in citations must have: tag, url, and optionally title.
    Lines are returned in the order: Reference: → Adapted from: → Source:
    """
    order = {"Reference:": 0, "Adapted from:": 1, "Source:": 2}
    sorted_citations = sorted(citations, key=lambda c: order.get(c["tag"], 99))
    lines = [
        format_citation(lang, c["tag"], c["url"], c.get("title", ""))
        for c in sorted_citations
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Format citation comments for the code-citation skill.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--lang", help="Language name (e.g. python, javascript, c)")
    parser.add_argument("--file", help="Source file path — used to auto-detect language")
    parser.add_argument(
        "--detect-style",
        action="store_true",
        help="Print the comment style for the given --file or --lang and exit",
    )
    parser.add_argument(
        "--type",
        dest="tag",
        choices=["Source:", "Adapted from:", "Reference:"],
        help="Citation tag type",
    )
    parser.add_argument("--url", help="Citation URL")
    parser.add_argument("--title", default="", help="Human-readable title (for Reference: tags)")
    parser.add_argument(
        "--list-languages",
        action="store_true",
        help="Print all supported language names and exit",
    )

    args = parser.parse_args()

    if args.list_languages:
        for name in sorted(COMMENT_STYLES):
            style = COMMENT_STYLES[name]
            prefix = style["single"] or f"{style['block_open']}...{style['block_close']}"
            print(f"  {name:<20} {prefix}")
        return

    # Resolve language
    lang = args.lang
    if not lang and args.file:
        lang = detect_language(args.file)
        if not lang:
            print(
                f"Error: could not detect language from {args.file!r}. "
                "Use --lang to specify it manually.",
                file=sys.stderr,
            )
            sys.exit(1)

    if args.detect_style:
        if not lang:
            print("Error: provide --lang or --file to detect style.", file=sys.stderr)
            sys.exit(1)
        style = COMMENT_STYLES.get(lang.lower())
        if not style:
            print(f"Error: unknown language {lang!r}", file=sys.stderr)
            sys.exit(1)
        if style["single"]:
            print(f"Single-line: {style['single']}")
        else:
            print(f"Block: {style['block_open']} ... {style['block_close']}")
        return

    # Validate required args for citation formatting
    if not lang:
        parser.error("--lang or --file is required")
    if not args.tag:
        parser.error("--type is required")
    if not args.url:
        parser.error("--url is required")

    try:
        result = format_citation(lang, args.tag, args.url, args.title)
        print(result)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
