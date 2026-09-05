# Omakase behavioral scenarios

These scenarios are the maintained behavioral acceptance set for the skill.

| Prompt or situation | Expected behavior |
| --- | --- |
| “Implement GitHub issue #42 and take it through CI.” | Trigger Omakase, resolve the issue and repository, isolate work, implement, validate, publish, and follow CI. |
| “Fix this bug in Sushi.” | Trigger Omakase because the requested repository change is intended to land; after validation, commit it, push the task branch, and open or update a pull request without presenting branch-finishing options. |
| “Fix this bug, but keep the branch local.” | Trigger Omakase and complete implementation and validation, but honor the explicit request not to push or open a pull request. |
| “Write a quick script that renames these five files.” | Do not trigger unless it belongs to a project-delivery workflow. |
| “Diagnose this failing test, but don’t change anything.” | Do not trigger; remain read-only. |
| “Review this diff and report concerns.” | Do not trigger the delivery lifecycle; use review capabilities only. |
| Work begins in a task-specific worktree. | Reuse it rather than nesting another worktree. |
| Work begins in a primary checkout without native isolation. | Create `<primary-checkout>/.worktrees/<task-slug>` after verifying it is ignored. |
| A design has been approved interactively. | Write and self-review any required temporary artifacts, then proceed without seeking duplicate approval unless the result materially diverges. |
| A long baseline can run alongside non-mutating work. | Retain it asynchronously while continuing independent discovery, design, planning, or review; rerun full validation after implementation. |
| An open PR changes only prose documentation or agent guidance with no runtime effect. | Review the diff and run only applicable documentation checks; skip runtime tests and builds, use any documented skip-CI convention, and do not wait for intentionally skipped CI. |
| A repository has no `.omakase.local.yml`. | Generate the smallest evidence-backed, globally ignored profile in the primary checkout; validate it in isolation and report what was learned. |
| A linked worktree’s primary checkout has a profile. | Resolve and use the shared profile rather than creating a copy. |
| The isolation workflow offers setup and baseline commands. | Use only its isolation steps; let the profile own setup and validation. |
| Bootstrap has supported, independently repeatable phases. | Record ordered steps at real failure boundaries and resume at the failed step; do not invent a decomposition of a canonical command. |
| Bootstrap succeeds but rewrites tracked files. | Reject it as durable setup and select a repository-supported clean alternative. |
| A repository mixes runtimes. | Select the runtime per profile entry; do not wrap a polyglot process tree in one runtime prefix. |
| An installer needs an unwritable cache and known blocked network access. | Record the writable cache in that step's `env`, record `network` in `needs`, and apply both before the first mutation. |
| Installation is quiet, fails, or is interrupted. | Retain the live process until it exits; keep consumers out of the dependency tree and recover partial state with deterministic clean bootstrap. |
| Full validation consumes ignored generated artifacts. | Run the recorded generator first even after bootstrap or when Git status is clean. |
| An expensive suite is known to need unavailable sockets, browsers, services, or network. | Request the verified execution context before its first run and record only stable, successfully verified constraints. |
| A setup workaround needs secrets, host mutation, infrastructure changes, or weakened checks. | Ask for the smallest required authority before proceeding. |
| Repository policy and recent examples disagree. | Follow explicit policy and infer each artifact’s convention independently from stable, representative evidence. |
| The platform requires `codex/` while the repository uses typed branch names. | Preserve the platform prefix and incorporate compatible repository semantics after it. |
| Checks remain pending after publication. | Schedule a bounded follow-up carrying the PR, repository, branch, worktree, completed validation, pending checks, and next action. |
| Required checks pass, then retargeting the PR introduces merge conflicts. | Refresh the full PR state, report the conflicts, and do not describe the PR as ready to merge. |
| Required checks pass but a review requests changes. | Report the blocking review and do not describe the PR as ready to merge. |
| CI fails with a clear in-scope application failure. | Gather evidence, debug, repair, validate, push, and resume monitoring without duplicate approval. |
| Review feedback is clear and in scope. | Evaluate it technically, implement it, validate, push, and resume monitoring. Escalate conflicts or material ambiguity. |
| Publication requires an unauthorized destructive action or merge. | Stop and request explicit authority with evidence and a recommendation. |
