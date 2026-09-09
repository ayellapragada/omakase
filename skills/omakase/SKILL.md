---
name: omakase
description: Use when a requested change to an actual code project is intended to land, including features, fixes, refactors, tickets, pull requests, CI follow-up, or review follow-up; also use when invoked explicitly as `$omakase`. Do not use for one-off scripts, read-only explanation or review, or diagnosis-only debugging.
---

# Omakase

Coordinate project delivery around Codex without creating another agent harness, tracker, or workflow engine.

## Scope

Trigger for repository changes intended to land, including work from an issue or pull request and requests to publish, follow CI, address review, or merge. When activating, say briefly that Omakase applies because the request is project work intended to land.

Do not trigger for one-off scripts, read-only exploration or review, diagnosis without a requested fix, ordinary file manipulation, or unrelated monitoring. If intent to deliver is ambiguous and affects what would be changed or published, ask rather than expanding the request silently.

## Own the delivery contract

Omakase directly defines the core workflow for planning, isolation, implementation, validation, review, publication, and follow-up.

- Superpowers is optional. Use it when the user explicitly requests it or when scale, risk, or repository policy warrants a deeper specialized workflow; Omakase does not depend on it.
- Use available GitHub tooling for issues, pull requests, reviews, checks, and Actions evidence. `gh-fix-ci` is optional, not a dependency.
- Use Grim for Wistia Shortcut or internal-service context when required by `AGENTS.md`. If Grim is unavailable, say so rather than searching for a private CLI.
- Use Codex scheduled follow-ups for delayed CI, review, or merge checks.
- Treat user instructions, `AGENTS.md`, repository documentation, and pull-request templates as authoritative policy.

## Operating defaults

### Lean review

Keep ordinary delivery in the main implementation context. Run focused checks while developing and full applicable validation before publication. Every change intended to land gets one independent review of the completed diff; fix material findings, rerun affected validation, and request at most one scoped re-review when those fixes warrant it.

Use implementer-per-task delegation only when the user requests exhaustive execution, repository policy requires it, or scale and risk justify the extra review cycle. Route every dispatch explicitly: cheapest capable tier for mechanical work, a balanced tier for ordinary implementation or review, and the strongest tier for architecture, security, concurrency, difficult debugging, or consequential final review. Always set both model and reasoning effort.

### Authority

Continue through safe editing, validation, publication, and follow-up already authorized by the delivery request. Ask only for a material product decision, conflicting requirements, missing credentials or permissions, destructive or security-sensitive action, broader scope, speculative repair, or an unauthorized merge or release.

An attention request states what was found, why progress cannot safely continue, the smallest decision or authority needed, and the recommended option.

## Intake and isolation

Before editing:

1. Resolve the task source, definition of done, and target repository.
2. Read applicable instructions and the personal project profile in [references/project-guidance.md](references/project-guidance.md).
3. Resolve artifact-specific writing and naming rules with [references/repository-conventions.md](references/repository-conventions.md).
4. Inspect Git status and preserve unrelated changes.
5. Ask only when missing information materially changes the result.

When the repository uses a project-local Treehouse pool, opportunistically reconcile landed allocations during intake through [the Treehouse lifecycle](references/treehouse-worktrees.md). This maintenance does not change which provisioning environment owns the current task's workspace.

Implementation is isolated by default. If the task already runs in a clean task-specific worktree, reuse it rather than acquiring another. Otherwise, Treehouse is the required provisioning layer: read the Treehouse lifecycle reference, verify its required lease interface, and create an isolated worktree from its project-local pool. Do not silently fall back to a raw Git worktree when Treehouse is missing or incompatible; report the prerequisite and request the smallest action needed to restore it.

Isolation remains environment separation only: the Omakase profile owns setup and validation. Preserve either workspace while its pull request is open. For a pre-existing task worktree, leave its cleanup to the provisioning environment; for an Omakase-acquired lease, follow the identity-checked return rules in the Treehouse reference after landing. Never nest worktrees or alter unrelated ones. Remote branch deletion requires explicit authorization.

## Personal project profile

Each repository may have one globally ignored `.omakase.local.yml` in its primary checkout, shared by linked worktrees. Resolve it from this skill directory with [scripts/profile_path.py](scripts/profile_path.py):

```bash
python3 scripts/profile_path.py --repo <checkout-or-worktree>
```

If it exists, read it after higher-priority repository instructions. If absent, use [assets/omakase.local.example.yml](assets/omakase.local.example.yml) and [references/project-guidance.md](references/project-guidance.md) to create the smallest evidence-backed profile. Before creating it, prove that Git ignores the resolved path; if not, stop and report the missing protection. Verify a created profile in the isolated worktree and tell the user. Update it only with durable, successfully verified machine-local knowledge; never store secrets or transient failures.

## Delivery

### Visual product work

When a change materially affects the rendered product experience, read [references/visual-product-work.md](references/visual-product-work.md) before implementation. Use that path for changes to UI, layout, styling, interaction states, or product imagery when visual exploration or evidence will improve the result. Do not activate it merely because a change has a frontend file; nonvisual logic, infrastructure, and internal refactors stay on the ordinary delivery path.

### Plan

Plan at a depth proportionate to the change. For a straightforward, well-specified change, keep the plan concise and proceed. For work with meaningful product, architecture, security, or UX choices, explore the requirements and obtain design approval before implementation. Once the user approves a design interactively, faithfully writing and self-reviewing any temporary working artifacts and proceeding with implementation does not require a second approval. Ask again only if new evidence materially diverges from the approved scope, behavior, architecture, risk, acceptance criteria, or external actions.

### Implement and validate

Work in the isolated checkout. Follow the profile's ordered bootstrap and validation entries plus repository-provided checks. Read [references/project-guidance.md](references/project-guidance.md) before setup or validation; it defines runtime selection, clean bootstrap, dependency-tree safety, generated artifacts, sandbox preflight, long-running processes, and durable profile updates.

Classify the completed diff before choosing validation. A documentation-only change means every changed file is prose documentation or agent guidance and cannot affect runtime behavior. For such a diff, run the documentation-focused checks that apply—diff review, formatting, links, or skill validation—and skip runtime tests, builds, and CI waiting. Do not classify changes to workflows, executable configuration, dependencies, schemas, migrations, generated files, or assets as documentation-only. Use the repository's documented skip-CI convention when one applies.

Do not block independent discovery, design, or review behind a long baseline when they can proceed safely without mutating its inputs. Inspect the diff and run applicable validation yourself; an agent's “done” is not evidence. Report exact commands and outcomes.

### Review and publish

Review the completed diff against the task, repository policy, and acceptance criteria. Obtain one independent review for ordinary changes; increase review depth only when risk warrants it. Treat a project change intended to land as authorization to publish it through a pull request after validation. Do not present the branch-finishing options menu or ask whether to push; proceed directly to the pull-request path unless the user explicitly asks to keep the work local or an attention condition prevents publication.

On the default publication path, follow the resolved convention for each artifact, preserve the pull-request template, commit only task-related changes, push the task branch, create or update the pull request, and read the resulting commit and PR state back. This default does not authorize merging, force-pushing, releasing, or any destructive or materially broader action.

### Follow CI and review

Whenever assessing GitHub status, read the current PR state, draft status, mergeability and merge-state, required checks, and review decision. Refresh all of them after changing its base branch or making another PR mutation. Say a PR is ready to merge only when it is open and non-draft, required checks are green or intentionally skipped under repository policy, GitHub reports no merge conflicts or policy blockers, and no requested changes or required reviews are outstanding. Treat unknown mergeability as pending rather than ready. Report blockers precisely and continue follow-up or request attention as appropriate.

When a documentation-only change validly uses a skip-CI convention, confirm the published artifact and current PR state once; do not wait for or schedule CI that was intentionally skipped.

If required checks or mergeability are pending, schedule a follow-up in the current Codex task carrying the repository and PR URL, branch and worktree, pending conditions, completed validation, and next permitted action. Concrete blockers such as conflicts, failed checks, draft status, or unsatisfied review requirements must be reported and handled or escalated as appropriate. Stop follow-up when the PR becomes ready, closes or merges, or attention is required. Do not keep monitoring a ready PR solely to reclaim its Treehouse lease after an expected external merge; a later Omakase task will reconcile landed allocations before it acquires isolation.

For CI failures, gather logs and commit state, debug the root cause, repair clear in-scope failures in the same worktree, validate, push, and resume monitoring. For review feedback, fetch the full context, verify each request against the code and task, implement clear in-scope requests, validate, push, and resume monitoring. Escalate conflicting or materially ambiguous feedback.

## Completion

Do not invent turn, repair, or token budgets. A delivered change is complete when the isolated diff satisfies the task, applicable local validation passes, publication exists when appropriate, required CI is green or intentionally skipped under repository policy, actionable review feedback is resolved, and the user knows whether the PR is ready, merged, or awaiting a specific decision. Continue monitoring external merge state only when a scheduled follow-up is useful and authorized.
