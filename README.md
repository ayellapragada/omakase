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
- `tests/` verifies the skill contract and helpers.
- `evals/` records behavioral scenarios that should remain true.

Temporary design specs and implementation plans are working artifacts, not maintained repository documentation.

## Validation

Run the contract and helper tests:

```bash
python3 -m unittest discover -s tests -v
```

Validate the Codex skill structure:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/omakase
```
