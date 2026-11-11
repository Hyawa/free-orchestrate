# Briefing template

Copy this template for each worker. Workers do not see the lead conversation,
so the briefing must be self-contained.

## Briefing: <unit name>

**Goal:** <one sentence, in terms of a finished outcome>

**Context:** <what the worker needs to know; link files with `@path`>

**Files in scope:** <list; keep it tight>

**Task:** <concrete steps, in order>

**Acceptance criteria:**
- <criterion 1, observable>
- <criterion 2, observable>

**Output format:**
- Summary: <short, with `file:line` pointers>
- Diff: <what changed, if writing>
- Checks: <commands run and their results>
- Risks: <anything uncertain, plus what you did not verify>

**Constraints:**
- Do not edit files outside the scope.
- Do not use paid models and do not launch subagents.
- Keep the response under <N> lines; put long output in a file and link it.
- If blocked, report the blocker instead of guessing.

## Example: a scout unit

```text
Goal: map how authentication is wired before we add SSO.

Context: the API lives in services/api. Sessions are created in
services/api/src/auth/session.ts. We are adding an OIDC provider.

Files in scope: services/api/src/auth/**, services/api/src/routes/**,
services/api/package.json

Task:
1. Find where a session is created, validated, and destroyed.
2. Find every place that reads the current user.
3. Note where a provider abstraction would need to hook in.

Acceptance criteria:
- Every claim has a file:line pointer.
- No files are edited.

Output format:
- Summary: at most 20 bullet points.
- Diff: none.
- Checks: none.
- Risks: anything you could not find.
```

## Example: a coder unit

```text
Goal: add an `expiresAt` column to the sessions table and enforce it on read.

Context: @services/api/src/auth/session.ts validates sessions.
@migrations/ holds Kysely migrations. Postgres 16.

Files in scope: services/api/src/auth/session.ts,
migrations/2026xxxx_add_session_expiry.ts, services/api/src/auth/session.test.ts

Task:
1. Add the migration.
2. Set expiresAt on creation (30 days).
3. Reject expired sessions in the read path.
4. Add tests for both valid and expired sessions.

Acceptance criteria:
- `pnpm test auth` passes.
- No behavior change for non-expired sessions.

Output format:
- Summary: 5 lines.
- Diff: the changed files.
- Checks: the exact command and its result.
- Risks: migration rollback concerns.
```
