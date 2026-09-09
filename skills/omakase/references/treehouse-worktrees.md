# Treehouse worktree lifecycle

Treehouse is Omakase's required provisioning layer when the current task is not already in a clean task-specific worktree. It provides reusable isolated slots whose ignored dependencies and build caches survive between tasks. It does not replace the project profile, bootstrap, validation, publication, or review workflow.

## Preflight and acquire

Resolve the primary checkout and run Treehouse from there. Use a project-local pool with `--root .` so the pool remains inside the repository's writable boundary. Before the first mutation, verify that `treehouse` exists and that its help exposes every flag used below: leased JSON acquisition, the project-local root, optional no-fetch acquisition, JSON status, and conditional return by both lease identity fields. If the interface is missing or incompatible, stop before editing and request installation or repair. Do not silently fall back to a raw Git worktree.

During intake, and in any case before requesting another allocation, read `treehouse status --root . --json` and opportunistically reconcile existing leases. For each leased Git worktree with a local branch, use the current repository and exact head branch to look up its pull request. Return an allocation only when exactly one matching pull request is proven merged and every safeguard in [Retain and return](#retain-and-return) passes against the live status record. Leave open pull requests and leases without a matching pull request untouched. Preserve closed-unmerged, multiply matched, dirty, live-process, identity-mismatched, or otherwise unverifiable allocations and report the concrete state and smallest required action. Reconciliation is best-effort maintenance, not authority to merge, discard work, force a return, or delete a remote branch.

Resolve the task's base branch and fetch required refs once. When those refs were already fetched and verified during intake, acquire with this shape to avoid a duplicate network operation:

```bash
treehouse get --lease --json --lease-holder "$lease_holder" --root . --no-fetch
```

Otherwise omit `--no-fetch` and let Treehouse fetch. Parse and retain the returned absolute `path`, `lease_id`, and `lease_holder`. Treat missing, malformed, or mismatched allocation data as a failed acquisition.

Treehouse worktrees begin at detached HEAD on the repository default. In the acquired path, move the clean detached worktree to the already-fetched base ref, then create the task branch using the resolved repository and platform naming convention:

```bash
git switch --detach "$base_ref"
git switch -c "$task_branch"
```

Confirm that the worktree, branch, base commit, and lease record match the intended task before editing. Carry the allocation identity in every scheduled follow-up that may resume the task.

Satisfy required local files after acquisition using the project profile without exposing or committing their contents. Treehouse hooks do not own bootstrap: their failures are non-fatal, so correctness-critical setup and dependency refresh remain ordered profile steps. Run those steps even when a reused slot already contains dependencies; the warm slot should make an incremental refresh cheap, not make freshness implicit.

## Retain and return

Keep the lease while its pull request is open so CI fixes and review feedback use the same warmed environment. A local-only task likewise keeps its lease until its authorized landing or another explicit disposition.

After the pull request merges or an authorized local landing succeeds, verify all of the following before cleanup:

- the landing or pull-request outcome is current and proven;
- the path is the exact managed worktree recorded for this task;
- `lease_id` and `lease_holder` still match the live Treehouse allocation;
- the task worktree is clean and no task process is still using it; and
- the local task branch is safe to delete under the repository's merge semantics.

From the primary checkout, pass the recorded absolute path explicitly and condition the return on both identity fields:

```bash
treehouse return --if-lease-id "$lease_id" --if-lease-holder "$lease_holder" "$path"
```

Do not use a force option to erase a failed safety check. Read `treehouse status --root . --json` back from the primary checkout and confirm that the same recorded path is no longer leased before deleting the local task branch.

Do not return a dirty, unlanded, mismatched, unverifiable, or still-running allocation. If a pull request closes without merging, work is abandoned, or conditional return fails, preserve the lease and report its path, identity, state, and the smallest decision or repair needed. Never destroy a Treehouse slot as an implicit cleanup fallback.
