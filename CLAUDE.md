# CLAUDE.md — AI Assistant Guide for DahshIn-research

This file provides context and conventions for AI assistants (Claude, Copilot, etc.) working in this repository.

---

## Repository Overview

**Name:** DahshIn-research
**Remote:** `xeverusj/DahshIn-research`
**Purpose:** Research repository (early stage — structure and stack are not yet defined)

### Current State (as of 2026-02-27)

This is a freshly initialized repository. Currently it contains only:

```
/
├── README.md    # Minimal project heading
└── CLAUDE.md   # This file
```

No source code, build tooling, CI/CD, tests, or application framework has been introduced yet. When the project grows, update this file to reflect the new structure.

---

## Git Workflow

### Branch Naming Convention

Feature branches created by Claude (AI-assisted sessions) follow this naming scheme:

```
claude/<session-slug>-<session-id>
```

Example: `claude/claude-md-mm49gy5m78siqs79-QZKIv`

**Rules:**
- Always develop on the designated `claude/` branch for a session.
- Never push directly to `master` without explicit permission.
- Branches must start with `claude/` and end with the matching session ID, or a push will fail with HTTP 403.

### Standard Git Operations

```bash
# Push to a feature branch (always use -u the first time)
git push -u origin claude/<session-slug>-<session-id>

# Fetch a specific branch
git fetch origin <branch-name>

# Pull a specific branch
git pull origin <branch-name>
```

**Retry policy for network failures:** retry up to 4 times with exponential backoff (2 s → 4 s → 8 s → 16 s).

### Commit Messages

Write short, imperative commit messages in the present tense:

```
Add initial project scaffold
Fix null-pointer error in parser
Update CLAUDE.md with new conventions
```

---

## Development Conventions (to be updated as the stack is chosen)

Because the technology stack has not yet been selected, this section contains general conventions. **Update it when concrete tooling is introduced.**

### File Organization

- Keep related files in clearly named directories (`src/`, `tests/`, `docs/`, etc.).
- Avoid committing generated or build artefacts; add them to `.gitignore` immediately.
- Do not commit secrets, credentials, or `.env` files.

### Code Style

- Prefer explicit over clever.
- Favour small, single-responsibility functions/modules.
- Do not add docstrings, comments, or type annotations to code you did not change.
- Do not introduce error handling for scenarios that cannot realistically occur.

### Testing

- Write tests alongside new code, not as an afterthought.
- All tests must pass before a branch is merged.
- Add the test command(s) to this file once a test framework is chosen.

### Documentation

- Keep `README.md` accurate and concise.
- Update this `CLAUDE.md` whenever the project structure, conventions, or tooling changes significantly.

---

## Guidance for AI Assistants

1. **Read before editing.** Always read a file before modifying it.
2. **Minimal changes.** Only change what is directly requested. Do not refactor surrounding code, add unsolicited comments, or clean up style.
3. **No speculative abstractions.** Do not create helpers, utilities, or abstractions for one-time operations.
4. **Security.** Do not introduce command injection, SQL injection, XSS, or other OWASP Top 10 vulnerabilities.
5. **Reversibility.** Prefer reversible actions. For irreversible or high-blast-radius actions (deleting branches, force-pushing, dropping data), confirm with the user first.
6. **Branch discipline.** All work must go to the branch specified for the session (see Git Workflow above).
7. **Commit and push when done.** After implementing a task, commit with a descriptive message and push to the feature branch.
8. **Update this file.** If you introduce new tooling, scripts, or conventions, add them here so future sessions have accurate context.

---

## Updating This File

When the project evolves, expand the relevant sections:

| Section | When to update |
|---|---|
| Repository Overview / Current State | When directories/files are added |
| Git Workflow | When branching strategy changes |
| Development Conventions | When a tech stack, linter, or formatter is chosen |
| Commands Reference | When build, test, or lint commands exist |

### Commands Reference (placeholder)

Once tooling is set up, document commands here, for example:

```bash
# Install dependencies
# <command here>

# Run tests
# <command here>

# Lint / format
# <command here>

# Build
# <command here>
```
