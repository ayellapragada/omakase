# Omakase

Omakase is a personal Codex conductor skill for coding work that is intended to land. Codex remains the application and coding agent; Omakase supplies consistent defaults for isolation, project setup, validation, publication, CI follow-up, and review follow-up.

It is deliberately not a second agent harness, issue tracker, daemon, or replacement UI.

## What it coordinates

- Its own lean delivery workflow for planning, isolation, validation, review, and publication
- Optional specialized skills, including Superpowers, when explicitly requested or justified by scale, risk, or repository policy
- GitHub tooling for issues, pull requests, checks, and Actions evidence
- Repository-approved integrations for issue and internal-service context when available
- Codex scheduled follow-ups for pending CI and review work
- A globally ignored `.omakase.local.yml` for verified machine-local project knowledge
- Treehouse as the required reusable-worktree layer when Codex has not already isolated the task

## Installation

The active personal installation links this repository's skill directory into the shared agent-skills directory:

```text
~/.agents/skills/omakase -> ~/Code/omakase/skills/omakase
```

Changes to `skills/omakase/` therefore apply to the installed skill without a separate copy or packaging step.

[Treehouse](https://github.com/kunchenguid/treehouse) is a required machine prerequisite for work that begins in a primary checkout. Omakase reuses an existing task-specific worktree when Codex already supplied one; otherwise it leases a warmed Treehouse slot from a project-local pool and retains that lease through publication and follow-up.

## Repository structure

- `skills/omakase/SKILL.md` defines the conductor behavior and trigger boundary.
- `skills/omakase/references/` contains focused supporting guidance.
- `skills/omakase/assets/` contains the local project-profile template.
- `skills/omakase/scripts/` contains deterministic helper scripts.
- `skills/omakase/agents/` contains Codex-facing display metadata.
- `scripts/` contains repository-level validation entry points.
- `tests/` verifies executable behavior and repository structure.
- `evals/` records categorized manual behavioral scenarios; CI validates their structure but does not execute them.

Temporary design specs and implementation plans are working artifacts, not maintained repository documentation.

## Validation

Install the development dependency, then run the contract and helper tests:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
```

Validate the Codex skill structure:

```bash
python3 scripts/validate_skill.py skills/omakase
```
