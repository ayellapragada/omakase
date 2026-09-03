---
name: omakase
description: Use when a requested change to an actual code project is intended to land, especially features, fixes, refactors, tickets, pull requests, CI follow-up, or review follow-up; also use when invoked explicitly as `$omakase`. Do not use for one-off scripts, read-only explanation or review, or diagnosis-only debugging.
---

# Omakase

Treat Codex as the application and coding agent. Coordinate the project-delivery lifecycle around it without creating a second agent harness, issue tracker, or workflow engine.

## Hybrid trigger

Use this skill implicitly when the user asks for a change to an actual code project that is intended to land. Strong signals include:

- a GitHub issue, Shortcut story, or pull request;
- a feature, bug fix, refactor, migration, or repository change;
- a request to open a PR, follow CI, address review, merge, or take work across the finish line;
- explicit invocation with `$omakase`.

Do not trigger for:

- a small one-off or throwaway script outside a project-delivery workflow;
- read-only explanation, exploration, or code review;
- diagnosis or debugging when the user did not ask for a fix;
- ordinary file manipulation that is not intended to land in a repository;
- monitoring unrelated to coding delivery.

If the boundary is ambiguous, do not silently expand a small request into the full lifecycle. Ask only if the distinction materially affects what will be changed or published.

When activating, say briefly that Omakase is being used because the request is project work intended to land.

## Compose existing capabilities

Omakase is the conductor. Do not restate or weaken the detailed workflows owned by other capabilities.

- Use Superpowers for brainstorming, planning, git worktrees, TDD, systematic debugging, code-review discipline, verification, and branch finishing when their trigger conditions apply.
- Use the GitHub plugin for GitHub issues, pull requests, review threads, checks, and Actions evidence when available.
- For issue or internal-service context, use repository-approved integrations according to the active `AGENTS.md` instructions. If a required integration is unavailable, report that limitation rather than searching for an undocumented private CLI.
- Use Codex scheduled follow-ups for delayed CI, review, and merge checks.
- Follow applicable `AGENTS.md`, repository documentation, pull-request templates, and user instructions as authoritative project policy.

The separately installed `gh-fix-ci` skill can be used when the user invokes it or when its approval-oriented workflow is appropriate. Do not make it a mandatory Omakase dependency.

## Review intensity and model routing

### Lean review by default

Keep ordinary delivery in one implementation context, with independent review at the point where it has the most leverage:

1. Implement directly in the main agent, following the applicable design, TDD, debugging, and verification disciplines.
2. Run focused validation while developing and the applicable full validation before publication.
3. For every project change intended to land, request one independent review of the completed diff. Fix valid material findings and rerun affected validation. Request at most one scoped re-review, and only when material findings required fixes.

Do not invoke `superpowers:subagent-driven-development` merely because a plan can be split into tasks. Use its implementer-per-task and reviewer-per-task cycle only when the user requests an exhaustive workflow, repository policy requires it, or the change's scale and risk justify the additional model consumption. Examples include security-sensitive behavior, data migrations, subtle concurrency, or several genuinely independent implementation domains.

For every subagent dispatch, set both the model and reasoning effort explicitly. Use the cheapest capable tier for mechanical work with complete requirements and a balanced mid-tier for implementation from prose or ordinary review. Reserve the most capable tier for architecture, security, concurrency, difficult debugging, or a consequential final review. Never allow an omitted routing choice to inherit an expensive main-session default accidentally.

## Intake

Before changing files:

1. Resolve the task source and definition of done.
2. Resolve the target repository. For a multi-repository scope, inspect only enough repositories to identify the relevant set.
3. Read applicable instructions and resolve the personal project profile described in [references/project-guidance.md](references/project-guidance.md).
4. Inspect git status and preserve unrelated user changes.
5. Ask a question only when the answer is genuinely blocking or would materially change the result.

### Personal project profile

Each repository may have one machine-local `.omakase.local.yml` in its primary checkout. It is personal operational memory, not repository policy, and must be globally ignored by Git. Linked worktrees share that profile; do not copy it into each worktree.

Resolve its path from any checkout with:

```bash
python3 scripts/profile_path.py --repo <checkout-or-worktree>
```

Run that script from this skill's directory, or invoke it by its absolute installed path. Then:

- If the profile exists, read it after `AGENTS.md` and repository instructions. Higher-priority instructions always win.
- If it is absent, inspect the repository and generate a minimal profile from concrete evidence. Start with `assets/omakase.local.example.yml`; omit unknown or unused fields.
- Prefer established repository entry points such as `bin/setup`, `script/bootstrap`, declared package scripts, or documented Make targets. Record required setup as ordered `bootstrap.steps`, with each step selecting its own `runtime` and `run` command. These may be run without a redundant confirmation when they are safe and within the requested task.
- Ask before inventing novel shell setup, obtaining secrets, changing infrastructure, weakening checks, or performing destructive operations. Store secret file paths or prerequisite names only, never secret values.
- Tell the user when a profile is first generated or materially changed, but do not require approval for a safe evidence-backed initial profile.

Treat the profile as living memory. When worktree setup exposes a problem, diagnose it first. Update the profile only when the fix is durable and reproducible across future worktrees, rerun the affected setup or validation, and retain the change only after it works. Do not encode transient outages, sandbox failures, or speculative workarounds.

A verified bootstrap must leave tracked project files unchanged. Check `git status` after running candidate steps. If setup rewrites a tracked lockfile or generated source unexpectedly, reject that sequence and choose a repository-supported clean alternative; do not normalize a dirty worktree as successful setup.

## Worktree policy

Implementation work must be isolated by default.

- If the current directory is already a clean, task-specific worktree, reuse it.
- Otherwise invoke Superpowers’ `using-git-worktrees` workflow before modifying project files. When no native harness-managed worktree is available, create the manual worktree at `<primary-checkout>/.worktrees/<task-slug>` after verifying `.worktrees/` is ignored.
- Never nest worktrees.
- Do not move, delete, reset, or clean unrelated worktrees.
- Read-only intake and diagnosis may happen before worktree creation; implementation may not.
- Preserve a task worktree while its pull request remains open. After a merge, remove only an Omakase-created worktree that is clean and has the expected identity; delete its local task branch only after successful removal. Remote branch deletion still requires explicit authorization.

## Delivery workflow

### 1. Understand and plan

Use the relevant Superpowers workflow. Match planning depth to the task: do not inflate a bounded change into a product-design exercise, but do not skip required design or planning gates for substantial work.

Once the user approves a design through interactive back-and-forth, faithfully writing and self-reviewing the design spec, creating the implementation plan, and proceeding with the authorized implementation does not require a second approval. Ask again only when the written artifact or new evidence materially diverges from the approved scope, behavior, architecture, risk, acceptance criteria, or external actions.

### 2. Implement and validate

Implement in the task worktree. When the worktree is not ready, run every profile `bootstrap.steps` entry in order. Select the configured runtime for each bootstrap or validation entry; never apply one textual runtime prefix to an entire mixed-runtime process tree. Follow the runtime-resolution rules in [references/project-guidance.md](references/project-guidance.md). Then use the profile's validation commands alongside project-provided commands and repository conventions. Apply TDD, systematic debugging, and verification as required by the corresponding Superpowers skills.

Do not serialize independent preparation behind a long full-suite baseline. When useful, start a background baseline asynchronously, retain its live process, and continue non-dependent discovery, design, specification, planning, or review. Do not modify files, dependencies, generated artifacts, or configuration consumed by that running check. A focused relevant baseline may gate the first implementation edit; full validation must run again after implementation.

Treat mutation of one dependency tree as an exclusive operation. While an installer is active, do not start another installer, test, build, or commit hook that consumes or mutates that tree. If installation fails or is interrupted after touching the tree, wait for the installer to exit, treat the tree as untrusted, and use the repository's clean deterministic bootstrap command before running consumers.

When a long-running setup command yields a live process or session, retain and monitor that same process. Retry only after confirming it exited or failed; lack of recent output alone is not evidence of failure.

If a dependency tool fails only because its default cache or log directory is outside the writable sandbox, retry with a task-scoped cache under the system temporary directory. Do not change repository configuration, ownership of the user's cache, or the project profile for this harness-specific condition.

Do not accept an agent statement such as “done” as evidence. Inspect the diff and run the applicable validation commands. Report exact commands and outcomes.

### 3. Review and publish

Review the completed diff against the original task. Use Superpowers’ review and branch-finishing workflows where applicable.

When publication is authorized:

- preserve repository branch and commit conventions;
- preserve the repository’s PR template and fill it from known evidence;
- commit only task-related changes;
- push the task branch;
- create or update the pull request;
- read the resulting PR state back before claiming publication succeeded.

Do not merge a protected branch unless the user or established repository policy explicitly authorizes it.

### 4. Follow CI

Inspect required checks immediately after publication.

If checks are pending, create a scheduled follow-up in the current Codex task. The follow-up must retain or restate:

- repository and pull-request URL;
- task branch and worktree path;
- pending checks;
- validation already completed;
- the next permitted action.

Use a practical cadence based on expected CI duration. Avoid permanent polling: stop the schedule when checks resolve, the PR merges or closes, or attention is required.

If CI fails:

1. Gather the failing check, logs, annotations, and relevant commit state.
2. Use systematic debugging to identify the root cause.
3. Repair clear in-scope failures in the same worktree without asking for a redundant yes/no confirmation.
4. Repeat appropriate local validation and completion verification.
5. Push the repair and resume scheduled follow-up.

Ask before expanding scope, changing product behavior, weakening tests or CI, modifying secrets or infrastructure, or taking an action that needs new authority.

### 5. Follow review feedback

When review feedback arrives:

1. Fetch the full actionable context, not only a notification summary.
2. Use Superpowers’ `receiving-code-review` discipline to evaluate technical validity.
3. Implement clear, in-scope requests; validate, push, and resume CI monitoring.
4. Do not automatically treat general discussion, preferences, or conflicting requests as coding instructions.

Escalate conflicting or materially ambiguous feedback with a concise explanation and recommendation.

## Attention policy

Do not ask the user to confirm safe, expected actions already authorized by the delivery request. Continue through routine editing, testing, validation, and follow-up when permissions allow.

Request attention for:

- unresolved product or acceptance ambiguity;
- conflicting task, repository, or review requirements;
- credentials, permissions, or unavailable integrations;
- destructive, irreversible, security-sensitive, or materially broader actions;
- an unexpected failure for which the next repair would be speculative;
- a merge or release decision not covered by existing authorization.

Every attention request must state:

1. what was discovered;
2. why progress cannot safely continue;
3. the smallest decision or authority needed;
4. the recommended option.

## Completion

Do not impose a custom turn, repair, or token budget. Let the coding harness enforce its own limits.

By default, a delivered change is complete when:

- implementation is isolated from unrelated work;
- the diff satisfies the task;
- applicable local validation passes;
- the branch is published and a PR exists when appropriate;
- required CI is green;
- unresolved review feedback is absent;
- the user has been told whether the PR is ready, merged, or waiting on an explicitly identified decision.

If merge is external, continue monitoring only when a scheduled follow-up is useful and authorized. Stop obsolete schedules promptly.
