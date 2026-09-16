# Omakase

Omakase is a personal Codex conductor skill for engineering work, from investigation and disposable prototypes through reviewed project delivery. Codex remains the application and coding agent; Omakase supplies opinionated scoping, workflow selection, project tool preferences, and a concise learning loop alongside isolation, setup, validation, publication, and follow-up.

This repository is shared for reference. It is built for my own environment and workflow, not maintained as a general-purpose tool. There is no promise of portability, compatibility, support, or a stable interface. The setup notes below describe my usage; adapting it to another environment is up to you.

It is deliberately not a second agent harness, issue tracker, daemon, or replacement UI.

## What it coordinates

- A compact task brief covering outcome, boundaries, uncertainties, proof, and next steps
- Explicit investigation, prototype, bug fix, feature, refactor, performance, and read-only review workflows
- Shared delivery steps for isolation, validation, independent review, publication, and follow-up
- Optional specialized skills, including Superpowers, when explicitly requested or justified by scale, risk, or repository policy
- GitHub tooling for issues, pull requests, checks, and Actions evidence
- Repository-approved integrations for issue and internal-service context when available
- Codex scheduled follow-ups for pending CI and review work
- Personal defaults that improve from explicit user corrections
- A globally ignored `.omakase.local.yml` for project tool preferences, standing project corrections, and verified machine-local knowledge
- Treehouse as the required reusable-worktree layer when Codex has not already isolated the task

## Personal setup

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

## Scope, tools, and learning

Investigations finish with supported findings and recommendations. Disposable prototypes finish with demonstrated decision evidence and production limitations. Neither automatically enters publication. Production transitions refresh the scope and use the authority already provided by the user.

Read-only work can use the current checkout without a lease or setup. Prototype writes and production implementation use isolation. Missing optional `tools` and `preferences` fields in existing version 1 profiles inherit personal defaults; projects can override only the purposes they need. Tool configuration describes preferences and evidence gates, not credentials, tool availability, or permission to perform external actions.

Explicit corrections persist at their stated personal or project scope when editing is authorized; inferred preferences remain proposals until confirmed. Verified operational discoveries belong in the project profile. See the skill's personal defaults, workflow, and project guidance references for details.

Long-running project orchestration is a future goal. Current scheduled follow-ups address pending CI and review. Behavioral scenarios remain manual; structural checks do not prove agent compliance.

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

## License

[MIT](LICENSE). The license permits reuse; it does not change this project's personal scope or support expectations.
