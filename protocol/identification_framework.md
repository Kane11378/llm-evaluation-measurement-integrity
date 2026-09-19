# Identification framework

## Target problem

A contextual provenance-role effect is only interpretable when the treatment changes the provenance role attached to task-relevant information without simultaneously changing the semantic information needed to solve the task.

The framework separates four layers:

1. **Task information** — what determines the correct target.
2. **Intervention** — which contextual attribute changes between conditions.
3. **Behavior** — the model response under the frozen operating point.
4. **Measurement/inference** — completion, extraction, scoring, continuation and the independent inferential unit.

## Semantic-information equivalence

Matched conditions must preserve the target-relevant semantic content of the context and current prompt except for the intended provenance-role assignment.

## Computational necessity

The designated contextual record is task-level necessary when there exist admissible worlds with the same current prompt and the same nondesignated task-relevant information, but different designated-record values and different oracle targets.

This is an information-structure property of the task. It is **not** evidence that a neural model internally retrieves or represents the record in any particular way.

## Provenance-only intervention

The intended treatment changes which provenance role carries the same designated necessary information. Where role counts could themselves provide a cue, a companion record can be swapped oppositely so that the role multiset remains fixed.

## Behavioral observation versus integrity failure

A completed, readable, nonexact response is a behavioral error and remains in the denominator.

An event that prevents the planned behavioral observation from existing—such as transport failure, noncompletion, resource exhaustion or unreadable/custody failure—is an integrity failure.

## Independent unit

Repeated calls from the same generated instance share task structure and are not automatically independent. Inference must operate on the independent design unit or use an explicit dependence model.

## Identification versus detection

A design can identify a narrow causal/measurement contrast even when the observed confidence interval includes zero. Statistical significance does not repair an identification failure, and non-significance does not imply that an otherwise valid design is unidentified.
