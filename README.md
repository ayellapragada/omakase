# Omakase

Omakase is a personal Codex conductor skill for coding work that is intended to land. Codex remains the application and coding agent; Omakase supplies consistent defaults for isolation, project setup, validation, publication, CI follow-up, and review follow-up.

It is deliberately not a second agent harness, issue tracker, daemon, or replacement UI.

## What it coordinates

- Superpowers for design, planning, worktrees, implementation discipline, review, and verification
- GitHub tooling for issues, pull requests, checks, and Actions evidence
- Grim for Wistia and Shortcut context when available
- Codex scheduled follow-ups for pending CI and review work
- A globally ignored `.omakase.local.yml` for verified machine-local project knowledge

## Installation

The active personal installation links this repository's skill directory into the shared agent-skills directory:

```text
~/.agents/skills/omakase -> ~/Code/omakase/skills/omakase
```

Changes to `skills/omakase/` therefore apply to the installed skill without a separate copy or packaging step.

## Repository structure

- `skills/omakase/SKILL.md` defines the conductor behavior and trigger boundary.
- `skills/omakase/references/` contains focused supporting guidance.
- `skills/omakase/assets/` contains the local project-profile template.
- `skills/omakase/scripts/` contains deterministic helper scripts.
- `tests/` verifies the skill contract and helpers.
- `evals/` records behavioral scenarios that should remain true.

Design specs and implementation plans under `docs/superpowers/` are local working artifacts. They are globally ignored and are not part of the repository's maintained documentation.

## Validation

Run the contract and helper tests:

```bash
python3 -m unittest discover -s tests -v
```

Validate the Codex skill structure:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/omakase
```
