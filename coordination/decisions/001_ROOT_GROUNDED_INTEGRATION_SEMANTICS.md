# Decision 001 — Root-Grounded Integration Semantics for v0

Status: proposed for canonical coordination state by Lane 01; grounded from existing constitutional text plus Lane 03 counterexamples.

Scope: internal AXM Institution Fabric v0 integration receipts. This decision does not redefine the four roots and does not grant Lane 01, any founder, specialist, model, or Git permission constitutional authority.

## Why this decision exists

Lane 02 PR #3 introduced a machine-readable integration receipt with per-root assessments: `grounded`, `uncertain`, or `conflict`.

Lane 03 then produced a concrete counterexample showing that the current schema shape can describe `decision: accepted` while a constitutional root is simultaneously assessed as `conflict`. The same contract can also describe state-transition contradictions such as a deferred decision producing a new revision.

Those shapes are syntactically possible but institutionally ambiguous. A later occupant should not need hidden chat convention to infer whether such a receipt means canonical state changed.

## v0 semantic rule

For **internal AXM canonical evolution**, a receipt may create a new canonical state revision only when the proposed transition is sufficiently grounded against all four roots.

For v0, make that machine-testable with the following conservative rule:

1. `accepted`
   - all four root assessments MUST be `grounded`;
   - `unresolved_conflicts` MUST be empty;
   - `resulting_state_revision` MUST be non-null;
   - the new revision remains a technical state transition whose standing comes from stored grounding/evidence, not actor identity.

2. `rejected`, `deferred`, or `repair_requested`
   - MUST NOT create a new canonical state revision;
   - `resulting_state_revision` MUST be null;
   - root assessments MAY contain `uncertain` or `conflict`, because those states help explain why canonical transition did not occur.

3. `partially_integrated`
   - is **not sufficiently specified for a state-creating v0 receipt yet**;
   - the current receipt does not identify which packet outputs were integrated versus withheld;
   - until explicit accepted/deferred subset references exist, v0 validation should reject or disable state-creating use of `partially_integrated` rather than invent hidden semantics.

4. A root assessment of `uncertain` is not equivalent to ordinary packet uncertainty.
   - ordinary implementation uncertainty may survive into an accepted revision when the transition is still root-grounded;
   - uncertainty about whether the transition itself satisfies a constitutional root means the root gate is not yet established strongly enough for full acceptance.

5. Root assessments are evidence-bearing reasons, not four votes.
   - identity, seniority, founder status, specialist title, model capability, confidence, schedule position, or Git permission cannot override an explicit unresolved root conflict.

## Related continuity requirements confirmed by the adversarial review

These are not new constitutional roots; they are derived v0 contract requirements needed to make continuity reconstructable:

- strong evidence states such as `automated_tested` must have enough explicit support to reconstruct how they were established; exact field encoding remains a Lane 02 implementation concern;
- occupancy lifecycle must be internally coherent (`active` cannot also be ended; ended occupancy must carry an end record/time);
- decision/result pairs must be cross-field coherent rather than relying on prose convention;
- the seed lane contract should join the same explicit schema-versioning convention before Stage 1 is frozen;
- the epoch/barrier descriptor remains the final missing canonical object named by the Stage 1 build plan.

## Root grounding

### Truth
A canonical receipt must not simultaneously claim acceptance and record that constitutional compatibility is unresolved or in conflict. The machine-readable state should say what actually happened.

### Agency / non-domination
No actor category or technical permission can turn a root conflict into acceptance. The rule applies identically regardless of who occupies the lane.

### Continuity
A replacement occupant can determine from the receipt alone whether canonical state changed, why, and what remains unresolved.

### Wisdom before speed
When root compatibility is uncertain, defer or request repair rather than freezing ambiguity into revision history.

## Implementation boundary

Lane 02 owns the exact JSON Schema/runtime encoding and regression tests. Lane 03 owns adversarial counterexamples/oracles. Lane 01 owns keeping these semantics coherent with the project architecture and reviewing the integrated result.

A passing schema test will establish contract behavior only. It will not by itself prove the integration runtime, immutable state store, or replay engine.
