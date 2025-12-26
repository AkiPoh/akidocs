# Akidocs
Akidocs converts Markdown files to PDF. Part of a larger personal project with the goal of exploring documentation tooling. Currently very minimal.

⚠️ **Alpha software** ⚠️ - This is currently a learning project in early development. Expect frequent breaking changes, major missing features, and non-comprehensive documentation.

Currently functional on **Windows 11 via PowerShell,** all instructions for PowerShell if not otherwise specified. Other platforms remain untested.

## Current Features
Takes in a Markdown file, parses it, and outputs it as a PDF

- Headers (levels 1-6)
- Paragraphs
- Inline formatting
  - `*Italics*` is *Italics*
- Usable as a CLI tool (`aki`)
  - `-h` or `--help` for help information
  - `-v` or `--version` for version information
  - `-O` or `--open` to open the PDF after creation

## Prerequisites
**Requires uv**, if not installed follow https://docs.astral.sh/uv/getting-started/installation/

## Install
Akidocs is available from GitHub (https://github.com/AkiPoh/akidocs), with releases available from GitHub Releases (https://github.com/AkiPoh/akidocs/releases).

### Install from GitHub Releases (Preferred)
Go to GitHub Releases (https://github.com/AkiPoh/akidocs/releases) and follow the instructions for the most recent release.

## Usage
```powershell
# Usage after installed globally
# Convert Markdown to PDF
aki input.md output.pdf

# Convert and open in default application
aki input.md output.pdf --open  # or:
aki input.md output.pdf -O

# Show help
aki --help  # or:
aki -h

# Show version
aki --version  # or:
aki -v
```

## Development
```powershell
# Move to correct directory from repository root
cd ./akidocs-core
# Sync dependencies from lockfile
uv sync
# Install package in editable mode
uv pip install -e .
# Run tests
uv run python -m pytest
# Output test PDF and open it
uv run python -m akidocs_core test.md output.pdf -O
```

**Installing globally and testing build**
```powershell
cd ./akidocs-core
# Install Akidocs globally
uv tool install .
cd ..
aki test.md output.pdf -O
```
