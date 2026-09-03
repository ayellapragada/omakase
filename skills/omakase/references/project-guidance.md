# Personal project profile

`.omakase.local.yml` is Omakase's personal, machine-local operational memory for one Git repository. It captures the small amount of setup and delivery knowledge that is repeatedly rediscovered in isolated worktrees. It must be globally ignored and never committed.

The profile supplements rather than replaces `AGENTS.md`, repository documentation, CI configuration, or user instructions. Those sources define shared project policy and take precedence. The profile is appropriate for machine-specific commands, local prerequisite paths, worktree caveats, and verified shortcuts.

## One profile across worktrees

Keep the file at the root of the primary checkout. A globally ignored file is not automatically present in linked worktrees, so resolve it through Git metadata rather than looking only in the current directory:

```bash
python3 scripts/profile_path.py --repo <checkout-or-worktree>
```

The resolver returns the first checkout reported by `git worktree list --porcelain`, which is the primary checkout. This gives every task worktree one shared profile that can improve over time.

## Generate when missing

When a repository has no profile, Codex should create a minimal one without turning setup into an onboarding interview:

1. Read active instructions, README setup guidance, runtime version files, CI workflows, and existing automation.
2. Inspect established repository entry points such as `bin/setup`, `script/bootstrap`, `package.json` scripts, and documented Make targets.
3. Start from `assets/omakase.local.example.yml`, retaining only evidence-backed fields.
4. Run the selected bootstrap or validation command in the isolated worktree.
5. Inspect `git status` and confirm bootstrap did not unexpectedly rewrite tracked files.
6. Keep the generated profile only after the relevant command succeeds cleanly, and tell the user what was learned.

Established repository entry points can be used without a redundant confirmation when they are safe and fall within the authorized coding task. Ask before writing novel shell setup, fetching secrets, modifying infrastructure, weakening verification, or doing anything destructive.

## Suggested schema

The schema is intentionally small and extensible:

- `version`: profile format version; currently `1`.
- `bootstrap.steps`: ordered idempotent entries with `runtime` and `run` fields required to make a fresh worktree usable.
- `validation.quick`: focused or inexpensive checks used during implementation.
- `validation.full`: the local completion checks.
- `worktree.required_local_files`: paths that may need to be made available in a worktree; never include their contents.
- `worktree.notes`: verified machine-local caveats that do not fit another field.
- `ci.provider` and `ci.required_checks`: how remote completion is assessed.
- `publication.base_branch` and `publication.merge`: local publication defaults when repository policy does not already specify them.

Unknown fields should be ignored rather than treated as fatal so the profile can evolve without a migration ceremony.

Run `bootstrap.steps` sequentially and stop at the first failure. Validation entries use the same `{runtime, run}` shape. `runtime` identifies the tool family needed for that one command; it is not a shell prefix.

Make `validation.full` self-preparing. When a check consumes ignored generated artifacts, record the repository-supported generator as an earlier validation entry even if bootstrap also runs it. Mirror generators that CI or production builds run before the same checks. A clean Git status does not prove that ignored artifacts are current.

For an asdf-managed project, resolve only the executable needed by the current step:

- `runtime: ruby`: resolve the configured Ruby. Invoke repository Ruby binstubs with that Ruby. Invoke Bundler's executable through the same Ruby interpreter.
- `runtime: node`: resolve the configured Node, npm, or npx executable. Keep the repository's `node_modules/.bin` ahead of language-global executable directories for child processes.
- Do not wrap a Rails or other polyglot process tree in `asdf exec`. Language-global executables can share names with project-local tools and shadow them in descendants.

A command that is merely quiet may still be working; retain its live session and inspect its eventual exit before retrying. Dependency installation is an exclusive operation for that dependency tree: do not overlap it with another installer or a test, build, or hook that consumes the same tree. If an install fails or is interrupted after mutation, treat the tree as untrusted. Once the process has exited, recover with the repository's clean deterministic install or bootstrap command rather than layering an incremental install over partial state.

If the sandbox denies a dependency manager's user-level cache, use a task-scoped cache under the system temporary directory for that execution. Treat this as execution-environment handling, not project knowledge.

## Learning loop

Do not update the profile merely because a command failed. First classify the cause:

- Durable and reproducible: wrong runtime selection, a consistently required bootstrap step, a required local file path, or a stable validation command. Fix, rerun, then persist the learning.
- Dirty bootstrap: a setup command succeeds but rewrites a tracked lockfile or generated source. Prefer a repository-supported clean alternative and verify it leaves tracked files unchanged before persisting it.
- Transient: network outage, registry hiccup, temporary CI incident, or one-time cache corruption. Recover if possible, but do not memorialize it.
- Unsafe or uncertain: secret acquisition, novel host mutation, infrastructure changes, or a speculative workaround. Ask for the smallest required decision before proceeding.

Keep the file concise. Delete stale instructions when repository automation makes them unnecessary.
