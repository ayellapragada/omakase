# Personal project profile

`.omakase.local.yml` is Omakase's personal project preferences and machine-local operational memory for one Git repository. It captures the small amount of setup and delivery knowledge that is repeatedly rediscovered in isolated worktrees. It must be globally ignored and never committed.

The profile supplements rather than replaces `AGENTS.md`, repository documentation, CI configuration, or user instructions. Those sources define shared project policy and take precedence. The profile is appropriate for explicit project workflow preferences, purpose-specific tool choices, machine-specific commands, local prerequisite paths, worktree caveats, and verified shortcuts. Missing optional `tools` and `preferences` fields in existing version 1 profiles behave as empty values.

## One profile across worktrees

Keep the file at the root of the primary checkout. A globally ignored file is not automatically present in linked worktrees, so resolve it through Git metadata rather than looking only in the current directory. From this skill directory, run:

```bash
profile_path="$(python3 scripts/profile_path.py --repo <checkout-or-worktree>)"
```

The resolver returns the first checkout reported by `git worktree list --porcelain`, which is the primary checkout. This gives every task worktree one shared profile that can improve over time.

## Generate when missing

When a repository has no profile and persistence is allowed by the task, Codex should create a minimal one without turning setup into an onboarding interview. Read-only work can use inferred context without creating a file; do not run bootstrap merely to populate a profile for an investigation. For delivery setup:

1. Before writing, verify that Git ignores the resolved path:

   ```bash
   git -C "$(dirname "$profile_path")" check-ignore -q -- "$profile_path"
   ```

   If this fails, stop without creating the profile and report that `.omakase.local.yml` must be added to the user's global Git excludes file.
2. Read active instructions, README setup guidance, runtime version files, CI workflows, and existing automation.
3. Inspect established repository entry points such as `bin/setup`, `script/bootstrap`, `package.json` scripts, and documented Make targets.
4. Start from `assets/omakase.local.example.yml`, retaining only evidence-backed fields.
5. Run the selected bootstrap or validation command in the isolated worktree.
6. Inspect `git status` and confirm bootstrap did not unexpectedly rewrite tracked files.
7. Keep the generated profile only after the relevant command succeeds cleanly, and tell the user what was learned.

Established repository entry points can be used without a redundant confirmation when they are safe and fall within the authorized coding task. Ask before writing novel shell setup, fetching secrets, modifying infrastructure, weakening verification, or doing anything destructive.

## Suggested schema

The schema is intentionally small and extensible:

- `version`: profile format version; currently `1`.
- `tools`: optional mapping from purpose to ordered tool preferences, required evidence and permitted fallbacks; see below.
- `preferences`: optional list of explicit standing workflow preferences for this project; these supplement personal defaults under higher-priority instructions.
- `bootstrap.steps`: ordered idempotent entries required to make a fresh worktree usable.
- `validation.quick`: focused or inexpensive checks used during implementation.
- `validation.full`: the local completion checks.
- `worktree.required_local_files`: paths that may need to be made available in a worktree; never include their contents.
- `worktree.notes`: verified machine-local caveats that do not fit another field.
- `ci.provider` and `ci.required_checks`: how remote completion is assessed.
- `publication.base_branch` and `publication.merge`: local publication defaults when repository policy does not already specify them.

Unknown fields should be ignored rather than treated as fatal so the profile can evolve without a migration ceremony.

Run `bootstrap.steps` sequentially and stop at the first failure. Bootstrap and validation entries share this shape:

- `runtime`: the tool family needed for the command; it is not a shell prefix.
- `run`: the repository command to execute.
- `env`: an optional mapping of non-secret environment variables required by that command.
- `needs`: an optional list of execution capabilities that must be obtained before running the command, such as `network`, `localhost`, or `browser`.

Apply `env` before the first attempt. Request the execution context named by `needs` before the first attempt, using the narrowest available permission for each capability. These fields describe how to execute the recorded repository command; they do not grant new authority for destructive operations, releases, merges, or unrelated external changes. Omit empty optional fields from established profiles. Do not duplicate structured step requirements in `worktree.notes`.

Align bootstrap steps with failure and retry boundaries when the repository provides evidence for doing so. If repository-supported phase-specific commands or flags expose dependency installation, database preparation, or generation as independently repeatable phases, record those phases as separate ordered steps. After repairing a failure, resume at the failed profile step rather than rerunning earlier successful expensive steps. Do not decompose a canonical entry point into invented shell setup; when the repository supports only one setup command and a failed mutation leaves state untrusted, rerun that clean command.

Make `validation.full` self-preparing. When a check consumes ignored generated artifacts, record the repository-supported generator as an earlier validation entry even if bootstrap also runs it. Mirror generators that CI or production builds run before the same checks. A clean Git status does not prove that ignored artifacts are current.

For an asdf-managed project, resolve only the executable needed by the current step:

- `runtime: ruby`: resolve the configured Ruby. Invoke repository Ruby binstubs with that Ruby. Invoke Bundler's executable through the same Ruby interpreter.
- `runtime: node`: resolve the configured Node, npm, or npx executable. Keep the repository's `node_modules/.bin` ahead of language-global executable directories for child processes.
- Do not wrap a Rails or other polyglot process tree in `asdf exec`. Language-global executables can share names with project-local tools and shadow them in descendants.

Treat mutation of one dependency tree as an exclusive operation. Do not overlap an installer with another installer or a test, build, or hook that consumes the same tree. A command that is merely quiet may still be working; retain its live session and confirm that it exited before retrying. If an install fails or is interrupted after mutation, treat the tree as untrusted and recover with the repository's clean deterministic install or bootstrap command rather than layering an incremental install over partial state.

Before a dependency installer mutates its tree, check known harness constraints that can be established locally. Confirm that package-manager cache and log directories are writable; if not, record a writable directory under the system temporary directory in the step's `env` mapping. Prefer a task-scoped cache; a repository-scoped cache is appropriate when the package manager supports concurrent access and the stable path is needed across worktrees. If the installer is known to require registry access unavailable in the sandbox, record `network` in `needs`. Combine known constraints into one first attempt.

Before an expensive validation command, inspect its profile notes and known constraints. If repository evidence or a verified prior run shows that it needs localhost sockets, browser processes, external services, or network access unavailable in the default sandbox, request the required execution context on the first run. Do not infer broader access from speculation or persist a one-off sandbox failure.

## Learning loop

Do not update the profile merely because a command failed. First classify the cause:

- Durable and reproducible: wrong runtime selection, a consistently required bootstrap step, a required local file path, or a stable validation command. Fix, rerun, then persist the learning.
- Stable harness constraint: a fixed command repeatably needs a specific environment value or execution capability. After a successful verification, record it on that command with `env` or `needs`; reserve `worktree.notes` for caveats that cannot be represented structurally.
- Dirty bootstrap: a setup command succeeds but rewrites a tracked lockfile or generated source. Prefer a repository-supported clean alternative and verify it leaves tracked files unchanged before persisting it.
- Transient: network outage, registry hiccup, temporary CI incident, one-time cache corruption, or a one-off sandbox denial. Recover if possible, but do not memorialize it.
- Unsafe or uncertain: secret acquisition, novel host mutation, infrastructure changes, or a speculative workaround. Ask for the smallest required decision before proceeding.

Keep the file concise. Delete stale instructions when repository automation makes them unnecessary.

## Project tools

Resolve a tool route per purpose needed by the task, not an inventory to invoke on every run. Precedence is current user instructions, applicable repository policy, explicit project profile choices, then personal defaults. Within a route, check `preferred` in order against available capabilities and project authorization. If none can serve the purpose, use a listed `fallback` only when it supplies appropriate evidence and complies with policy. An omitted route inherits personal defaults; an explicit empty route disables default service selection for that purpose and uses only locally available evidence until clarified.

Each purpose has an optional `preferred` list, `fallback` list and `required` boolean (default false). Purpose keys and tool names are descriptive, not guessed MCP action identifiers. The agent interprets this profile; there is no new tool router or plugin installer. Resolve actual tools through the sanctioned discovery mechanism. A route can describe an MCP service, CLI, repository entry point, browser, or local evidence source. Do not store credentials or executable setup for novel integrations.

For example, a work project might use:

```yaml
tools:
  issue_context:
    preferred: [the approved issue-tracker integration]
    fallback: [local issue notes]
    required: true
  runtime_evidence:
    preferred: [the approved observability integration]
    required: false
  publication:
    preferred: [authenticated GitHub integration]
    fallback: [host GitHub CLI]
preferences:
  - Show the caller flow and scope before implementation.
```

A personal project might instead override `issue_context` with GitHub issues and `runtime_evidence` with a local browser or application logs. Arbitrary purpose keys let projects name their own needs without changing the schema.

`required: true` means the purpose’s evidence or capability is a gate for dependent decisions, not that a preferred vendor must be used. A sanctioned fallback can satisfy it only if its evidence is sufficient. If blocked, name the unavailable tool, missing evidence and affected step; continue independent local discovery and ask only for the missing material input. Optional unavailable routes reduce the evidence available; report the limitation and proceed where the task remains supportable. If the missing evidence prevents a workflow’s finish condition, that workflow remains inconclusive even when the route is optional. Never bypass a service write refusal or install/configure integrations solely because a profile names them.
