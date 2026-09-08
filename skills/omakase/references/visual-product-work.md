# Visual product work

Use this path when a change materially affects rendered UI, layout, styling, interaction states, or product imagery. Apply it proportionately: a focused component fix needs baseline and result verification, while a new or substantially redesigned experience may benefit from broader exploration and critique.

Do not activate this path merely because a frontend file changes. Skip it when screenshots would not materially improve implementation or review, including backend behavior, infrastructure, internal refactors, and nonvisual frontend logic. For tiny copy or pixel changes, use screenshots only when they make the effect meaningfully easier to assess.

## Establish visual evidence early

Before editing, identify the representative routes, states, data, themes, and viewports that communicate the change. Capture the meaningful baseline before implementation while the base behavior is still easy to reproduce. If comparison matters, capture the result with the same state, data, viewport, and theme; label intentional differences.

Do not fabricate a before state for a new surface. State that the surface is new and provide representative after views. Prefer a small, reviewable set over an exhaustive gallery.

## Explore and build proportionately

For open-ended or substantial design work, define the intended feeling, product purpose, constraints, and quality bar before choosing a direction. Explore genuinely distinct directions when that would reveal a meaningful product choice. Treat supplied references or generated concept art as a moodboard and quality baseline, not material to copy.

Consider image generation when custom imagery, texture, atmosphere, or visual storytelling would give the product useful identity or communicate something code-native primitives cannot. Use the environment's dedicated image-generation capability when available, inspect generated assets, and optimize accepted outputs for the product. Do not generate imagery for routine controls, established icon or logo systems, simple diagrams, or decoration that adds no product value. Prefer the project's existing design system and repo-native assets when they fit.

Implement the approved direction, then inspect the real rendered experience in a browser. Exercise representative content, empty and error states when relevant, responsive widths, supported themes, and important interactions. Check hierarchy, readability, contrast, overflow, focus behavior, motion, loading, and consistency with the product rather than judging a single ideal screenshot.

## Critique and polish

For substantial visual work, make the required independent review include independent visual critique. Give the reviewer the visual brief, acceptance criteria, target references when relevant, and current screenshots; avoid implementation rationale that anchors it to existing choices. Ask for prioritized, specific gaps in composition, hierarchy, product fit, accessibility, responsiveness, restraint, and conspicuous AI-generated patterns.

Keep the loop bounded: perform one critique pass, address material findings, and request at most one scoped re-review when warranted. Do not chase an arbitrary score. Remove elements that do not serve comprehension, interaction, or the intended emotional effect.

## Embed screenshots in the pull request

For every qualifying change, add a `## Screenshots` section to the pull-request body. Use descriptive alt text and, when comparison matters, a compact before/after table. If there is no meaningful baseline, say why and include after screenshots only. Preserve the repository's pull-request template: place the section in the most appropriate existing location or append it without replacing required structure.

Keep captures as temporary delivery artifacts outside tracked source. Do not commit them solely to make them available to reviewers. Draft the PR body with Markdown references to the local files, then pass those same paths to GitHub CLI with `--attach` on `gh pr create` or `gh pr edit`. GitHub replaces the local references with hosted URLs.

Read the published body back and confirm the expected images render as direct embeddings with accurate labels. A qualifying visual change is not review-ready while its required screenshots are missing or broken. Retry a safe upload when appropriate; otherwise report the concrete permission or tooling blocker instead of silently omitting the evidence.
