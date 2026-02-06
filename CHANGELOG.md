# Changelog
See [README.md](./README.md) for current version's documentation.

Notable changes and release notes will be documented in this file. GitHub Releases are the primary reference for changes and version information. This file is a secondary reference for convenience, that may or may not be up to date.

## Early development

***Notes***

Early development release. Not yet usable for serious work. ⚠️

Should work across platforms including Windows (PowerShell), Ubuntu, and macOS. Developed and primarily tested on Windows 11 via PowerShell. Instructions default to PowerShell if not otherwise specified.

See https://github.com/AkiPoh/akidocs/tree/v0.2.1-alpha for specific version's documentation. Replace version tag with right one.

Full Changelog: [https://github.com/AkiPoh/akidocs/compare/v0.2.0-alpha...v0.2.1-alpha](https://github.com/AkiPoh/akidocs/compare/v0.2.0-alpha...v0.2.1-alpha). Replace version tags with desired ones.

***Install***

Requires uv, if not installed follow https://docs.astral.sh/uv/getting-started/installation/

Then in PowerShell:
```powershell
# Replace version tag "v0.2.1-alpha" with desired version tag
uv tool install git+https://github.com/AkiPoh/akidocs.git@v0.2.1-alpha#subdirectory=akidocs-core
```

### Akidocs - v0.3.0-alpha / 0.3.0a0 - 2026-02-06
#### What's New
- Tab character now accepted as separator after `#` in ATX headers (`#\tTitle` works)
- Trim trailing `#` characters sequence from ATX header (`## Header ##` works)
- Officially adopted Apache 2.0 as project license
- Switched to Issue and PR-based development workflow — all work tracked via GitHub Issues with linked PRs
- Now leveraging Claude Code for development
- Simplify `DEVELOPMENT.md` and update it with section on syncing fork after PR merge
- Added `CLAUDE.md` guide for AI assistants covering project structure, conventions, and workflows

#### What's New Internally
- Refactored `inline_tokenizer.py` for readability
- Total number of tests: 66

### Akidocs - v0.2.1-alpha / 0.2.1a0 - 2025-12-28
#### What's New
- Adopted feature branch workflow with squash merging to main, ensuring that the main branch stays cleaner and always functional
- Added DEVELOPMENT.md documenting the new Git/GitHub workflow
- Added branch protection to main branch

#### What's New Internally
- Renamed `base_font_style` to `paragraph_base_font_style` and added `header_base_font_style` for independent control
- Total number of tests: 60

### Akidocs - v0.2.0-alpha / 0.2.0a0 - 2025-12-27
#### What's New
- Trying to overwrite a file that already exists now prompts for confirmation
- New CLI flags: 
  - `-n` or `--non-interactive` to error instead of prompting when trying to overwrite
  - `-f` or `--force` to overwrite output without prompting or erroring
  - `-s` or `--style` to select document style, for example `--style generic`
    - `generic` (g) — clean sans-serif, default
    - `times` (t) — balanced serif style
    - `regard` (r) — monospace, bold, enormous margins
- CLI now shows conversion info on generation, for example: `From input.md (Helvetica, generic) to output.pdf`
- Added CHANGELOG.md for tracking version history in repository
- Added Technical Overview to README.md

#### What's New Internally
- Considerable refactors throughout codebase
- Styles now have their own module `styles.py` with dataclass from `style_base.py`
- Styles now have configuration for edge margins and base font style
- Standardized internal measurements to millimeters, converting to points only at boundaries where relevant
- Total number of tests: 60

### Akidocs - v0.1.0-alpha / 0.1.0a0 - 2025-12-26
#### What's New
- Inline text formatting
  - `*Italics*` is *Italics*
  - `**Bold**` is **Bold**
  - `***Bold and Italic***` is ***Bold and Italic***
  - Nested styles, for example `**bold with *italic* inside**` is **bold with *italic* inside** works correctly
- New CLI flags:
  - `-h` or `--help` for help information
  - `-v` or `--version` for version information
  - `-o` or `--open` to open the PDF after creation
  
#### What's New Internally
- New inline tokenizer system for parsing formatted text
- Included significant changes and refactors throughout codebase, especially as many before mentioned changes were considerable

### Akidocs - v0.0.1-alpha / 0.0.1a0 - 2025-12-25
#### What's New
- Better handling of Markdown headline edge cases (7+ hashes, missing space after #, etc.)
- Windows line endings (CRLF) now parse correctly
- Removed installing from source from suggested installation methods in README.md, instead installing from source is now under development section

#### What's New Internally
- General internal improvements and refactoring
- Extracted style constants to the top of renderer
- Now uses points for all styling constants instead of millimeters
- Refactored renderer and tokenizer internals

### Akidocs - v0.0.0-alpha / 0.0.0a0 - 2025-12-25

#### Features
- Takes in a Markdown file, parses it, and outputs it as a PDF
- Headers (levels 1-6)
- Paragraphs
- Usable as a CLI tool (`aki`)

Full changelog for this version: https://github.com/AkiPoh/akidocs/commits/v0.0.0-alpha
