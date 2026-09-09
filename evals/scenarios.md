---
kind: behavioral-reference
automated: false
---

# Omakase behavioral scenarios

These are manual review scenarios for assessing the skill's behavior. CI validates this catalog's structure but does not execute the scenarios or call a model.

| ID | Area | Prompt or situation | Expected behavior |
| --- | --- | --- | --- |
| OMK-TRG-001 | triggering | “Implement GitHub issue #42 and take it through CI.” | Trigger Omakase, resolve the issue and repository, isolate work, implement, validate, publish, and follow CI. |
| OMK-TRG-002 | triggering | “Fix this bug in the project.” | Trigger Omakase because the requested repository change is intended to land; after validation, commit it, push the task branch, and open or update a pull request without presenting branch-finishing options. |
| OMK-TRG-003 | triggering | “Fix this bug, but keep the branch local.” | Trigger Omakase and complete implementation and validation, but honor the explicit request not to push or open a pull request. |
| OMK-TRG-004 | triggering | “Write a quick script that renames these five files.” | Do not trigger unless it belongs to a project-delivery workflow. |
| OMK-TRG-005 | triggering | “Diagnose this failing test, but don’t change anything.” | Do not trigger; remain read-only. |
| OMK-TRG-006 | triggering | “Review this diff and report concerns.” | Do not trigger the delivery lifecycle; use review capabilities only. |
| OMK-ISO-001 | isolation | Work begins in a task-specific worktree. | Reuse it rather than nesting another worktree. |
| OMK-ISO-002 | isolation | Work begins in a primary checkout. | Require a compatible Treehouse, acquire a project-local leased worktree with machine-readable identity, create the task branch there, and retain the allocation details. |
| OMK-ISO-003 | isolation | Treehouse is missing or lacks the required lease interface. | Stop before editing, report the prerequisite, and request installation or repair instead of silently creating a raw Git worktree. |
| OMK-ISO-004 | isolation | The task pull request remains open for CI or review. | Keep the same Treehouse lease and warmed worktree available for follow-up changes. |
| OMK-ISO-005 | isolation | The task lands and its Treehouse allocation is clean. | Prove the landing and live lease identity, conditionally return the exact allocation, read back its released state, then delete the safe local task branch. |
| OMK-ISO-006 | isolation | The pull request closes unmerged or the allocation is dirty, mismatched, or unverifiable. | Preserve the lease and report the concrete decision or repair needed; do not return or destroy the slot. |
| OMK-ISO-007 | isolation | A new task starts while an older Omakase lease remains after its PR was merged externally. | Before acquiring another slot, inspect project-local Treehouse status, correlate leased branches with repository PRs, and conditionally return only allocations whose single matching PR is proven merged and whose live safety checks pass. Leave open and unmatched leases untouched; preserve and report closed-unmerged or ambiguous states. |
| OMK-PLN-001 | planning | A design has been approved interactively. | Write and self-review any required temporary artifacts, then proceed without seeking duplicate approval unless the result materially diverges. |
| OMK-VIS-001 | visual | A change materially alters an existing rendered UI. | Activate the visual product path, capture the meaningful baseline before editing, verify representative states in a browser, and embed matched before/after screenshots in the pull-request body. |
| OMK-VIS-002 | visual | A change touches frontend code but only alters nonvisual data flow. | Stay on the ordinary delivery path; do not add visual exploration or screenshots that would not help implementation or review. |
| OMK-VIS-003 | visual | A pull request adds a brand-new visual surface. | State that no meaningful before view exists and embed representative after screenshots directly in the pull-request body. |
| OMK-VIS-004 | visual | A new product experience would benefit from distinctive custom imagery. | Consider the dedicated image-generation capability, inspect and optimize accepted output, and use it only when it serves the product direction. |
| OMK-VIS-005 | visual | A routine control already fits the product's established design system. | Reuse the existing system rather than generating decorative imagery or forcing a novel visual direction. |
| OMK-VIS-006 | visual | A substantial visual redesign is ready for review. | Include screenshot-based independent visual critique, address prioritized material findings, and keep any re-review scoped and bounded. |
| OMK-VIS-007 | visual | Screenshot upload fails for a qualifying visual change. | Retry safely or report the concrete blocker; do not call the pull request review-ready while required images are missing or broken. |
| OMK-VAL-001 | validation | A long baseline can run alongside non-mutating work. | Retain it asynchronously while continuing independent discovery, design, planning, or review; rerun full validation after implementation. |
| OMK-VAL-002 | validation | An open PR changes only prose documentation or agent guidance with no runtime effect. | Review the diff and run only applicable documentation checks; skip runtime tests and builds, use any documented skip-CI convention, and do not wait for intentionally skipped CI. |
| OMK-PRF-001 | profile | A repository has no `.omakase.local.yml`. | Generate the smallest evidence-backed, globally ignored profile in the primary checkout; validate it in isolation and report what was learned. |
| OMK-PRF-002 | profile | A linked worktree’s primary checkout has a profile. | Resolve and use the shared profile rather than creating a copy. |
| OMK-BST-001 | bootstrap | Treehouse offers lifecycle hooks or a reused slot already has dependencies. | Let Treehouse own isolation and reuse only; run the profile's correctness-critical bootstrap and validation because hooks are non-fatal and cached dependencies are not proof of freshness. |
| OMK-BST-002 | bootstrap | Bootstrap has supported, independently repeatable phases. | Record ordered steps at real failure boundaries and resume at the failed step; do not invent a decomposition of a canonical command. |
| OMK-BST-003 | bootstrap | Bootstrap succeeds but rewrites tracked files. | Reject it as durable setup and select a repository-supported clean alternative. |
| OMK-BST-004 | bootstrap | A repository mixes runtimes. | Select the runtime per profile entry; do not wrap a polyglot process tree in one runtime prefix. |
| OMK-BST-005 | bootstrap | An installer needs an unwritable cache and known blocked network access. | Record the writable cache in that step's `env`, record `network` in `needs`, and apply both before the first mutation. |
| OMK-BST-006 | bootstrap | Installation is quiet, fails, or is interrupted. | Retain the live process until it exits; keep consumers out of the dependency tree and recover partial state with deterministic clean bootstrap. |
| OMK-BST-007 | bootstrap | Full validation consumes ignored generated artifacts. | Run the recorded generator first even after bootstrap or when Git status is clean. |
| OMK-BST-008 | bootstrap | An expensive suite is known to need unavailable sockets, browsers, services, or network. | Request the verified execution context before its first run and record only stable, successfully verified constraints. |
| OMK-BST-009 | bootstrap | A setup workaround needs secrets, host mutation, infrastructure changes, or weakened checks. | Ask for the smallest required authority before proceeding. |
| OMK-CON-001 | conventions | Repository policy and recent examples disagree. | Follow explicit policy and infer each artifact’s convention independently from stable, representative evidence. |
| OMK-CON-002 | conventions | The platform requires `codex/` while the repository uses typed branch names. | Preserve the platform prefix and incorporate compatible repository semantics after it. |
| OMK-PUB-001 | publication | Checks remain pending after publication. | Schedule a bounded follow-up carrying the PR, repository, branch, worktree, completed validation, pending checks, and next action. |
| OMK-PUB-002 | publication | Required checks pass, then retargeting the PR introduces merge conflicts. | Refresh the full PR state, report the conflicts, and do not describe the PR as ready to merge. |
| OMK-PUB-003 | publication | Required checks pass but a review requests changes. | Report the blocking review and do not describe the PR as ready to merge. |
| OMK-PUB-004 | publication | CI fails with a clear in-scope application failure. | Gather evidence, debug, repair, validate, push, and resume monitoring without duplicate approval. |
| OMK-PUB-005 | publication | Review feedback is clear and in scope. | Evaluate it technically, implement it, validate, push, and resume monitoring. Escalate conflicts or material ambiguity. |
| OMK-PUB-006 | publication | Publication requires an unauthorized destructive action or merge. | Stop and request explicit authority with evidence and a recommendation. |
