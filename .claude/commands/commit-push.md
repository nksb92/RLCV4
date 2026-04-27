Analyse all uncommitted changes and commit them in logical groups, then push. Follow these steps exactly:

## Step 1 — Inventory

Run `git status` and `git diff HEAD` to see every changed and untracked file. Read the diffs carefully.

## Step 2 — Plan logical groups

Partition the changes into logical commit groups. Each group must have a single, coherent purpose (e.g. "typography changes", "new feature X", "refactor Y"). A file may only belong to one group. Write out the plan — list each group with its files and a draft commit message — before doing anything else.

## Step 3 — Commit each group (one at a time)

For each group, in order:

1. Present the user with:
   - The list of files in this group
   - The exact `git add` command you will run
   - The exact commit message you will use
2. **Stop and wait for the user to confirm** with "yes", "ok", "go", or similar before proceeding. Do not commit until confirmed.
3. Once confirmed: stage the files (`git add <specific files>`), then commit with the agreed message, ending with:
   ```
   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
   ```
4. Show the result of `git status` after the commit so the user can see remaining changes.

## Step 4 — Branch check before push

Before pushing, check the current branch with `git branch --show-current`.

If the current branch is `main` or `master`:
1. Propose a short, descriptive branch name based on the commits just made.
2. Present the exact `git checkout -b <branch>` command you will run.
3. **Stop and wait for the user to confirm** the branch name (they may suggest a different name). Do not create the branch until confirmed.
4. Once confirmed: create the branch with `git checkout -b <branch>`.

If the current branch is already a feature branch, state its name and continue.

## Step 5 — Push

Show the full list of commits about to be pushed (`git log origin/HEAD..HEAD --oneline`) and the target branch. Ask the user to confirm the push. Once confirmed, run `git push -u origin <branch>`.

## Rules

- Never batch multiple groups into one commit.
- Never use `git add -A` or `git add .` — always name specific files.
- Never amend existing commits.
- Never skip hooks (`--no-verify`).
- Never push directly to `main` or `master`.
- If `git status` shows nothing to commit at any point, say so and stop.
