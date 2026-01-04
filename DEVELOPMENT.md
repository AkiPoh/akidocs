# Development
Partial reference notes for development approach and workflow. Intended for internal reference.

⚠️ **Note** — This is a personal reference for the repository holder. Does not currently address other contributors or developers.

## Valid PR and Issue Prefixes
* `feat: ` — new functionality
* `fix: ` — bug fixes
* `refactor: ` — internal changes that do not affect behaviour
* `test: ` — additional test coverage
* `docs: ` — documentation
* `chore: ` — tasks not covered above
* `epic: ` — larger project goals and directions (only for issues)

## Syncing Fork After PR Merge
**Configure upstream for your fork (if you haven't already):**
```bash
# Add upstream, if you haven't already
git remote add upstream https://github.com/AkiPoh/akidocs.git
```

Please note that the following ***deletes all work*** currently in the fork that has not been merged to upstream.

**Fetch upstream changes, and reset main branch of fork, and push to GitHub:**
```bash
# Fetch upstream changes
git fetch upstream

# Reset your main branch to match upstream
git checkout main
git reset --hard upstream/main

# Push to your fork on GitHub (force needed due to history rewrite)
git push origin main --force
```
