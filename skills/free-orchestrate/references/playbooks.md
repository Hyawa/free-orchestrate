# Playbooks

Playbooks are reusable orchestration patterns. Pick one that fits the task,
then adapt the worker models to what is available in `/models`.

## scout-then-build

Use when: unfamiliar code, much to read, little to write.

1. **Scout** (read-only, `free-scout`): map the relevant areas. Return a short
   summary with `file:line` pointers, under ~1.5K tokens.
2. **Plan** (lead): turn the summaries into one concrete change plan.
3. **Build** (`free-coder`): implement the plan. Return changed files, checks
   run, failures, risks.
4. **Fix** (`free-coder`, only if checks fail): fix from the failure excerpt
   and the diff.
5. **Review** (`free-reviewer`): review the final diff.

## plan-big-execute-small

Use when: up to ~10 independent reads, audits, or checks.

1. **Decompose** (lead): split into independent units.
2. **Execute** (free workers, parallel): one unit each.
3. **Synthesize** (lead): merge results, resolve conflicts.
4. **Verify** (`free-reviewer`): run checks on the merged result.

## audit-at-scale

Use when: dozens or hundreds of similar items.

1. **Slice** (lead): split items into batches.
2. **Audit** (`free-scout` or `free-longctx`, parallel): one batch each.
3. **Normalize** (lead): merge findings, dedupe.
4. **Report** (lead): severity-ordered findings with file:line.

## parallel-worktrees

Use when: independent modules with disjoint files.

1. **Split** (lead): one worktree per module.
2. **Build** (`free-coder`, one per worktree, parallel): implement.
3. **Integrate** (lead): merge worktrees, resolve conflicts.
4. **Verify** (`free-reviewer`): run the full test suite.

OpenCode has native worktrees. Prefer them over manual branches.

## review-gate

Use when: a finished diff before merge.

1. **Review** (`free-reviewer`, read-only): correctness, security, missing tests.
2. **Fix** (`free-coder`, only if issues): address findings.
3. **Re-review** (`free-reviewer`): confirm.

## best-of-n

Use when: a hard, high-stakes fix worth several attempts.

1. **Attempt** (`free-coder`, N parallel): independent attempts.
2. **Score** (`free-reviewer`): score each attempt against the acceptance criteria.
3. **Pick** (lead): choose the best, merge, verify.
