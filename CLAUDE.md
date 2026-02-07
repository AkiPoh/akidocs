# Akidocs — AI Assistant Guide

Guide for AI assistants working on the Akidocs codebase.

## Project Overview

Akidocs is a Markdown-to-PDF converter CLI tool written in Python. The main package lives in `akidocs-core/`. It is in alpha development (v0.3.0.dev0).

- **Language**: Python 3.14+
- **Package manager**: `uv`
- **Production dependency**: `fpdf2` (PDF generation)
- **Test framework**: `pytest`
- **License**: Apache 2.0

## Before Starting Any Work

**NEVER work directly on `main`.** Create a feature branch before writing any code. All work happens on branches — `main` only receives changes through merged PRs.

Before writing code or making changes, always verify the starting state:

1. **Create a branch** — `git checkout -b feat/your-feature` (or `fix/`, `chore/`, etc.). Do this first, before any changes. Never accumulate uncommitted work on `main`
2. **Up to date with main** — run `git fetch origin main` and check that your branch is not behind `origin/main`. Rebase if needed before starting
3. **Clean working tree** — run `git status` to ensure there are no uncommitted changes from previous work
4. **Dependencies synced** — run `uv sync` in `akidocs-core/` if there's any chance dependencies changed

Catching these issues at the start is far cheaper than discovering them mid-work (e.g., merge conflicts after writing code, wrong branch name on a PR).

## Quick Reference

```bash
# All commands run from akidocs-core/
cd akidocs-core

# Install dependencies and package
uv sync

# Run tests
uv run python -m pytest
uv run python -m pytest -v          # verbose

# Lint
uv run ruff check .
uv run ruff check . --fix     # auto-fix safe violations

# Format
uv run ruff format .
uv run ruff format --check .  # check without modifying

# Run the CLI (dev invocation)
uv run aki input.md output.pdf
uv run aki input.md output.pdf -o         # open after creation
uv run aki input.md output.pdf -s times   # use "times" style
```

> **Windows/Git Bash note:** `uv run pytest` fails with "Failed to canonicalize script path" on Windows under Git Bash. Use `uv run python -m pytest` instead. This applies to all pytest invocations throughout this document.

## Project Structure

```
akidocs/
├── akidocs-core/                  # Main Python package
│   ├── src/akidocs_core/          # Source code
│   │   ├── __init__.py            # Package init
│   │   ├── cli.py                 # CLI entry point (argparse)
│   │   ├── tokenizer.py           # Block-level tokenization (headers, paragraphs)
│   │   ├── inline_tokenizer.py    # Inline style tokenization (bold, italic)
│   │   ├── tokens.py              # Data classes: Token, Header, Paragraph, InlineText
│   │   ├── renderer.py            # PDF generation via fpdf2
│   │   ├── styles.py              # Style presets (generic, times, regard)
│   │   ├── style_base.py          # Style dataclass and unit conversion (pt <-> mm)
│   │   ├── opener.py              # Cross-platform file opening
│   │   └── __main__.py            # Module entry point
│   ├── tests/                     # pytest test suite
│   │   ├── test_cli.py            # CLI integration tests (subprocess-based)
│   │   ├── test_tokenizer.py      # Block tokenizer unit tests
│   │   ├── test_inline_tokenizer.py
│   │   ├── test_renderer.py
│   │   └── test_opener.py         # Platform-specific tests with mocking
│   ├── test.md                    # Visual test — render to PDF to verify output. Update when adding features
│   ├── pyproject.toml             # Package config and dependencies
│   ├── uv.lock                    # Dependency lock file
│   └── .python-version            # Python 3.14
├── .github/workflows/test.yml     # CI: runs pytest on push/PR to main
├── README.md
├── DEVELOPMENT.md                 # PR/issue naming conventions
└── CHANGELOG.md                   # Version history
```

## Architecture

The processing pipeline flows in one direction:

```
Markdown text -> tokenize() -> list[Token] -> render_pdf() -> PDF bytes
                     |
              Block-level split (paragraphs, headers)
              then inline tokenization (bold, italic)
```

**Key modules and their roles:**

- `tokenizer.py` — Line-by-line tokenization: headers terminate at single newline, non-header lines accumulate into `Paragraph` blocks separated by blank lines
- `inline_tokenizer.py` — Handles backtick code spans first (literal content, no nested parsing), then recursively parses `*`, `**`, `***` delimiters for inline styles. Handles nesting
- `tokens.py` — Immutable data structures: `Header`, `Paragraph`, `InlineText`, `Bold`, `Italic`, `Code`. Union type `Token = Header | Paragraph`
- `renderer.py` — Converts token list to PDF bytes using fpdf2. Uses `match` statements for token dispatch
- `styles.py` — Three named presets (`generic`, `times`, `regard`) with shorthand aliases (`g`, `t`, `r`)
- `style_base.py` — Frozen `Style` dataclass. All dimensions stored in millimeters; `pt_to_mm()` / `mm_to_pt()` for conversion at boundaries
- `cli.py` — argparse-based CLI. Orchestrates: read file -> tokenize -> render -> write PDF

## Code Conventions

- **Type hints** — functions use type annotations (some entry points like `main()` may omit return types)
- **Frozen dataclasses** for immutable data (`Token` types, `Style`)
- **Match statements** for token dispatch in the renderer
- **Private functions** prefixed with `_` (e.g., `_render_header`, `_find_closing`)
- **PascalCase** for classes, **snake_case** for functions and variables
- **Pathlib** for all file paths (`Path` instead of string paths)
- **UTF-8 encoding** always specified explicitly: `read_text(encoding="utf-8")`
- **Millimeters internally** — points only at PDF generation boundaries
- **Minimal dependencies** — only `fpdf2` in production; keep it lean
- **Ruff** for linting and formatting — configured in `pyproject.toml`. Run `uv run ruff check .` and `uv run ruff format .` before committing
- **Preserve original names and intent** — never silently rename variables, extract unnecessary temporaries, or reword precise text to satisfy linting rules. If code is correct and clear, configure the tooling around it, not the other way around

## Documentation Quality

Documentation (README, CHANGELOG, code comments) priorities in order: **precision**, **clarity**, **brevity**. Provide the correct information in the right place — never incorrect, misplaced, or filler content. Every word should earn its place. When modifying documentation, the result must be higher quality than what it started with.

## Testing

Development follows **test-driven development (TDD)**.

- Tests live in `akidocs-core/tests/`
- CLI tests invoke the module via `subprocess.run(["uv", "run", "python", "-m", "akidocs_core", ...])`
- `AKIDOCS_TEST_MODE` environment variable prevents file-open operations during tests
- Uses `tmp_path` fixture for temporary file I/O
- Uses `@pytest.mark.parametrize` for style/flag matrix testing
- Uses `unittest.mock.patch` for platform-specific mocking in opener tests

**Run tests before committing any change:**
```bash
cd akidocs-core && uv sync && uv run python -m pytest
```

## CI

GitHub Actions workflow (`.github/workflows/test.yml`):
- Triggers on push to `main` and pull requests to `main`
- Runs on `ubuntu-latest`
- **`lint` job**: checkout -> install uv -> `uv sync` -> `uv run ruff check .` -> `uv run ruff format --check .`
- **`test` job**: checkout -> install uv -> `uv sync` -> `uv run pytest`

## GitHub Workflow

### Issue and PR Naming

All issues and PRs use a conventional prefix in their title (from `DEVELOPMENT.md`):
- `feat:` — new functionality
- `fix:` — bug fixes
- `refactor:` — internal changes, no behavior change
- `test:` — test coverage
- `docs:` — documentation
- `chore:` — other tasks
- `epic:` — larger goals (issues only)

### Issue Structure

- **Epic issues** are high-level tracking issues prefixed with `epic:`. They contain a description of the scope and use GitHub sub-issues to track child work items. Examples: `epic: ATX header compliance`, `epic: Code span support`, `epic: List support`.
- **Regular issues** describe a single unit of work (a feature, bug fix, test, etc.). They typically include context, implementation considerations, and acceptance criteria. When completed, they are closed by a linked PR.

### PR Workflow

1. **One issue, one PR** — each PR addresses a specific issue and links to it (e.g., "Closes #7")
2. **PR titles match the issue prefix** — a `feat:` issue gets a `feat:` PR
3. **Fork-based contributions** — work is done on a fork and PRs target `main` on the upstream repo
4. **TDD approach** — tests are written first or alongside the implementation; pytest must pass before merge. **Commit at each Red-Green-Refactor step**: commit the failing test (Red), commit the passing implementation (Green), commit the cleanup (Refactor). Each step is a separate commit. This is not optional — frequent small commits document the process and are squash merged anyway
5. **README.md and CHANGELOG.md updates** — PRs that add features, change user-facing behavior, or modify dev tooling affecting human developers should update README.md and CHANGELOG.md as appropriate. README.md reflects current capabilities; CHANGELOG.md tracks what changed per version
6. **CI gate** — the GitHub Actions test workflow runs on all PRs to `main` and must pass
7. **Keep PR up to date** — when changes are made after the PR is created, update the title and description to accurately reflect the current state of the PR. The PR title and top-level bullet summary are used as the squash merge commit message — they must always be current
8. **Don't amend commits** — PRs are squash merged, so individual commits don't need to be clean. Use separate commits to document the process, including Red-Green-Refactor steps

### PR Description Format

PR descriptions start with a precise bullet-point summary. The PR title and this summary become the squash merge commit message — nothing below it is included. Each bullet describes a specific change, starting with an action verb. Link the closing issue as the first bullet when applicable.

Example:
```
* Closes #43, simplify `DEVELOPMENT.md` by removing irrelevant content
* Add section on valid Issue and PR prefixes in `DEVELOPMENT.md`
* Remove feature branch focused content from `DEVELOPMENT.md`
* Remove reference to `DEVELOPMENT.md` from `README.md`
* Document simplification in `CHANGELOG.md`
```

### Branch Strategy

- `main` is the primary branch; all PRs merge into `main`
- Feature work happens on separate branches or forks
- After a PR merges, fork holders sync by resetting their `main` to upstream (see `DEVELOPMENT.md`)

## Releases

### Version Scheme

Versions follow the pattern `X.Y.Z` with PEP 440 suffixes:
- **During development**: `0.3.0.dev0` in `pyproject.toml`, `0.3.0.dev0 - UNDER DEVELOPMENT` in CHANGELOG header
- **At release**: `0.3.0a0` in `pyproject.toml`, `v0.3.0-alpha / 0.3.0a0 - YYYY-MM-DD` in CHANGELOG header

### CHANGELOG Conventions

- The current dev version section sits at the top of the version list in `CHANGELOG.md`
- Entries are roughly chronological — earlier changes first, later additions (workflow changes, tooling, etc.) toward the end
- `#### What's New` for user-facing changes, `#### What's New Internally` for internal changes
- Entries should integrate brief inline examples where they add precision (e.g., `` `code` `` renders in bold monospace)
- The last line in "What's New Internally" is `Total number of tests: ADD BEFORE RELEASE` during development, replaced with the actual count at release time

### Release Checklist

1. Update CHANGELOG.md:
   - Replace dev header (`0.3.0.dev0 - UNDER DEVELOPMENT`) with release header (`v0.3.0-alpha / 0.3.0a0 - YYYY-MM-DD`)
   - Fill in the test count placeholder with the actual number from `uv run pytest`
   - Verify entries are complete and in chronological order
2. Bump version in `pyproject.toml` (e.g., `0.3.0.dev0` -> `0.3.0a0`)
3. Run `uv sync` to update `uv.lock`
4. Run full test suite: `cd akidocs-core && uv run python -m pytest`
5. Commit: `chore: Prepare vX.Y.Z-alpha release`
6. After merge, create a GitHub Release with the `vX.Y.Z-alpha` tag

### After Release

To start the next dev cycle, bump the version to the next dev marker (e.g., `0.4.0.dev0`) and add a new CHANGELOG section:

```markdown
### Akidocs - 0.4.0.dev0 - UNDER DEVELOPMENT
#### What's New
-

#### What's New Internally
-
- Total number of tests: ADD BEFORE RELEASE
```

## Key Design Decisions

1. **Delimiter priority** in inline tokenizer: longest match first (`***` > `**` > `*`). The `DELIMITERS` list order matters.
2. **Recursive inline parsing**: `tokenize_inline()` calls itself for nested styled content, carrying `inherited_styles` through recursion.
3. **Style system**: Frozen `Style` dataclass ensures styles are never accidentally mutated. All three presets are defined in `styles.py` with a lookup dict including shorthand aliases.
4. **Error handling**: CLI uses `sys.exit(1)` for user-facing errors. Internal functions return `None` or `-1` for "not found" cases rather than raising exceptions.
5. **File overwrite safety**: CLI supports `--force`, `--non-interactive`, and interactive prompt for existing output files.
6. **Code spans are literal**: Backtick-delimited content is not parsed for nested styles. Handled before the DELIMITERS system in `tokenize_inline()`.
7. **Code spans escape enclosing styles**: At render time, `code_font_style` is used as the complete font style for code spans, ignoring delimiter-influenced Bold/Italic. This follows the convention that code is visually independent from its surrounding context.
