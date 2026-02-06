# CLAUDE.md

Guide for AI assistants working on the Akidocs codebase.

## Project Overview

Akidocs is a Markdown-to-PDF converter CLI tool written in Python. The main package lives in `akidocs-core/`. It is in alpha development (v0.3.0.dev0).

- **Language**: Python 3.14+
- **Package manager**: `uv`
- **Production dependency**: `fpdf2` (PDF generation)
- **Test framework**: `pytest`
- **License**: Apache 2.0

## Quick Reference

```bash
# All commands run from akidocs-core/
cd akidocs-core

# Install dependencies
uv sync

# Install package in editable mode (required before running tests)
uv pip install -e .

# Run tests
uv run pytest
uv run pytest -v          # verbose

# Run the CLI
uv run python -m akidocs_core input.md output.pdf
uv run python -m akidocs_core input.md output.pdf -o    # open after creation
uv run python -m akidocs_core input.md output.pdf -s times  # use "times" style
```

## Project Structure

```
akidocs/
├── akidocs-core/                  # Main Python package
│   ├── src/akidocs_core/          # Source code
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

- `tokenizer.py` — Splits text into blocks by double-newline, classifies each as `Header` or `Paragraph`
- `inline_tokenizer.py` — Recursively parses `*`, `**`, `***` delimiters for inline styles. Handles nesting
- `tokens.py` — Immutable data structures: `Header`, `Paragraph`, `InlineText`, `Bold`, `Italic`. Union type `Token = Header | Paragraph`
- `renderer.py` — Converts token list to PDF bytes using fpdf2. Uses `match` statements for token dispatch
- `styles.py` — Three named presets (`generic`, `times`, `regard`) with shorthand aliases (`g`, `t`, `r`)
- `style_base.py` — Frozen `Style` dataclass. All dimensions stored in millimeters; `pt_to_mm()` / `mm_to_pt()` for conversion at boundaries
- `cli.py` — argparse-based CLI. Orchestrates: read file -> tokenize -> render -> write PDF

## Code Conventions

- **Type hints everywhere** — all functions have type annotations
- **Frozen dataclasses** for immutable data (`Token` types, `Style`)
- **Match statements** for token dispatch in the renderer
- **Private functions** prefixed with `_` (e.g., `_render_header`, `_find_closing`)
- **PascalCase** for classes, **snake_case** for functions and variables
- **Pathlib** for all file paths (`Path` instead of string paths)
- **UTF-8 encoding** always specified explicitly: `read_text(encoding="utf-8")`
- **Millimeters internally** — points only at PDF generation boundaries
- **Minimal dependencies** — only `fpdf2` in production; keep it lean
- **No external linter/formatter config** — no mypy, ruff, black, or flake8 config files exist

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
cd akidocs-core && uv sync && uv pip install -e . && uv run pytest
```

## CI

GitHub Actions workflow (`.github/workflows/test.yml`):
- Triggers on push to `main` and pull requests to `main`
- Runs on `ubuntu-latest`
- Steps: checkout -> install uv -> `uv sync` -> `uv pip install -e .` -> `uv run pytest`

## PR and Issue Naming

Use these prefixes (from `DEVELOPMENT.md`):
- `feat:` — new functionality
- `fix:` — bug fixes
- `refactor:` — internal changes, no behavior change
- `test:` — test coverage
- `docs:` — documentation
- `chore:` — other tasks
- `epic:` — larger goals (issues only)

## Key Design Decisions

1. **Delimiter priority** in inline tokenizer: longest match first (`***` > `**` > `*`). The `DELIMITERS` list order matters.
2. **Recursive inline parsing**: `tokenize_inline()` calls itself for nested styled content, carrying `inherited_styles` through recursion.
3. **Style system**: Frozen `Style` dataclass ensures styles are never accidentally mutated. All three presets are defined in `styles.py` with a lookup dict including shorthand aliases.
4. **Error handling**: CLI uses `sys.exit(1)` for user-facing errors. Internal functions return `None` or `-1` for "not found" cases rather than raising exceptions.
5. **File overwrite safety**: CLI supports `--force`, `--non-interactive`, and interactive prompt for existing output files.
