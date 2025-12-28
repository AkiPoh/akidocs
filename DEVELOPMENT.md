# Development
Guide for development approach and workflow. Intended for internal reference.

⚠️ **Note** — This is a personal reference for the repository holder. Does not currently address other contributors or developers.

## Overview
Development follows a branch-based workflow:
- **Main** — the stable branch, always works, always passes tests
- **Feature branches** — where work happens, temporary, merged when complete
- **Pull requests (PRs)** — the checkpoint between branch and main, reviewed before merging

Work never happens directly on main. Each piece of work gets its own branch. When the work is done and tested, it merges to main through a PR and the branch is deleted.

## Branch Scope
One branch, one logical change. A feature, a fix, a refactor, a documentation update. If it can be described in a short phrase, it's one branch.

Examples of well-scoped branches:
- Add code block support
- Fix crash on empty paragraph
- Refactor tokenizer to extract functions
- Add development guide

If working on something and noticing an unrelated issue, that's a separate branch.

## Commits
Branches contain the working history — granular commits from the development process. TDD commits like "add failing test" then "make pass" belong here.

Main contains the clean history — one squashed commit per merged branch. The PR preserves the granular history if ever needed.

Commit messages start with an imperative verb: Add, Fix, Refactor, Remove, Update. Not "Added" or "Adding."

## Workflow

### Starting Work
```bash
# Switch to main
git checkout main
# Create a new branch and switch to it
git checkout -b feature/your-feature-name
```

Branch naming — prefix by type, describe briefly:
- `feature/` — new functionality (`feature/code-blocks`)
- `fix/` — bug fixes (`fix/empty-paragraph-crash`)
- `refactor/` — internal changes (`refactor/extract-tokenizer`)
- `docs/` — documentation (`docs/development-guide`)
- `chore/` — tasks not covered above (`chore/bump-0.2.1.dev0`)

### Working on a Branch
```bash
# Stage all changes
git add .
# Commit with a message
git commit -m "Add failing test for feature"
```

Commit freely during development. This history stays in the branch.

### Pushing and Opening a PR
```bash
# Push branch to GitHub, -u sets up tracking for future pushes
git push -u origin feature/your-feature-name
```

On GitHub, open a PR from your branch to main. The PR description should summarize what the branch accomplishes — this becomes the squash commit message.

### Reviewing and Merging
Review the diff in the GitHub PR view. This shows exactly what will reach main.

Before merging, tests must pass locally:
```bash
cd ./akidocs-core
uv run python -m pytest -v
```

Main must pass before squash merging.

On GitHub, select **Squash and merge**. The commit message should:
- Start with an imperative verb
- Describe what changed, not how
- Be semi-comprehensive for larger changes

Good: "Add style system with generic, times, and regard options"
Not: "Add tests, implement parser, fix edge cases, update docs"

### Cleaning Up
After merging, GitHub can auto-delete the branch (enable in repository settings). Locally:
```bash
# Switch to main
git checkout main
# Get the merged changes from GitHub
git pull
# Delete the local branch
git branch -d feature/your-feature-name
```

## Keeping Branches Current
When main has changed from other merged work, update your branch before merging:
```bash
# Switch to your branch
git checkout feature/your-feature-name
# Replay your commits on top of current main
git rebase main
```

If there are conflicts, Git will pause and show which files conflict. Edit the files to resolve, then:
```bash
# Stage resolved files
git add .
# Continue the rebase
git rebase --continue
```

## Multiple Branches
Multiple branches in flight is normal. If something unrelated comes up while working:
```bash
# Store uncommitted changes temporarily
git stash
# Switch to main
git checkout main
# Create branch for the other thing
git checkout -b fix/the-other-thing
```

Work on the fix, push, open PR, merge. Then return:
```bash
# Switch back to original branch
git checkout feature/original-work
# Get any changes from main
git rebase main
# Restore uncommitted changes
git stash pop
```
