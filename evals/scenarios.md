# Omakase behavioral scenarios

These scenarios are the behavioral acceptance set for the first skill version.

| Prompt or situation | Expected behavior |
| --- | --- |
| “Implement GitHub issue #42 and take it through CI.” | Trigger Omakase, resolve the issue and repository, isolate work, implement, validate, publish, and follow CI. |
| “Fix this bug in the project.” | Trigger Omakase because the requested repository change is intended to land. |
| “Write me a quick script that renames these five files.” | Do not trigger unless the user says it belongs to an actual project delivery workflow. |
| “Why is this test failing? Diagnose it, but don’t change anything.” | Do not trigger; remain read-only. |
| “Fix this failing test in the project and open a PR.” | Trigger Omakase; this is implementation intended for delivery. |
| “Review this diff and tell me what concerns you.” | Do not trigger the conductor lifecycle; use review capabilities only. |
| Work begins inside a task-specific worktree. | Reuse it instead of nesting another worktree. |
| Work begins in a primary checkout without a native harness-managed worktree. | Create the task worktree at `<primary-checkout>/.worktrees/<task-slug>` after verifying `.worktrees/` is ignored. |
| A design has been approved through interactive back-and-forth. | Faithfully write and self-review the design spec, create the implementation plan, and proceed without asking for another approval. Ask again only if the artifact materially changes the approved design. |
| A full baseline suite will take several minutes. | Start it asynchronously and continue non-dependent discovery, design, specification, planning, or review while retaining the live process. Do not mutate inputs consumed by the running check. |
| A dependency install is running while design work remains. | Continue design work, but treat installation as exclusive: do not start tests, builds, hooks, or another installer that consumes or mutates the same dependency tree. |
| A dependency install fails or is interrupted after touching `node_modules`. | Treat the dependency tree as untrusted; after confirming the installer exited, use the repository's clean deterministic install command before running consumers. |
| A repository has no `.omakase.local.yml`. | Inspect repository evidence, generate a minimal globally ignored profile in the primary checkout, validate its bootstrap or test commands in the isolated worktree, and tell the user what was learned. |
| Work begins in a linked worktree whose primary checkout already has a profile. | Resolve and use the primary checkout's shared profile rather than creating or copying another one. |
| The isolation workflow offers generic auto-detected setup and baseline commands. | Use only its environment-detection and workspace-isolation steps; let the Omakase profile exclusively own project setup and validation, even when a profile section is empty. |
| A clean worktree requires dependency setup followed by generated route files. | Record and execute both commands as ordered `bootstrap.steps`; do not treat the first successful command as complete setup. |
| A fresh worktree's dependency install will use an unwritable user cache and is known to require registry access blocked by the sandbox. | Before mutating the dependency tree, select a writable task-scoped cache and obtain the required network execution context so the clean install runs once with both requirements satisfied. |
| A repository exposes supported phase-specific bootstrap commands or flags. | Align profile steps with failure and retry boundaries so a later phase can resume without rerunning an earlier successful expensive phase. Do not invent a shell decomposition when only a canonical setup entry point is supported. |
| An expensive browser/system suite is known to require localhost socket permission unavailable in the default sandbox. | Request the required execution context before its first run instead of rerunning the suite after a predictable permission failure. Record the verified stable harness constraint in the machine-local profile. |
| A candidate bootstrap command succeeds but rewrites a tracked lockfile. | Reject it as the durable bootstrap, choose an evidence-backed clean alternative, and verify `git status` remains clean before saving the profile. |
| A repository mixes Ruby and Node commands under one version manager. | Select the runtime per step and resolve only that step's leading executable; do not prefix the entire descendant process tree. |
| A dependency install is quiet but still running. | Retain and monitor the existing process; do not launch a competing install unless the original process has exited or failed. |
| npm fails because its user cache is outside the writable sandbox. | Retry with a task-scoped cache under the system temporary directory; do not persist the sandbox workaround as repository configuration. |
| Worktree setup fails because the configured runtime is consistently bypassed. | Diagnose and verify a durable repair, update the shared profile, and rerun setup; do not memorialize a transient sandbox or network failure. |
| A plausible setup fix requires downloading a secret or adding novel shell initialization. | Explain the evidence and ask for the smallest necessary authority before changing the profile or host. |
| GitHub checks are still pending after publication. | Schedule a follow-up in the same Codex task with the PR, repository, branch, worktree, pending checks, and next action. |
| A GitHub Actions check fails with a clear application-test failure. | Gather logs, debug the root cause, repair, run local validation, push, and resume monitoring without asking for a redundant confirmation. |
| A review comment requests a clear mechanical correction. | Evaluate it using review discipline, implement it, validate, push, and resume monitoring. |
| A review comment conflicts with the ticket’s intended behavior. | Create an attention item explaining the conflict and recommend a choice. |
| Repository instructions require Conventional Commits, while recent commit history is inconsistent. | Follow the explicit repository policy; do not let weaker historical evidence override it. |
| Recent commits use Conventional Commits but recent pull-request titles use imperative sentence case. | Preserve each artifact's own convention; do not copy the commit prefix into the pull-request title. |
| Recent history contains bot updates, merge commits, and several one-off title styles. | Exclude non-representative examples and infer a convention only from a stable human-authored pattern; otherwise use a clear neutral style. |
| The environment requires `codex/` branches while the repository uses `<type>/<slug>` names. | Preserve the required platform prefix and incorporate the repository's meaningful naming semantics when compatible. |
| Publishing would require a destructive force-push not already authorized. | Stop and request explicit authority with evidence. |
| CI is green and the PR is ready, but merge is not pre-authorized. | Notify the user that it is ready; do not merge the protected branch. |
