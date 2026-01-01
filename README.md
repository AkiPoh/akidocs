# Akidocs
Akidocs converts Markdown files to PDF. Part of a larger personal project with the goal of exploring documentation tooling. Currently very minimal.

⚠️ **Alpha software** ⚠️ - This is currently a learning project in early development. Expect frequent breaking changes, major missing features, and non-comprehensive documentation.

Currently functional on **Windows 11 via PowerShell,** all instructions for PowerShell if not otherwise specified. Other platforms remain untested.

## Current Features
Takes in a Markdown file, parses it, and outputs it as a PDF

- Headers (levels 1-6)
  - Trailing `#` characters in ATX headers (`## Header ##`)
- Paragraphs
- Inline formatting
  - `*Italics*` is *Italics*
  - `**Bold**` is **Bold**
  - `***Bold and Italic***` is ***Bold and Italic***
  - Nested styles: for example `**bold with *italic* inside**` is **bold with *italic* inside** works correctly
- Usable as a CLI tool (`aki`)
  - `-h` or `--help` for help information
  - `-v` or `--version` for version information
  - `-o` or `--open` to open the PDF after creation
  - `-s` or `--style` to select document style, for example `--style generic`
    - `generic` (g) — clean sans-serif, default
    - `times` (t) — balanced serif style
    - `regard` (r) — monospace, bold, enormous margins
  - `-n` or `--non-interactive` to error instead of prompting when output file exists
  - `-f` or `--force` to overwrite output file without prompting

## Technical Overview
**Stack**
- Python 3.14
- uv for package and dependency management
- fpdf2 for PDF generation
- pytest for testing
- akidocs-core (this package)

**Understanding the codebase**

The entry point lives in [cli.py](./akidocs-core/src/akidocs_core/cli.py), and that's a good place to get started with understanding this project. Here's the core flow as a snippet from there:
```python
text = input_path.read_text(encoding="utf-8")
tokens = tokenize(text)
pdf_bytes = render_pdf(tokens, style)
output_path.write_bytes(pdf_bytes)
```

The internal flow goes something like this: read the markdown, tokenize it into blocks (like headings and paragraphs), then tokenize the raw text within those blocks to inline tokens (like normal text, bold and italic), then render it with the selected style to PDF with fpdf2, and finally write to disk.

Development is test-driven development (TDD) based - see [tests/](./akidocs-core/tests) for how features are specified and verified.

Git/GitHub workflow for this project is documented in [DEVELOPMENT.md](./DEVELOPMENT.md).

Version history is tracked in [GitHub Releases](https://github.com/AkiPoh/akidocs/releases) (primary) and [CHANGELOG.md](./CHANGELOG.md) (secondary).

## Prerequisites
**Requires uv**, if not installed follow https://docs.astral.sh/uv/getting-started/installation/. In the following steps uv will automatically install the correct version of Python; you do not need to install Python manually.

## Install
Akidocs is available from GitHub (https://github.com/AkiPoh/akidocs), with releases available from GitHub Releases (https://github.com/AkiPoh/akidocs/releases).

### Install from GitHub Releases (Preferred)
Go to GitHub Releases (https://github.com/AkiPoh/akidocs/releases) and follow the instructions for the most recent release.

## Usage
```powershell
# Show help
aki --help  # or:
aki -h

# Show version
aki --version  # or:
aki -v

# Usage after installed globally
# Convert Markdown to PDF
aki input.md output.pdf

# Convert and open in default application
# with default style (generic)
aki input.md output.pdf --open  # or:
aki input.md output.pdf -o

# Convert and open in default application
# with chosen style, available: generic / g,
# times / t, regard / r
aki input.md output.pdf --style regard  # or:
aki input.md output.pdf --style r  # or:
aki input.md output.pdf -s regard  #or:
aki input.md output.pdf -s r

# If output.pdf exists, you'll be prompted:
#   output.pdf already exists. Overwrite? [y/N]
# Enter y to proceed, anything else to abort

# Skip the prompt in scripts
aki input.md output.pdf --non-interactive  # errors if exists

# Overwrites silently without prompting or erroring
aki input.md output.pdf --force
```

## Development
```powershell
# Move to correct directory from repository root
cd ./akidocs-core
# Sync dependencies from lockfile
uv sync
# Install package in editable mode
uv pip install -e .
# Run tests (-v for showing individual test results)
uv run python -m pytest -v
# Output test PDF and open it
uv run python -m akidocs_core test.md output.pdf -o
```

**Installing globally and testing build**
```powershell
cd ./akidocs-core
# Install Akidocs globally
uv tool install .
cd ..
aki test.md output.pdf -o
```
