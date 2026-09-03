# Repository conventions

Discover how the target repository names and writes delivery artifacts before creating them. Preserve meaningful local consistency without copying incidental quirks, author-specific voice, or stale automation.

## Evidence order

Use the strongest applicable evidence for each artifact:

1. **Explicit policy:** user instructions, `AGENTS.md`, contributing guides, repository configuration, release tooling, and pull-request templates. Higher-priority instructions always win.
2. **Recent accepted examples:** representative human-authored commits and merged or maintained pull requests on the target repository. Prefer roughly 10–20 recent examples when available, but stop once the pattern is clear.
3. **Clear neutral style:** use concise imperative wording and the platform's safe defaults when the available evidence is mixed or weak.

Exclude merge commits, reverts, bot or dependency-update output, generated releases, abandoned experiments, and obvious outliers unless the current artifact is the same kind. Favor recent examples accepted on the default branch over old or merely open work.

Do not promote a historical pattern over explicit policy. Do not treat a pattern as established from one or two examples when broader evidence is available.

## Inspect by artifact

Resolve each relevant artifact separately:

- **Branch names:** inspect current and recent remote branch names. Identify prefixes, separators, issue identifiers, and slug style. If the platform or user requires a prefix such as `codex/`, keep that required platform prefix and incorporate the repository's meaningful naming semantics after it when compatible.
- **Commit subjects and bodies:** inspect recent non-merge, human-authored commits. Determine whether the repository uses Conventional Commits, scopes, imperative mood, capitalization, terminal punctuation, wrapped bodies, or issue trailers. Do not add a scope, body, or trailer without evidence or a concrete need.
- **Pull-request titles:** inspect recent merged pull requests independently from commits. Match their title structure, capitalization, prefixes, and issue identifiers; do not infer title style from squash commits unless the evidence shows they intentionally match.
- **Pull-request bodies:** use the repository template exactly when present. Preserve its headings, comments, checklists, and expected issue-link syntax. Use recent accepted bodies only to clarify how sections are normally completed.
- **Release notes and changelog entries:** follow repository tooling and recent entries for category, audience, and tense.
- **Review replies:** be concise and factual. Match established resolution markers or issue references when evident, but do not imitate personal tone or ceremonial acknowledgements.

Local Git can establish commit and branch conventions. Use the available authenticated GitHub integration for pull-request evidence; if unavailable, continue with local and explicit evidence rather than blocking publication solely to infer style.

## Apply and verify

Before creating an artifact, state the inferred rule internally in one sentence and check the draft against it. Keep content accurate even when an example contains a typo or misleading phrasing.

After a commit, push, or pull-request mutation, read the created or updated artifact back and verify both its content and format. Correct an accidental convention mismatch before reporting publication complete. Do not rewrite published history solely for cosmetic consistency unless that rewrite is already authorized and safe.
