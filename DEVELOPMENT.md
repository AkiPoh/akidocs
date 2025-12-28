# Development
Guide for development approach and workflow. Intended for internal reference.

## Branch Model
Main is respected. It always works, always passes tests. All work happens on branches.

```bash
# Starting new work
git checkout main
# Remember to use correct prefix and name
git checkout -b feature/code-blocks

# When done and tests pass
git checkout main
git merge feature/code-blocks
git branch -d feature/code-blocks
```

## Branch Naming
Prefix by type, describe in a few words:

- `feature/` — new functionality (`feature/code-blocks`, `feature/list-support`)
- `fix/` — bug fixes (`fix/empty-paragraph-crash`)
- `refactor/` — internal changes (`refactor/extract-tokenizer`)
- `docs/` — documentation (`docs/development-guide`)

## Commits
On branches, commit freely. TDD "add failing test" / "make pass" granularity is good.

When merging to main, squash into one meaningful commit. The PR preserves granular history if needed later.

## Pull Requests
Open PR against main. Review the diff - this is the checkpoint. Squash and merge with a message describing what changed, not how.

Good: "Add code block support"
Not: "Add tests, implement parser, fix edge cases, update docs"

## Staying Current
When main changes, update your branch:

```bash
git checkout feature/code-blocks
git rebase main
```

Resolve conflicts once, continue.

## Multiple Branches
Having several branches in flight is normal. If you notice something unrelated while working:

```bash
git stash
git checkout main
git checkout -b fix/unrelated-thing
# fix, commit, push, merge
git checkout feature/original-work
git rebase main
git stash pop
```

## Tests
Always before merging:

```bash
cd ./akidocs-core
uv run python -m pytest -v
```

Main must pass. No exceptions.
