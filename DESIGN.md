# Omakase Design Specification

Status: v0.3 product and technical design  
Date: 2026-09-02  
Proof-of-concept fixture: Sushi (`/Users/akshithyellapragada/Code/sushi`)

## 1. Summary

Omakase is a personal macOS supervisor for coding work performed by Codex.

The user gives Omakase a task. Omakase resolves the relevant project profile, creates and bootstraps an isolated git worktree, starts or resumes a Codex session inside it, runs the project's established validation process, independently checks the resulting diff against the task, follows CI and review state, gives failures back to the same Codex session, and notifies the user only when judgment or authorization is genuinely required.

Omakase is not a new coding agent. Codex remains responsible for understanding and changing code. Omakase is the durable coordination layer around it.

## 2. Product promise

> Start a ticket, walk away, and come back when it is finished or when a real decision is needed.

For the first version, "finished" means:

1. Codex has completed its implementation.
2. The configured local validation commands pass.
3. A fresh, read-only verification session has reviewed the original task and resulting diff without inheriting the implementation conversation or its self-justification.
4. Omakase has committed and pushed the work to its isolated branch.
5. A pull request exists.
6. Required GitHub checks pass.
7. The resulting diff contains a stated, reviewable connection to the original task, or an explicit no-change outcome has been accepted.
8. Omakase has either observed the merge or marked the work ready for the user to merge, according to the run's completion policy.

## 3. Design principles

### Codex stays in the driver's seat

Omakase embeds Codex through `codex app-server`. It does not recreate an agent loop, rewrite Codex prompts, or place another agent above Codex.

### Durable, not elaborate

Runs, schedules, Codex thread IDs, worktree paths, and external identifiers are persisted locally. Restarting Omakase must not lose track of active work.

### Defaults replace routine confirmations

The user defines policy once per scope and project. Safe, expected operations can then proceed without repeatedly asking for confirmation. Anything outside that policy becomes an explicit, actionable interruption.

### Repository conventions are authoritative

Omakase discovers and preserves `AGENTS.md`, git configuration, pull-request templates, existing test commands, and repository-specific configuration. It does not impose a universal development workflow.

### Generic core, project-specific profiles

Omakase understands stable concepts such as repositories, bootstrap steps, validation suites, resource leases, CI evidence, and publication. A reviewable project profile maps those concepts onto a particular codebase. Rails conventions may help discover a profile, but Rails, RSpec, database names, and workflow names are not built into the core.

### Isolation is mandatory

Every implementation phase starts in a dedicated worktree. A preceding read-only intake or profiling pass may inspect a primary checkout, but Omakase never changes it or performs implementation there.

### Completion is evidence-based

An agent saying "done" is not completion. Local validation, independent semantic review, git state, pull-request state, CI, and an explicit account of how the diff satisfies the task provide the evidence. Green checks prove that configured checks passed; they do not by themselves prove that the requested change was implemented correctly.

### Verification cannot rewrite its own rules silently

The validation configuration used by a run is pinned before implementation starts. Changes to trusted validators, CI policy, or Omakase configuration cannot silently redefine success. Ordinary test files remain implementation code and are evaluated through configured integrity signals and independent verification rather than blanket path protection.

### The core does not depend on the window

The durable supervisor is a headless user process with a CLI. The macOS application is a client of that process. Closing or quitting the graphical application must not silently abandon active work.

### The UI shows exceptions, not theater

The product should not simulate a company, create artificial agent personas, or require the user to manage a miniature issue tracker. The primary UI is a concise list of work and anything that needs attention.

## 4. Terminology

### Scope

A named collection of local paths and policies in which work may be started.

A scope is deliberately not synonymous with a git repository. It can represent:

- one repository, such as `~/Code/sushi`;
- a folder containing many repositories, such as `~/Code/wistia`;
- a focused set of repositories, such as `wizard` and `grim` together.

The proof of concept supports one repository per scope. Multi-repository scopes are part of the design and follow after the core loop is proven.

### Task

The unit of user intent. A task can originate from free-form text, a GitHub issue, or later a Shortcut story.

### Project profile

A trusted, versioned description of how Omakase should operate one repository: git defaults, bootstrap requirements, validation commands, resource constraints, CI checks or dispatches, protected control-plane paths, and completion policy. A profile may extend reusable user-owned templates and may be proposed by a read-only Codex discovery session, but Omakase validates the resolved result and the user trusts it before any command is executed automatically.

### Run

One execution history for a task. A run owns a Codex thread, one or more worktrees, scheduled follow-ups, validation attempts, and external links.

### Attention item

A question, policy decision, conflict, or failure that Omakase cannot safely resolve under the configured policy.

## 5. First user experience

### Configure a project

The user points Omakase at a repository or a scope containing repositories. Repository indexing is lightweight; a folder scope such as `~/Code/wistia` does not cause every discovered repository to be profiled immediately. When a task first targets a repository without a trusted profile, Omakase offers a read-only discovery pass. Codex inspects repository instructions, language and framework conventions, scripts, CI configuration, pull-request templates, obvious local setup requirements, and available user-owned templates, then proposes a project profile.

The proposal explicitly calls out uncertain or sensitive items. The user reviews it once, including any local-only files or secret-bearing environment mappings. Omakase validates the schema and command locations, stores the trusted user-owned profile, and may optionally emit a shareable `.omakase.yml` containing only repository-safe configuration. It never executes an LLM-proposed command merely because it was proposed.

This is a shared interface across projects. A Rails-aware discovery prompt can recognize common shapes such as `bin/setup`, `bin/rails test`, RSpec, parallel test databases, and GitHub Actions, while the resulting profile still uses the same generic bootstrap, validation, resource, and CI schema as any other project. Reusable templates can hold common Rails defaults so each new app needs only a reviewed repository-specific overlay.

Sushi is the first concrete profile and acceptance fixture; its details are collected in Appendix A rather than treated as core behavior.

### Start work

The user enters a task or pastes a GitHub issue URL. The only required choices are the scope and task description.

Omakase then:

1. Resolves and snapshots the trusted project profile.
2. Starts a cheap, read-only Codex intake turn in the source repository. It either reports `ready` or asks only genuinely blocking questions; `ready` requires no user interaction.
3. Fetches the configured remote after intake succeeds.
4. Creates a branch from the latest configured base ref and an isolated worktree.
5. Copies or links configured local-only files and runs the pinned bootstrap steps.
6. Continues the Codex thread with its working directory set to the worktree and streams progress to connected clients.
7. Waits for Codex to finish its implementation turn.
8. Requires a final implementation-evidence statement and checks that an implementation task produced a meaningful diff.
9. Runs the configured, pinned local validation.
10. If validation fails, checks repair-integrity policy, sends the relevant failure output back to the same Codex thread, and repeats within the configured repair limits.
11. Starts a fresh read-only Codex verification thread with the original task and base-to-final diff, but no implementation history or completion self-report.
12. If independent verification rejects the change, sends its findings to the implementation thread for repair; repeated materially identical rejection becomes attention.
13. Omakase commits the validated tree, pushes the task branch, and creates or discovers its pull request when policy permits.
14. Starts or observes the configured GitHub checks and workflows.
15. If CI fails, checks repair-integrity policy, sends the failure summary and useful logs back to Codex, and continues through local and semantic verification again.
16. Watches for review changes, merge conflicts, base drift, and staleness.
17. Notifies the user when the pull request is ready, or earlier if a real decision is required.

## 6. Explicit non-goals

The first version will not provide:

- multiple users, organizations, roles, or permissions;
- a replacement issue tracker;
- agent personas or a simulated team;
- a general workflow/DAG builder;
- Kubernetes, remote workers, or hosted execution;
- an abstraction over every coding agent;
- automatic merging into protected branches;
- generalized multi-repository atomic changes;
- an embedded GitHub clone of reviews, diffs, and every Actions screen;
- a chat interface intended to replace the Codex desktop app for ordinary ad hoc work.

The proof of concept observes review state and can route concrete requested changes back to Codex, but it does not attempt to replace human code review or infer intent from every free-form discussion comment.

## 7. Product surface

Omakase has two clients over one headless core: a CLI used to prove and operate the full workflow, and a macOS Electron application that provides the everyday interface. Both display the same durable state and invoke the same core commands.

### Work

A compact list grouped by state:

- Needs attention
- Running
- Waiting on CI
- Ready
- Recently completed

Each row shows the task, scope, current phase, most recent meaningful event, next scheduled action, and whether the user is needed.

### New task

Inputs:

- scope;
- task description or issue URL;
- optional completion-policy override;
- optional base-branch override.

Advanced agent and git settings remain collapsed.

### Run detail

Displays:

- current phase, disposition, and next action;
- Codex's latest message and live activity;
- worktree and branch;
- local validation attempts;
- pull request and CI checks;
- task-completion evidence and repair-integrity warnings;
- a concise event history;
- pending question or policy decision, if any;
- controls for pause, resume, send guidance, open worktree, open pull request, and cancel.

The event history is not a second issue-comment system. User guidance is sent directly to the associated Codex thread.

### Scopes and projects

Scopes configure local roots, repository discovery, shared policy, and cleanup defaults. Each discovered repository has a reviewable project profile showing bootstrap, validation, resources, GitHub behavior, trust state, provenance, and the last accepted profile diff.

## 8. Run lifecycle

Run phase and run disposition are persisted separately. This prevents pause or attention handling from overwriting the work Omakase was doing.

Phases are:

```text
intake
preparing
bootstrapping
implementing
recording_evidence
validating_local
repairing_local
verifying_semantic
repairing_semantic
committing
publishing
waiting_for_ci
repairing_ci
responding_to_review
resolving_base_drift
ready
waiting_for_merge
completed
```

Dispositions are:

```text
queued
active
paused
needs_attention
terminal
```

A disposition records why it applies and what event can release it. Pausing a run that already needs attention preserves both the unresolved attention item and the current phase; resuming does not imply that the question was answered.

Important transition rules:

- Intake runs read-only and creates no worktree until it reports `ready`.
- Implementation completion moves through completion-record, local-validation, and independent semantic-verification phases before commit or publication.
- An implementation task with no meaningful diff needs attention unless its no-change outcome is explicitly accepted.
- A local, semantic, or CI failure starts another turn on the same implementation thread and re-enters all required gates afterward.
- Actionable pull-request review feedback returns to the implementation thread; general discussion remains visible without becoming an automatic coding instruction.
- Base drift or conflicts follow project policy, but the proof of concept never force-pushes an automatic rebase.
- Exhausting a configured repair loop changes disposition to `needs_attention`, not silently to terminal failure.
- The `completed` phase requires the evidence defined by the run's completion policy.
- Every phase or disposition change is written transactionally with the event that caused it and any next scheduled job.

## 9. Technical architecture

### Technology

- TypeScript for the core, CLI, and desktop application
- SQLite for durable local state
- Zod schemas at process, protocol, and persisted-payload boundaries
- Node child processes for Codex, git, repository validation, and GitHub CLI commands
- A user-level macOS LaunchAgent for the packaged background core
- Electron, Svelte 5, Vite, and Electron Forge for the later desktop client

The core and CLI are built before Electron. This keeps native packaging, signing, and UI work off the critical path for proving worktree isolation, repair loops, and CI follow-up.

### Process boundaries

#### Omakase core

A single headless process owns all privileged and durable behavior:

- SQLite;
- scheduler;
- Codex App Server subprocess;
- git and worktree operations;
- GitHub CLI operations;
- validation subprocesses;
- notifications;
- lifecycle recovery;
- filesystem access.

In development it runs in the foreground. In the packaged application it runs as an unprivileged per-user LaunchAgent. There is one authoritative core process per macOS user.

#### Local client protocol

The core exposes a versioned API over a user-owned Unix domain socket under Omakase's application-support directory. The socket and parent directory are accessible only to the current user. Requests are explicit commands; events are a subscribable stream. The protocol must be usable by both the CLI and Electron.

#### CLI

The `omakase` CLI is a complete operational client, not a debug-only backdoor. Through Milestone 3 it is the primary interface for creating, inspecting, pausing, resuming, answering, and canceling runs.

#### Electron application

The Electron main process connects to the core rather than owning orchestration state. Its preload bridge exposes a narrow typed API, and the Svelte renderer contains no durable workflow logic. Quitting Electron does not stop the core or active runs. Stopping the core is a separate, explicit command.

### Internal modules

```text
core/
  agent/
    AgentRuntime.ts
    CodexRuntime.ts
    AppServerClient.ts
    LivenessMonitor.ts
  projects/
    ProjectProfiler.ts
    ProfileResolver.ts
  orchestration/
    RunCoordinator.ts
    RunStateMachine.ts
    RecoveryService.ts
  git/
    GitClient.ts
    WorktreeManager.ts
    RepositoryDiscovery.ts
  github/
    GitHubClient.ts
    PullRequestMonitor.ts
    ActionsMonitor.ts
  validation/
    ValidationRunner.ts
    FailureSummarizer.ts
    SemanticVerifier.ts
    IntegrityChecker.ts
  resources/
    ResourceLeaseManager.ts
  scheduling/
    Scheduler.ts
    JobHandlers.ts
  policy/
    PolicyEngine.ts
  persistence/
    Database.ts
    repositories/
  notifications/
    NotificationService.ts
  protocol/
    Server.ts
    handlers.ts
cli/
  commands/
desktop/
  main/
  preload/
  renderer/
shared/
  contracts/
  types/
```

## 10. Agent runtime boundary

This section is provisional until Milestone 0 has exercised the installed App Server version. The spike records actual request, event, interruption, resume, and failure behavior; this section is then rewritten to describe observed behavior rather than preserving assumptions.

The orchestration layer depends on a small interface rather than directly on JSON-RPC:

```ts
interface AgentRuntime {
  start(input: StartAgentInput): Promise<AgentSession>;
  resume(sessionId: string): Promise<AgentSession>;
  runTurn(sessionId: string, input: AgentTurnInput): Promise<AgentTurn>;
  getStatus(sessionId: string): Promise<AgentSessionStatus>;
  respondToRequest(requestId: string, response: UserResponse): Promise<void>;
  interrupt(sessionId: string): Promise<void>;
  subscribe(sessionId: string, listener: AgentEventListener): () => void;
}
```

The boundary exists primarily as a test seam: orchestration tests can use a deterministic fake without starting Codex. `CodexRuntime` is the only production implementation required for the proof of concept. A future `PiRuntime` is possible, but it is not a design requirement.

### Codex integration

Omakase starts a local `codex app-server` process and communicates over its JSON-RPC protocol. It uses:

- `thread/start` for a new run;
- `thread/resume` after restart or when continuing a run;
- `turn/start` for the initial task and each repair/follow-up turn;
- streamed item and turn events for progress;
- `contextCompaction` events as observable Codex activity;
- thread reads and process health for reconciliation and liveness probes;
- server-initiated user-input requests;
- the Codex thread ID as the durable agent-session identifier.

The intake turn starts in the source repository with a read-only sandbox, approval policy `never`, and command network access disabled. It may inspect the repository and ask a blocking question, but it cannot edit files or perform setup. Once intake reports `ready`, the same implementation thread continues in the isolated worktree.

Each implementation and repair turn uses:

- `cwd` set to the isolated worktree;
- the project profile's configured model or the user's Codex default;
- sandbox mode `workspaceWrite`;
- approval policy `never`;
- command network access disabled;
- a service name identifying Omakase.

The Codex sandbox is the primary implementation boundary. With approvals disabled, Codex makes a best effort within that boundary instead of asking Omakase to classify arbitrary shell strings. Operations requiring broader filesystem or command-network authority fail inside the turn; Codex may still make an ordinary user-input request when it needs judgment or missing information. Full-access sandbox modes are outside the proof of concept.

The official Codex sandbox protects `.git` and a worktree's resolved git directory as read-only even within a writable root. Codex therefore edits and tests working-tree files, while Omakase owns every Git metadata mutation: branch and worktree creation, commits, merges, pushes, and cleanup. Milestone 0 verifies these properties on the installed version rather than relying only on documentation.

Omakase uses the user's existing local Codex authentication and configuration. It does not copy, inspect, or store Codex credentials.

On startup, Omakase starts App Server, reloads unfinished runs, resumes their threads, reconciles their external state, and restores their scheduled jobs.

### Liveness

Silence is a reason to probe, not proof that Codex is stuck. Omakase records the last App Server event and tracked child-process activity. After a configurable quiet interval it checks App Server process health, reads the thread or turn state when supported, and records the result. If the turn is still active, it continues waiting and schedules another probe. A dead, unreachable, or contradictory session enters recovery; only unrecoverable ambiguity becomes attention. Quiet intervals do not consume a time budget and do not interrupt a healthy long-running turn.

Omakase records the Codex CLI version and App Server initialization result on every core start. The initial development machine currently has `codex-cli 0.150.1`; this is a test baseline, not yet a promised minimum. Milestone 0 defines the minimum tested version and compatibility range. Omakase refuses to start new runs outside that range, while existing runs remain visible with an actionable compatibility error. Experimental App Server methods are not used in the core completion loop unless explicitly version-gated.

Codex owns context-window management and automatic history compaction using its model and user configuration. Omakase observes `contextCompaction` events but does not set a separate threshold or request manual compaction. A thread that cannot resume is an exceptional recovery case and becomes an attention item in the proof of concept; automatic replacement-thread handoffs are deferred until real failures justify them.

References: <https://learn.chatgpt.com/docs/app-server> and <https://learn.chatgpt.com/docs/agent-approvals-security>

## 11. Worktree and git behavior

### Location

The default managed worktree root is:

```text
~/Code/.omakase/worktrees/<repository>/<task-slug>-<short-id>
```

It is configurable per scope. Managed worktrees are kept separate from primary checkouts and are unmistakably owned by Omakase.

### Creation

For each run, Omakase:

1. Resolves the repository's configured remote and base branch.
2. Runs `git fetch` without modifying the primary checkout.
3. Creates `omakase/<task-slug>-<short-id>` from the fetched base ref.
4. Creates a worktree for that branch under the managed root.
5. Records repository identity, base SHA, branch, and absolute worktree path.
6. Snapshots the effective project profile and checksums protected control-plane paths.
7. Bootstraps configured local-only files and dependencies.
8. Starts Codex only after bootstrap succeeds.

The primary checkout may be dirty or on another branch; Omakase does not change it.

### Bootstrap

Fresh worktrees do not contain gitignored files or installed dependencies. Each project profile therefore defines an explicit bootstrap manifest containing:

- local-only paths to copy from a configured source checkout;
- local-only paths to symlink when sharing is intentional and safe;
- optional environment-file mappings;
- an optional setup command and timeout;
- paths that must exist before Codex starts.

Source and destination paths are resolved and checked against the configured repository and worktree roots. Omakase never guesses which secrets or ignored files to copy. It records metadata and checksums, not secret contents.

Files or environment values bootstrapped into a worktree are available to processes in that worktree and may be accessible to Codex tools. Omakase labels sensitive mappings and requires explicit user-owned profile configuration for them; repository-owned `.omakase.yml` cannot nominate new secret sources. Prefer narrowly scoped development credentials over production credentials.

A bootstrap failure creates an attention item categorized as environment setup. It is not sent to Codex as an implementation failure and does not consume a repair attempt. The bootstrap command is pinned from the configuration snapshot taken at run creation.

### Resource concurrency

A project profile declares named local resources with capacities, such as a repository-wide execution lease, database namespace, port range, container name, or shared cache. Each bootstrap, agent, and validation step declares the leases it needs. Omakase acquires them before the step and releases them while the run is paused, awaiting attention, or waiting on external systems.

The proof of concept supports the conservative `repository_execution` lease with capacity one. The generic schema leaves room for narrower resources, but Omakase will not invent database offsets or port namespaces without project-specific configuration. Runs for different repositories may proceed concurrently. Sushi's initial lease choice and shared-database rationale are fixture details in Appendix A; a narrower Sushi resource profile is a measured follow-up, not a prerequisite for the first loop.

### Cleanup

A worktree may be automatically removed only when all of the following are true:

- its run reached the configured terminal disposition;
- git reports no uncommitted or untracked work that policy says to preserve;
- its branch has been pushed or intentionally abandoned;
- its pull request is merged or the user explicitly requested cancellation and cleanup;
- the recorded path still belongs to the expected repository and run.

Otherwise Omakase retains it and explains why. Cleanup uses git-aware worktree removal and pruning; it never performs a broad recursive deletion based on an unresolved path.

## 12. Repository conventions and configuration

Configuration has three layers:

1. User-owned scope configuration in Omakase's database: roots, repository selection, global safety policy, defaults, and secret-source authority.
2. User-owned profile templates and a project profile for each configured repository: reusable defaults plus repository-specific operational knowledge such as bootstrap, validation, resources, CI, and completion policy.
3. Optional repository-owned `.omakase.yml`: shareable, non-secret defaults that may be committed with the codebase.

The resolved project profile is the shared interface between repository discovery and orchestration. Core code consumes the schema; it does not branch on Rails, Ruby, or Sushi. A profile can describe multiple validation suites, distinct commands for targeted and authoritative checks, external CI checks, workflow dispatch rules, and the resource leases required by each step. Templates are declarative profile fragments, not executable plugins; merge precedence is deterministic and the UI shows the fully resolved diff before trust.

### LLM-assisted project discovery

For an unconfigured repository, Omakase starts a fresh read-only Codex session with a constrained profiling request. It asks Codex to inspect, not change, the repository and propose:

- repository identity, remote, and base branch;
- applicable instruction files and pull-request templates;
- language, framework, and toolchain observations;
- bootstrap steps and required local-only paths;
- fast targeted checks and authoritative validation suites;
- CI checks to observe and workflows that require dispatch;
- likely shared resources such as databases, ports, or containers;
- trusted validator and policy paths that must not redefine themselves during repair;
- uncertainty, alternatives, and items requiring user confirmation.

The proposal is data, not authority. Omakase schema-validates it, rejects paths outside the repository or unsupported operations, and presents the effective diff for review. Secret sources, executable commands, remote writes, and broadened resource or network authority always require user-owned confirmation. The accepted profile records its provenance: generated, repository-provided, user-edited, and last trusted checksum.

Re-profiling is explicit. A changed repository-owned file may produce a suggested profile update, but it never mutates an active run or silently becomes trusted. This permits useful shared Rails discovery while keeping the execution model deterministic.

### Generic profile shape

```yaml
version: 1
extends: []

git:
  remote: origin
  base_branch: main
  branch_prefix: omakase/

bootstrap:
  copy_if_present: []
  symlink: []
  required_paths: []
  steps:
    - name: Project setup
      command: ./script/setup
      timeout_minutes: 15
      resources: [repository_execution]

resources:
  repository_execution:
    capacity: 1

validation:
  targeted: []
  authoritative:
    - name: Full local validation
      command: ./script/ci
      timeout_minutes: 30
      resources: [repository_execution]

github:
  create_pull_request: true
  required_checks: []
  workflow_dispatches: []
  completion: ready_to_merge

integrity:
  protected_control_paths:
    - .github/workflows/**
    - .omakase.yml
    - script/ci
  detectors:
    - skipped_test_added
    - test_file_deleted
    - validator_command_changed

repair:
  max_local_attempts: 3
  max_semantic_attempts: 2
  max_ci_attempts: 3

retention:
  event_days: 90
  full_log_days: 30

cleanup:
  after_merge: true
```

Test directories are not protected wholesale. Tests are ordinary implementation code. Framework-specific integrity detectors—for example, an RSpec-focused detector for newly skipped examples or removed assertions—are optional profile capabilities and must report concrete diffs rather than claiming general semantic safety.

Repository configuration is executable input because it can name commands. Repository-owned configuration supplies candidate defaults; the accepted user-owned project profile may override them; scope policy is the final authority ceiling. Omakase shows the resolved result before trust and requires renewed trust for later changes to executable or authoritative fields. Repository configuration cannot broaden user-owned filesystem, secret, network, Git, or GitHub authority.

The fully resolved profile is snapshotted onto each run before intake and bootstrap. Later edits do not change an in-flight run. Omakase always executes the pinned validators even if the implementation changes their source paths.

Omakase passes through normal Codex instruction discovery and records the instruction sources reported by App Server. Repository pull-request templates are preserved when Omakase creates a pull request.

## 13. Validation and self-correction loop

This section is provisional until the App Server spike and the first real repair runs establish which completion records, structured verifier outputs, and failure signals are reliable. Omakase records observed data so these rules can be simplified or corrected after the spike.

### Local validation

Validation commands run as ordinary child processes inside the worktree. Omakase captures:

- command and working directory;
- start and finish time;
- exit status and termination reason;
- bounded stdout and stderr;
- a path to the complete local log.

On failure, Omakase sends Codex:

- the failed command;
- exit status;
- the most useful bounded portion of the output;
- the complete log path;
- current git diff summary;
- the remaining automatic repair attempts for that loop;
- a direct instruction to diagnose, fix, and rerun the relevant checks.

Codex may run its own tests during the repair turn. Omakase still runs the configured authoritative validation after the turn ends.

### Task-completion evidence

Before local validation, Codex must provide a concise completion record containing:

- what changed;
- how each material change addresses the original task;
- what it tested;
- known limitations or follow-up work.

For an implementation task, Omakase also requires a tracked diff from the recorded base SHA. A zero-diff result becomes an attention item with Codex's explanation; it cannot proceed to `ready` automatically. Tasks explicitly categorized as investigation or already-fixed verification may use a no-change completion policy.

This is evidence, not a proof of semantic correctness. The implementing thread's account is retained for Omakase and the user, but it is deliberately withheld from the independent verifier's first verdict and is not itself the semantic gate.

The completion record is requested as part of the ordinary implementation turn's final response. If it is missing, Omakase makes at most one explicit follow-up request; a second missing or unusable record becomes an attention item. This is self-report from the implementing Codex context, intended to make human review faster rather than to detect a dishonest agent.

### Independent semantic verification

After authoritative local validation passes, Omakase starts a new Codex thread with a read-only sandbox, approval policy `never`, and command network access disabled. The verifier receives:

- the original task and accepted intake clarifications;
- applicable repository instructions;
- the recorded base SHA and complete base-to-working-tree diff.

Local validation results and the implementation completion record remain separate evidence visible to Omakase and the user; they are deliberately withheld from the first semantic verdict so green checks and implementation self-justification do not anchor the verifier.

It does not receive the implementation or repair conversation. It may inspect the read-only worktree and returns a structured verdict: `pass`, `needs_changes`, or `uncertain`, with concrete findings tied to the task or diff.

`pass` permits Omakase to commit and publish. `needs_changes` is sent to the original implementation thread, after which local validation and independent verification run again. A materially repeated verifier rejection or the configured semantic-repair limit creates attention. `uncertain` creates attention immediately because uncertainty is not evidence of completion. The verifier is an independent perspective, not a formal proof; its verdict and rationale remain visible to the user.

### Repair integrity

Omakase records the working-tree state and changed-path set before and after every repair turn. It compares repair changes with the pinned profile and protected control-plane paths from run start.

A repair turn becomes `needs_attention` before its result can count as successful when it:

- changes a protected control-plane path not explicitly allowed by the run's pinned user-owned profile;
- introduces a deterministic marker enabled by the project profile, such as a newly skipped test, deleted test file, disabled check, retry wrapper, or changed timeout;
- changes CI, `.omakase.yml`, bootstrap behavior, or the command Omakase uses as authoritative validation;
- triggers a project-specific integrity detector with a concrete before/after finding;
- introduces an unexplained generated or golden-file rewrite when that project profile marks such files for review.

Test edits are allowed during implementation and repair. Omakase does not infer cheating merely because a test changed, and generic code does not claim to detect vacuous behavior in application code. Protected control-plane changes are not universally forbidden during the initial implementation turn, but they cannot become the active rules for that run. A task whose purpose is to repair CI or validation may receive a narrow user-owned allowlist. The important rule is that a repair loop cannot silently redefine success after seeing a failure.

Omakase always executes the validation command and configuration captured at run start. If a legitimate task changes that command, the current run uses the pinned version and asks the user whether the new configuration should apply to a subsequent verification run.

### Failure repetition

The proof of concept deliberately uses a crude failure signature rather than claiming general failure normalization. The signature consists of the validation command, exit code, and the first identified failing step, test, or check after removing obvious timestamps and absolute worktree paths.

If the same signature occurs twice with no tracked tree change between attempts, Omakase stops. If the tree changed but the failure remains, the configured per-loop repair limit governs. Flake classification and semantic comparison are deferred until real run data justifies them.

### Loop safeguards

Omakase stops automatic repair when:

- the configured automatic repair limit is exhausted;
- the same proof-of-concept failure signature repeats twice without a tracked tree change;
- repair-integrity policy detects a protected or suspicious change;
- Codex requests user input;
- the required action violates policy;
- the worktree becomes inconsistent or unsafe;
- App Server or a required external dependency remains unavailable after bounded retries.

It then creates one attention item containing the relevant context and recommended choices.

### Supervisor loop guards

Codex owns the execution, context management, and duration of each agent turn. Omakase does not impose a global turn, token, cost, active-time, or wall-clock budget on a run.

Omakase limits only loops and processes it creates:

- maximum automatic local-repair attempts;
- maximum automatic semantic-verification repair attempts;
- maximum automatic CI-repair attempts;
- the repeated-failure stop described above;
- per-command timeouts for bootstrap and validation child processes;
- at most one follow-up turn for a missing completion record.

Review responses selected by the user are not charged against an artificial turn allowance. Queueing, CI, review, merge, sleep, and attention waits are governed by reconciliation and staleness reminders rather than time budgets. The run detail may show elapsed time, agent turns, repair counts, and available usage information for observation, not enforcement.

## 14. GitHub and CI

The first integration uses the authenticated `gh` CLI rather than a GitHub App or webhook server. This keeps setup local and reuses the user's existing GitHub authentication.

Omakase records the repository, pull-request number, head SHA, workflow run IDs, and check-suite conclusions. It never associates a CI result using only a branch name when a head SHA is available.

The ambient `gh` credential may have authority far beyond one run. Branch and repository restrictions are enforced by Omakase's own typed GitHub operations and target checks, not by a narrowly scoped token. Omakase does not expose a general authenticated `gh` shell endpoint to orchestration code. Codex edits and tests working-tree files; after the evidence gates pass, the Omakase core owns the local commit, push, pull-request mutations, workflow dispatch, and other GitHub writes. Codex command network access remains disabled.

### Workflow dispatch and correlation

A project profile distinguishes required checks that appear automatically from workflows Omakase must explicitly dispatch. When a dispatch accepts a unique run token, Omakase uses it. When it does not, correlation uses immutable and scoped evidence rather than branch name alone.

For each workflow and head SHA, Omakase:

1. Records a durable dispatch intent before contacting GitHub.
2. Ensures that only one local dispatch attempt for that workflow/SHA is active.
3. Dispatches against the unique Omakase task branch.
4. Polls for a run matching repository, workflow identity, event type, task branch, head SHA, optional run token, and a creation time at or after the recorded intent.
5. Stores the workflow-run ID as soon as one unambiguous match appears.

If multiple candidates match, or the core crashes in the uncertain interval after GitHub accepted dispatch but before Omakase recorded success, Omakase reconciles before retrying. Ambiguity becomes an attention item rather than an unbounded duplicate dispatch. Project-specific workflow behavior belongs in the profile; Sushi's initial correlation details are in Appendix A.

### Polling

While CI is incomplete, Omakase schedules durable follow-up jobs with bounded exponential backoff. A typical sequence is:

```text
30 seconds -> 1 minute -> 2 minutes -> 4 minutes -> every 5 minutes
```

Polling immediately stops when all required checks reach a terminal state.

On failure, Omakase retrieves a bounded failure summary and relevant logs, changes phase to `repairing_ci`, and starts a new turn on the existing implementation thread. After local and semantic verification pass, Omakase creates a new commit and pushes it; monitoring then moves to the new head SHA.

### Review and base drift

For an open pull request, Omakase periodically reconciles:

- review decision and concrete change requests;
- unresolved review threads when available through the chosen GitHub interface;
- base-branch SHA;
- mergeability and conflicts;
- whether checks are stale for the current head SHA.

Concrete requested changes move the phase to `responding_to_review` and are sent to the existing Codex thread with links and bounded context. General discussion, approvals, and ambiguous product feedback remain visible but are not automatically treated as coding instructions.

When the base branch moves, Omakase re-evaluates mergeability. The proof of concept may ask Codex to resolve a non-rewriting merge from the latest base when scope policy permits. It never automatically rebases and force-pushes. Conflicts, repeated drift, or an uncertain merge policy become attention items.

Runs waiting on a person or merge receive a configurable staleness check. Omakase re-notifies only after a meaningful state change or a configured reminder interval, and records the next reminder visibly.

GitHub writes allowed by scope policy may include:

- pushing only the run's task branch;
- creating or updating its pull request;
- dispatching configured workflows.

Merging, closing unrelated issues, modifying repository settings, and deleting remote branches require separate policy and are disabled initially.

## 15. Scheduler and background behavior

Omakase uses a durable application scheduler, not macOS cron. Cron has poor access to the interactive user's environment, credentials, application state, and structured retry context.

Scheduled jobs are SQLite records containing:

- job type;
- run ID;
- due time;
- payload;
- attempt count;
- state (`queued` or `running`);
- last error.

The scheduler wakes on the next due time and also performs a periodic reconciliation sweep. There is one authoritative core process, so distributed leases are unnecessary. On startup, jobs left `running` are reset to `queued` and their handlers reconcile external state before attempting any non-idempotent operation.

The packaged core is installed as an unprivileged user LaunchAgent and starts after login. It survives Electron window closure and Electron quit. The Electron application may expose core status and an explicit "Stop after current safe point" action, but ordinary application lifecycle does not abandon work.

Laptop sleep pauses local execution naturally. On wake or after a macOS restart, the core immediately reconciles overdue jobs, Codex threads, worktrees, pull requests, and CI before deciding what to do next. The first version installs no privileged daemon and performs no work before user login.

## 16. Policy and interruption model

This section is provisional until Milestone 0 verifies the sandbox boundary and real project setup reveals which operations belong in trusted profiles. The implementation favors a small number of explicit authority boundaries over a command-string approval engine.

The purpose of policy is to eliminate routine "confirm yes" interruptions without granting invisible, unlimited authority.

A trusted scope and project profile can pre-authorize Omakase itself to perform:

- exact configured bootstrap and validation commands inside managed worktrees;
- configured local-only file mappings;
- dependency installation performed as a profile-owned bootstrap step;
- named resource leases;
- pushes to Omakase-created task branches;
- pull-request creation and updates;
- dispatching and reading configured CI workflows.

Pre-authorization does not replace the Codex sandbox. Implementation threads run with `workspaceWrite`, approval policy `never`, and command network access disabled. Omakase does not parse or approve model-generated shell strings. A trusted project-profile command is executed only by the Omakase core as that exact snapshotted step, with a fixed working directory, bounded environment, timeout, log, and declared resource leases.

Git and GitHub authority is deliberately split: Codex may inspect and modify working-tree files, while Omakase performs Git metadata changes and configured remote writes through typed operations after independently checking repository, remote, branch, and head SHA. A failed Codex attempt to exceed its sandbox is recorded as a tool failure; if progress truly requires broader authority, Codex must explain the need through user input rather than receiving an invisible escalation.

The following require attention by default:

- writes outside a managed worktree;
- destructive cleanup that fails identity or cleanliness checks;
- force pushes;
- changes to repository or organization settings;
- merges;
- secrets or authentication changes;
- actions targeting a branch, pull request, or repository not owned by the run;
- an untrusted or materially changed project profile;
- protected control-plane changes introduced during repair;
- ambiguous product decisions requested by Codex.

Omakase does not manufacture an interactive approval path for an implementation thread configured with `never`. App Server user-input requests, project-profile trust decisions, integrity findings, and Omakase-owned privileged actions that exceed policy become durable attention items with enough detail for the user to decide.

## 17. Notifications

Omakase sends macOS notifications for:

- a question or policy decision requiring the user;
- ambiguous review feedback, a merge conflict, or stale work requiring a decision;
- a run that is ready to merge;
- a terminal failure after recovery is exhausted;
- an authentication or configuration problem preventing progress.

It does not notify for ordinary tool calls, successful polling, each validation attempt, or routine state changes.

Clicking a notification opens the relevant run and focuses the exact attention item. A notification must never be the only persisted representation of required action.

## 18. Persistence model

Initial SQLite entities:

### `scopes`

Name, roots, repository-selection rules, worktree root, default policies, and timestamps.

### `repositories`

Scope association, canonical local path, git common directory identity, remote, base branch, and discovered metadata.

### `project_profiles`

Repository association, schema version, resolved profile, provenance, trust state, source checksums, accepted time, and superseded profile. Secret contents are excluded.

### `profile_templates`

User-owned reusable profile fragments, schema version, provenance, trust state, and revision history. Runs store only the resolved snapshot, so later template edits do not change active work.

### `tasks`

User intent, source type, source identifier/URL, title, and scope.

### `runs`

Task association, phase, disposition, disposition reason, Codex implementation and verifier thread IDs, observed attempt/turn counters, completion policy, current head SHA, Codex CLI version, timestamps, and terminal reason.

### `worktrees`

Run, repository, path, branch, base SHA, creation status, cleanup status, and last verified identity.

### `external_links`

Run association plus typed identifiers for pull requests, GitHub issues, Shortcut stories, and future sources.

### `validation_attempts`

Run, kind, command, status, timing, bounded output, complete log path, normalized failure signature, and head SHA.

### `configuration_snapshots`

Run, resolved scope and project profile, trusted source checksums, protected-control-path checksums, bootstrap manifest, and creation time. Secret file contents are never included.

### `agent_turns`

Run, Codex thread and turn IDs, purpose, start/end working-tree identity, changed paths, timing, last event time, status, available usage data, and repair-integrity result.

### `semantic_verifications`

Run, verifier thread and turn IDs, input evidence hashes, structured verdict, findings, timing, and relationship to any repair turn.

### `resource_leases`

Named project resource, capacity slot, owning run and step, acquisition and release times, and recovery status.

### `jobs`

Durable scheduled work, due time, state, attempts, uniqueness key, and last error.

### `events`

Append-only meaningful run events used for recovery, debugging, and the visible activity history.

### `attention_items`

Run, category, prompt, structured choices, source request ID, status, and resolution.

Secrets and copied Codex/GitHub tokens are explicitly excluded from the database.

### Retention

Full validation and CI logs are retained for a configurable short period, defaulting to 30 days. Structured run records and meaningful events default to 90 days. Successful polling events and streamed token deltas are aggregated rather than retained indefinitely. Worktree cleanup and data retention are separate: deleting an old log must never delete source work.

## 19. Crash recovery and reconciliation

At launch, Omakase does not blindly continue from the last stored state. It reconciles:

1. Whether each recorded worktree still exists and has the expected git identity.
2. Whether the recorded branch and head SHA match git.
3. Whether the run's pinned scope and project profile and bootstrap requirements remain available.
4. Whether the installed Codex CLI is compatible and its thread can be resumed.
5. Whether an expected child process survived; normally it will not survive core-process exit.
6. Whether a pull request exists and what its current head SHA, review decision, base SHA, and merge state are.
7. Whether CI is queued, running, failed, stale, or complete for the recorded head SHA.
8. Whether scheduled jobs are overdue or were left in `running` state.
9. Whether an attention item is due for a configured reminder.
10. The last App Server event, recorded turn status, and any liveness probes.

The coordinator then derives the safe next action. Uncertain or contradictory state produces an attention item instead of destructive repair.

### Interrupted implementation turns

The managed worktree is the durable container for partial edits. Omakase does not automatically commit or stash an interrupted tree. Before recovery it records `git status`, a binary-capable diff, staged-state metadata, and an untracked-file manifest, while leaving the files in place.

If App Server reports the turn still active, Omakase reattaches and waits. If the process died or the turn is terminal without a usable result, Omakase resumes the implementation thread and starts one recovery turn describing the observed partial state and asking Codex to inspect before continuing. It does not blindly replay the original turn. If session status is contradictory or the worktree identity changed, the run needs attention. Omakase creates a commit only after the normal validation and independent-verification gates pass.

## 20. Integrations after the proof of concept

### GitHub issues

A GitHub issue can populate a task and remain linked for context. Omakase should not become the canonical issue tracker. Status derives from the run and pull request; closing or commenting on issues is a separate opt-in write policy.

### Shortcut through Grim

Shortcut support should be an adapter that reads story context through Wistia's Grim MCP integration and links the source story to a run. Because Grim writes may be policy-blocked, the first adapter should assume read-only context and treat external status updates as optional, explicit operations.

### Multi-repository scopes

A later run may own a bundle of worktrees, one per affected repository, under a common run directory. This requires explicit semantics for base refs, validation order, cross-repository dependencies, pull requests, and partial failure. It should not be approximated by letting Codex edit arbitrary primary checkouts.

### Alternative agent runtimes

The `AgentRuntime` boundary permits a later Pi-backed implementation. It is intentionally not part of the first product because it would introduce another agent harness and require additional permission controls before proving the core Omakase loop.

## 21. Implementation plan

### Milestone 0: App Server spike

Build a small TypeScript executable that:

- starts `codex app-server`;
- initializes the protocol;
- starts a read-only intake thread in Sushi and accepts either a structured `ready` result or a user-input question;
- continues an implementation turn in a temporary Sushi worktree;
- streams agent messages and tool events;
- verifies `workspaceWrite`, approval policy `never`, and command network disabled;
- positively verifies that Codex can edit and run local commands inside the worktree;
- negatively verifies that Codex cannot write outside the worktree, mutate `.git` or its resolved worktree git directory, reach the command network, or push through ambient Git/SSH credentials;
- records quiet-stream behavior and probes turn/process status without treating silence alone as failure;
- records and checks the installed Codex CLI version;
- persists the thread ID;
- stops and resumes that thread in a new process;
- interrupts one turn after a partial edit and records what resumption actually preserves.

Exit criterion: Codex can make a harmless working-tree change, cannot cross the tested sandbox boundaries, and the spike can reconcile and resume the same thread after restart. Sections 10, 13, and 16 are then rewritten if observed App Server behavior differs from this provisional design.

### Milestone 1: Headless core, CLI, and durable runs

- SQLite migrations
- versioned local client protocol
- usable `omakase` CLI
- generic project-profile schema and trust flow
- read-only Codex project discovery and reviewable Sushi profile proposal
- scope configuration for Sushi
- task creation
- read-only task intake
- worktree manager
- bootstrap manifest and setup handling
- named resource leases with the conservative repository lease implemented first
- pinned configuration snapshots
- `CodexRuntime`
- phase/disposition lifecycle model
- liveness probes and crash reconciliation, including partial working trees

Exit criterion: Omakase can propose and trust a Sushi profile, intake a task, bootstrap and complete a Codex turn in a managed worktree without touching the primary checkout, and safely recover a deliberately interrupted partial turn.

### Milestone 2: Local validation loop

- validation runner
- log storage and bounded output
- proof-of-concept failure signatures
- automatic repair turns
- repair-integrity checks and pinned validator behavior
- task-completion evidence
- fresh read-only semantic-verification threads
- semantic-verification repair routing
- per-loop repair limits, repeated-failure guards, and child-process timeouts
- attention items

Exit criterion: a deliberately failing Sushi task is returned to Codex, repaired, passes the pinned `bin/ci`, and receives a `pass` from a fresh read-only verifier. Ordinary spec repair succeeds without interruption, while an attempted validator or CI-policy weakening is stopped and surfaced.

### Milestone 3: GitHub completion loop

- authenticated `gh` integration
- safe branch push
- PR discovery/creation with template preservation
- workflow dispatch for Sushi
- ambiguous-dispatch reconciliation
- durable CI polling
- CI failure repair
- review-change routing
- base-drift and conflict detection
- merge observation

Exit criterion: Omakase carries a Sushi task from text to a green pull request, including at least one intentionally induced CI failure and repair.

### Milestone 4: Background operation and dogfood gate

- user-level LaunchAgent packaging
- native notifications
- pause/resume/cancel
- safe worktree cleanup
- retention cleanup
- resource-queue measurements and, only if the repository-wide lease is a demonstrated bottleneck, a Sushi profile spike for narrower database or port leases
- ten pre-registered real Sushi tasks with recorded outcome metrics and independent final-diff audits

Exit criterion: work survives client exit, sleep, and core restart; the user receives useful notifications; and ten real Sushi implementation tasks have been measured. The Electron client does not begin until the dogfood results justify it.

### Milestone 5: Electron client

- Electron/Svelte application shell
- Work, New Task, Run Detail, and Scopes views
- attention inbox
- native notification deep links
- core status and explicit stop controls
- packaging, signing, and update strategy

Exit criterion: the same workflows proven through the CLI can be completed through the macOS application without losing state when the UI quits or reloads.

### Milestone 6: Broader scopes and ticket sources

- repository discovery within a folder scope
- GitHub issue import
- Shortcut/Grim read adapter
- focused multi-root scopes
- design spike for multi-repository runs

## 22. Proof-of-concept acceptance criteria

The Sushi proof of concept succeeds when all of these are demonstrated:

- Starting a task always creates a new managed worktree from the configured remote base.
- An unconfigured repository can receive an LLM-proposed project profile, but no proposed executable command or secret mapping runs before the user trusts the effective profile.
- The generic profile schema represents Sushi's Rails setup, validation, CI, and shared resources without core code branching on Sushi or Rails.
- A read-only intake turn runs before worktree creation and proceeds without user interaction when no blocking clarification exists.
- The primary Sushi checkout remains untouched, even if it is dirty or on another branch.
- The worktree receives the explicitly configured local-only bootstrap files, including `config/master.key` when present, without persisting their contents in Omakase.
- A bootstrap failure becomes an environment attention item and never prompts Codex to "fix" repository code.
- A second Sushi run respects the profile's declared resource lease while another run holds it, but may proceed when the lease is released; a run in another repository can proceed independently.
- Codex runs inside the managed worktree and follows repository instructions.
- Codex uses `workspaceWrite`, approval policy `never`, and command network disabled. It can edit and test inside the worktree but cannot write outside it, modify Git metadata, reach the command network, or push.
- Omakase, not Codex, creates the validated local commit and performs typed remote writes.
- Quitting the CLI or Electron client does not stop the core; restarting the core preserves and resumes the task.
- A quiet agent stream triggers a health probe rather than an immediate interruption; a dead App Server or interrupted partial turn is reconciled without blindly replaying the task.
- The installed Codex CLI version is recorded, and an incompatible version fails clearly before a new task starts.
- The resolved scope and project profile and authoritative validator are pinned before implementation starts.
- Codex produces a completion-evidence statement connecting its diff to the task.
- An implementation task with no diff cannot silently advance to ready.
- The pinned `bin/ci` runs independently after Codex reports completion.
- A local validation failure is returned to the same Codex thread and repaired automatically.
- Ordinary spec changes during repair do not interrupt merely because they are tests; configured deterministic integrity findings remain visible.
- A repair that changes or weakens the pinned validator, CI policy, or another protected control path is stopped and surfaced.
- A fresh read-only Codex thread reviews the original task and final diff without implementation history, validation results, or completion self-report; rejection routes back to the implementation thread and uncertainty cannot advance to ready.
- Per-loop local, semantic, and CI repair limits, repeated-failure guards, and child-process timeouts prevent Omakase-created loops from running forever.
- The task branch is pushed without force.
- A pull request is created using the repository's template when one exists.
- The `CI` and `Engine` workflows are dispatched once and correlated to the correct workflow, branch, and head SHA; ambiguous correlation does not trigger repeated dispatches.
- A CI failure is returned to the same Codex thread and repaired automatically.
- A concrete requested review change can return to Codex and pass through validation again.
- Base drift and merge conflicts are detected without an automatic force push.
- Omakase notifies the user when the pull request is green and ready.
- Phase and disposition are persisted independently. Pausing a run is durable, schedules no new work, and does not erase an unresolved attention item or recovery phase.
- Omakase never merges without a separately enabled policy.
- Worktree cleanup refuses to remove uncertain or dirty work.
- Expired logs and high-volume events are pruned without deleting source work or active evidence.
- No Codex or GitHub credentials are copied into Omakase's database.

### Outcome gate

Before any of the ten runs begin, their task identifiers, original descriptions, and selection method are registered in the database from a real Sushi backlog. Replacing a task is recorded rather than silently changing the sample. For each task Omakase records:

- how many reached a green pull request without manual coding intervention;
- why each intervention was required;
- median and slowest wall-clock duration;
- median agent turns and repair attempts;
- available token or usage data and cost only when it can be measured honestly;
- minutes of human coding, review, clarification, and Omakase babysitting;
- false-positive interruptions and unattended time saved;
- semantic-verifier findings and the result of a separate final-diff audit against the original task;
- false-ready outcomes, unsafe repair attempts caught, cleanup failures, and whether merged work required a corrective follow-up within one week.

At least seven of ten tasks must reach a green pull request without manual coding intervention, with all ten independently audited, zero known false-ready outcomes after that audit, and zero unsafe cleanup or cross-worktree writes. This is a dogfood decision gate, not a statistical reliability estimate. Missing it sends the product back to the core loop instead of moving on to Electron polish.

## 23. Decisions intentionally deferred

- Final visual identity and icon
- Mac App Store distribution versus direct notarized download
- SQLite library selection after testing standalone core packaging
- Whether completed Codex threads should also appear in the Codex desktop sidebar
- Exact policy granularity for package-manager network access
- GitHub webhooks versus continued polling if a future always-on helper exists
- Whether mature project profiles can safely use narrower per-database or per-port resource namespaces
- Automatic merging
- Full semantics for tasks spanning multiple repositories

## 24. First engineering task

Do not begin with the full Electron interface.

Begin with Milestone 0 as a disposable but well-typed TypeScript spike. It resolves the highest-risk question: whether Omakase can reliably own the Codex App Server lifecycle, no-prompt sandbox boundary, event stream, liveness probes, thread persistence, and interrupted-turn recovery while the actual work occurs in an isolated, bootstrapped Sushi worktree.

Once that loop works, move the tested client behind `CodexRuntime` and build the headless core and CLI. Do not build the Electron shell until the local-validation and GitHub loops have survived the ten-task outcome gate.

## Appendix A: Sushi proof-of-concept profile

Sushi is Omakase's first project profile and acceptance fixture, not the product's ontology. The discovery flow should produce and explain a profile equivalent to the following candidate; the user still reviews it, and later explicit re-profiling may correct stale details.

```yaml
version: 1

git:
  remote: origin
  base_branch: main
  branch_prefix: omakase/

bootstrap:
  copy_if_present:
    - config/master.key
  required_paths: []
  steps:
    - name: Rails setup
      command: bin/setup --skip-server
      timeout_minutes: 15
      resources: [repository_execution]

resources:
  repository_execution:
    capacity: 1

validation:
  targeted: []
  authoritative:
    - name: Full local CI
      command: bin/ci
      timeout_minutes: 30
      resources: [repository_execution]

github:
  create_pull_request: true
  required_checks: []
  workflow_dispatches:
    - name: CI
    - name: Engine
  completion: ready_to_merge

integrity:
  protected_control_paths:
    - .github/workflows/**
    - .omakase.yml
    - bin/ci
    - config/ci.rb
  detectors:
    - skipped_test_added
    - test_file_deleted
    - validator_command_changed

repair:
  max_local_attempts: 3
  max_semantic_attempts: 2
  max_ci_attempts: 3

retention:
  event_days: 90
  full_log_days: 30

cleanup:
  after_merge: true
```

Fixture-specific facts:

- `config/master.key` is ignored and untracked in the source checkout, so it must be an explicitly user-authorized local-only mapping; its contents are never stored in Omakase's database.
- The initial conservative resource lease exists because Sushi worktrees can share fixed PostgreSQL test databases such as `sushi_test1` through `sushi_test4`. Namespacing those resources is a later measured optimization.
- `CI` and `Engine` currently require explicit dispatch and accept no Omakase nonce. Correlation therefore uses repository, workflow identity, event type, task branch, exact head SHA, and creation time after the durable dispatch intent. Ambiguity produces attention rather than duplicate dispatch.
- `bin/ci` is the authoritative local validation entry point. Its exact behavior is discovered and pinned rather than reproduced in Omakase core code.
