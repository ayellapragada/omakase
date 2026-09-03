# Omakase Conductor Skill Design

Status: approved for first implementation  
Date: 2026-09-02

## Purpose

Omakase is a personal Codex skill for coding work that is meant to land in an actual project. It keeps Codex as the application and coding agent, then supplies the missing delivery loop: isolated implementation, project-aware validation, publication, CI follow-up, review follow-up, and a precise handoff when human judgment is genuinely required.

Omakase is not an agent harness, issue tracker, daemon, or replacement UI.

## Trigger model

Omakase uses a hybrid trigger.

It should activate implicitly when the user requests a repository change that is intended to be delivered, especially when the request includes a GitHub issue, Shortcut story, pull request, feature, bug fix, refactor, or language such as “take this through CI” or “follow this through.” It can also be invoked explicitly as `$omakase`.

It should not activate for:

- small one-off or throwaway scripts outside an actual project delivery workflow;
- read-only explanations, exploration, or code review;
- diagnosis or debugging when the user has not asked for a fix;
- ordinary file manipulation that is not intended to land in a repository;
- monitoring requests that are unrelated to coding delivery.

## Responsibility boundary

Omakase coordinates capabilities rather than duplicating them.

- Codex owns reasoning, coding, tools, task continuity, permissions, and notifications.
- Superpowers owns brainstorming, planning, worktree creation, TDD, systematic debugging, code-review discipline, verification, and branch-finishing practices.
- The GitHub plugin owns GitHub issue, pull-request, review, check, and Actions access.
- Grim owns Wistia Shortcut and sanctioned internal-service access when it is available in the session.
- Codex scheduled tasks own delayed and recurring follow-ups.
- Repository instructions and project configuration own project-specific commands and conventions.

The separately installed `gh-fix-ci` skill remains available for direct use, but Omakase does not depend on its approval-heavy repair workflow. Omakase may inspect CI through the GitHub plugin and apply Superpowers debugging and verification directly.

## Delivery workflow

1. Resolve the task source, target repository, and definition of done.
2. Read applicable `AGENTS.md`, repository documentation, and PR templates; resolve or generate the personal `.omakase.local.yml` profile from the primary checkout.
3. For implementation work, use an existing task-specific worktree or invoke Superpowers’ worktree skill before changing files. Manual worktrees live predictably at `<primary-checkout>/.worktrees/<task-slug>`.
4. Use the applicable Superpowers workflow for design, planning, implementation, debugging, review, and verification. One interactive design approval authorizes faithful design documentation, planning, and implementation; only material divergence creates another approval boundary.
5. Run the project’s stated validation. Never invent success from an agent completion message.
6. Publish according to repository policy: commit, push, and open or update a PR when authorized.
7. Inspect CI immediately. If checks are pending, schedule a follow-up in the current Codex task.
8. When CI fails, gather evidence, repair the root cause in the same worktree, repeat local verification, push, and continue monitoring.
9. When actionable review feedback arrives, evaluate it rigorously, implement clear requests, revalidate, push, and continue monitoring.
10. Stop when the configured completion point is reached or a genuine attention item blocks safe progress.

## Attention policy

Do not ask the user to reconfirm safe, expected steps that are already authorized by the delivery request. Ask only when the answer would materially change the implementation or requires authority Codex does not have, including product ambiguity, conflicting requirements, credentials, destructive or irreversible actions, unclear review intent, or a merge decision not covered by existing policy.

Questions must include the evidence discovered, the decision required, and the recommended option.

## Completion

Omakase does not impose a turn or repair budget. The underlying coding harness and available execution environment govern resource limits.

By default, completion means the requested change is implemented in an isolated worktree, project validation passes, the branch is published, a PR exists when appropriate, and required CI is green. Omakase does not merge protected branches unless the user or repository policy has explicitly authorized that behavior. If merge is external, Omakase may continue monitoring until it observes the merge.

## Personal project profiles

Omakase first honors existing repository instructions. For the small amount of personal, machine-specific knowledge that repeatedly matters in isolated worktrees, it maintains one globally ignored `.omakase.local.yml` at the root of the primary checkout.

The profile is generated lazily the first time Omakase works in a repository. Codex inspects existing instructions, runtime files, setup scripts, package scripts, Make targets, and CI configuration, then writes only fields supported by that evidence. It may run established safe repository entry points without another confirmation. It must ask before inventing shell setup, retrieving secrets, changing infrastructure, weakening checks, or performing destructive work.

All linked worktrees resolve the primary checkout through Git worktree metadata and share its profile. The profile records ordered idempotent bootstrap steps, fast and full validation, required local file paths, CI expectations, and publication defaults only when useful. Each executable step selects its own runtime. The profile never contains secret values and is never committed.

Bootstrap is a sequence because a clean worktree may need both a repository setup entry point and generated artifacts before its baseline is meaningful. Runtime selection is per step rather than a textual prefix over an entire process tree, avoiding cross-language executable collisions in polyglot projects. Long-running setup processes are monitored through their existing live session and are not restarted merely because output is quiet. Dependency installation is exclusive for its dependency tree; interrupted installs make that tree untrusted until a repository-supported clean deterministic bootstrap succeeds. Sandbox-only cache failures use task-scoped temporary caches and do not become project configuration.

Long full-suite baselines do not block independent discovery, design, specification, planning, or review. Omakase may retain a baseline process in the background while continuing non-dependent work, but it does not mutate inputs consumed by the running check and always runs applicable full validation again after implementation.

Successful setup must also preserve a clean tracked worktree. A candidate sequence that rewrites a lockfile or tracked generated source is not persisted merely because it exits successfully; Omakase selects and verifies a repository-supported clean alternative.

The profile evolves through verified learning. When setup fails, Omakase diagnoses the cause and records a change only if the fix is durable and reproducible in future worktrees. Transient network, sandbox, CI, and cache failures are not persisted.

## First-version artifacts

- `skills/omakase/SKILL.md`: concise conductor instructions and trigger boundary.
- `skills/omakase/agents/openai.yaml`: display metadata and default prompt.
- `skills/omakase/references/project-guidance.md`: profile lifecycle and safety policy.
- `skills/omakase/assets/omakase.local.example.yml`: minimal generation template.
- `skills/omakase/scripts/profile_path.py`: deterministic primary-checkout resolver.
- `evals/scenarios.md`: behavioral trigger and workflow scenarios.
- `tests/test_skill.py` and `tests/test_profile_path.py`: contract and real linked-worktree tests.
