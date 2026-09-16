# Scoping and workflows

## Establish the task brief

Before substantive investigation, prototype writing, or implementation, present the smallest brief that makes the task checkable. For straightforward tasks, one paragraph is enough. For substantial work, use these slots:

- **Outcome and workflow:** the problem or decision, intended user or caller, and selected path.
- **Boundaries:** what is included, excluded, and whether the result is findings, disposable work, local production changes, or a PR.
- **Grounding and uncertainties:** current behavior and relevant caller/data flow from repository evidence; unresolved assumptions and material decisions.
- **Proof:** observable checks or comparison criteria, including important behavior that must remain unchanged.
- **Next steps:** the required workflow steps, applicable project tools, and any real checkpoint.

A source issue can supply these facts; reference it rather than copying it wholesale. Mark unknowns as unknown. Inspect the repository to resolve them rather than turning every slot into an interview. For an investigation whose flow is not yet known, state the initial evidence and which flow will be traced.

For “make this better,” establish the concrete symptom, user outcome, or decision before choosing a production solution. Begin with investigation when local discovery can reduce ambiguity. Ask when competing interpretations would materially change the result. A “maybe” addition remains an open decision, outside the active implementation scope.

Keep workflow steps visible in a task list for multi-step work. A skipped step carries its reason and the effect on confidence. Missing proof produces an inconclusive result or concrete blocker, not a confident completion claim.

## Select by the requested outcome

| Workflow | Select when | Required sequence | Finish condition |
| --- | --- | --- | --- |
| Investigation | The user wants understanding, diagnosis, or a recommendation | Frame the question; trace source and caller/data flow; gather relevant history or runtime evidence; test competing explanations safely; separate findings from hypotheses | Supported findings with evidence pointers, remaining uncertainty, and a recommended next step; no product edits or PR |
| Prototype | The user wants decision evidence from disposable work | Name the decision and comparison criteria; isolate artifacts; build the smallest experiment; exercise it; compare distinct alternatives when the question warrants them; identify production gaps | Demonstrated decision evidence, recommendation, limitations, and artifact locations; no production-readiness claim or automatic publication |
| Bug fix | Existing behavior violates an expected contract | Reproduce the symptom; trace its root cause and affected flow; make the smallest scoped repair; verify the original reproduction and relevant adjacent behavior; independently review and deliver | Original defect resolved with regression evidence and applicable full delivery validation |
| Feature | The user wants new or changed production behavior | Ground the user/caller flow and domain shape; settle material design choices; implement the scoped behavior; exercise representative success and failure states; independently review and deliver | Acceptance checks establish the requested behavior and preserved contracts; applicable full delivery validation passes |
| Refactor | Structure changes while observable behavior stays fixed | Identify callers and preserved contracts; establish characterization evidence; change structure; compare behavior at the same boundaries; independently review and deliver | Preserved outputs and side effects demonstrated, with structural goal achieved and applicable full delivery validation |
| Performance | The user wants a measured efficiency improvement | Define metric, workload, and target; establish baseline; locate the bottleneck; change one justified cause; compare under equivalent conditions and check correctness; independently review and deliver | Before/after measurements, method and trade-offs support the scoped improvement; applicable full delivery validation passes |
| Read-only review | The user wants assessment of existing work | Resolve intent and diff; inspect affected flows and acceptance evidence; verify suspected material defects safely; prioritize actionable findings | Findings with locations, consequences, evidence and limitations, or an explicit no-findings result; no edits or delivery lifecycle |

Reproduction can be a focused failing test or a repeatable real-app demonstration. Add regression tests when they provide useful protection; do not create tests that merely repeat the implementation. Performance without a credible baseline remains investigation until measurement is possible. Runtime symptoms and captured traces enter investigation, with the evidence source named in the brief.

## Add requirements proportionately

**Visual work:** apply the visual product reference to prototype comparison or production changes when rendered evidence matters. Disposable prototypes provide comparison evidence locally; PR screenshot requirements apply when publishing a qualifying production change.

**Multi-phase work:** split at real decisions or dependencies into units with their own scope, proof, and exit condition. State order and PR boundaries before implementing the first unit. Keep working artifacts in chat or temporary gitignored locations. This is decomposition within the current task, not a standing project orchestrator or unattended execution system.

**Delivery operations:** opening a PR and following CI/review reuse the core delivery lifecycle. For an existing PR, reconstruct its scope, current head and validation evidence before changing it; select bug fix, feature, or refactor for substantive follow-up work rather than treating every blocker as an undifferentiated repair.

## Prototype workspace disposition

A disposable prototype can be complete without landing. For a Treehouse-backed prototype, preserve the unlanded lease and artifacts at completion; do not return or clean the allocation merely because the experiment finished. Report the absolute worktree path, `lease_id`, `lease_holder`, and unlanded state alongside the decision evidence. State that the retained workspace is available for an authorized production transition or explicit artifact-preserving disposal decision. Do not make that decision a prerequisite for completing the prototype, silently publish it, or broaden Treehouse return safeguards.

For externally provided isolation, report artifact locations and leave disposal to its provisioning environment.

## Transition and re-scope

An investigation can recommend a prototype or implementation. A prototype can inform production design. Proceed only when the conversation already authorizes the new outcome; otherwise return the result and request the smallest next decision. Before an authorized transition, refresh the brief, proof, workspace requirements and publication intent. Prototype shortcuts are not production validation.

New evidence that changes a material boundary triggers re-scoping. Explain what changed and how it affects the outcome before continuing dependent work. Preserve approved scope and artifacts when new user input merely clarifies an existing requirement.

## Example

“Refactor the import parser, preserving output. Maybe change the UI too.”

Select refactor. Map parser callers, name the outputs and side effects to preserve, and establish comparison fixtures. Keep UI work outside the active scope until its intended behavior is decided. Implement and prove the parser change, then use shared review and delivery steps. If the user authorizes UI work, update the brief and add visual evidence requirements.
