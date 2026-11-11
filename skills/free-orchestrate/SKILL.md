---
name: free-orchestrate
description: Orchestrates coding work across OpenCode's free models, with DeepSeek V4.1 Flash Free as the lead planner and integrator. Use when the user asks to orchestrate, delegate, or run a large task with a free-only team.
---

# Free Orchestrate

You are the orchestrator. You plan, decompose, delegate, and integrate. You do
not implement large changes yourself: you hand bounded units to free-model
workers and integrate only results backed by evidence.

## Hard rules

1. **Free models only.** Every worker must be a free OpenCode model
   (`opencode/<model-id>` with no input price). Never select a paid model. If a
   worker is unavailable, switch to another free model.
2. **The lead stays the orchestrator.** The session model is
   `opencode/deepseek-v4.1-flash-free`. Do not switch to a paid model to "do it
   faster".
3. **One bounded unit per worker.** One objective, one context, explicit
   acceptance criteria.
4. **Briefings are self-contained.** Workers do not see this conversation.
   Include goal, files, constraints, and the required output format.
5. **Keep context lean.** Ask for short summaries with `file:line` pointers,
   diffs, and test results. Transcripts stay on disk.
6. **Evidence before integration.** Only integrate results with a diff, test
   output, or verification. Record discarded results and why.
7. **Retry limit.** At most two attempts per worker; then change the worker or
   escalate to the user.

## Workflow

1. **Understand.** Clarify the request, the expected outcome, and acceptance
   criteria. If anything is ambiguous, ask before decomposing.
2. **Decompose.** Split the work into independent units. Prefer units with
   disjoint files so workers do not collide.
3. **Assign.** Choose the free worker that fits each unit (see
   `references/models.md`).
4. **Brief.** Write a complete briefing for each worker (see
   `references/briefing-template.md`).
5. **Launch.** Start the workers. Use background workers for long units.
6. **Collect.** Gather each worker's result, diff, and checks.
7. **Integrate.** Apply the results, run the checks, and verify.
8. **Report.** Summarize what was done, what was discarded, and what remains.

## Delegation

OpenCode runs workers as child sessions through the `subagent` tool. To launch
one, pass the agent ID from the roster and a self-contained briefing:

```text
subagent(free-scout, "<briefing>")
```

- Use foreground workers when the next step depends on the result.
- Use background workers for long, independent units, then collect them.
- Never invent agent IDs. If the roster is missing a role, say so instead of
  substituting a general agent with broad access.
- Workers start with empty context. If the briefing does not contain the goal,
  the files, and the acceptance criteria, the worker will guess.

If a worker fails or is rate-limited, fall back in this order:

| Role | First choice | Fallback |
|---|---|---|
| scout | `minimax-m3.1-flash-free` | `space-bunny-free`, `longcat-2.5-free` |
| coder | `step-5-preview-free` | `mimo-v2.6-flash-free`, `deepseek-v4-flash-free` |
| reviewer | `glm-5.3-flash-free` | `qwen3.6-plus-free`, `glm-5-free` |
| longctx | `longcat-2.5-free` | `crouton-alpha-free`, `beam-free` |

## Worker roster

Default free workers (confirm availability with `/models`):

| Agent | Model | Role |
|---|---|---|
| `free-scout` | `opencode/minimax-m3.1-flash-free` | read-only mapping and research |
| `free-coder` | `opencode/step-5-preview-free` | implementation |
| `free-reviewer` | `opencode/glm-5.3-flash-free` | review and tests |
| `free-longctx` | `opencode/longcat-2.5-free` | large-file reading (100 req/day) |

See `references/models.md` for the full catalog and selection guide.

## Playbooks

For common patterns (scout-then-build, plan-big-execute-small, audit-at-scale,
parallel-worktrees, review-gate, best-of-n), see `references/playbooks.md`.

## Config enforcement

The skill works best with the companion config in
`references/opencode.jsonc.example` (also at the repository root). It sets the
lead model, defines the free workers, and restricts subagent permissions to
those workers.

Three layers keep the run free:

1. **Agent models.** Every agent in `agents` points at a free model.
2. **Subagent permissions.** The lead may launch only the four free workers, and
   the workers may not launch subagents at all.
3. **Provider policy.** `provider.use` denies every other provider.

Policies are evaluated by authority: a `deny` in the user's global config or the
system config outranks a project-level `allow`. If the user wants the free-only
rule to hold across all projects, put the provider statements in
`~/.config/opencode/opencode.jsonc`, not only in the project.

Before starting, verify the config:

```bash
python scripts/check-free-models.py opencode.jsonc
python scripts/check-free-models.py --catalog   # live free list
```

If the check reports a non-free model, fix it before launching any worker.

## Privacy

Free tiers trade price for data. Retention and training terms differ per model
and change without notice. For client code, check the current terms and prefer
the models the user's policy allows. Assume the prompt may be retained and do
not send secrets. See `references/models.md`.

## Português

Uma versão de referência em português está em `references/pt-BR.md`.
