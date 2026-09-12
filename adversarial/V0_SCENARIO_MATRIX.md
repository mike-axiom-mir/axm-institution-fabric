# Lane 03 — Adversarial v0 Scenario Matrix

Base inspected: `ec7f03f77145a0f151a895c9e804e7715bc95e9c`

Purpose: turn the Institution Fabric continuity hypothesis into concrete failure cases before the deterministic kernel hardens around incomplete assumptions.

This document does **not** claim the current scaffold fails these tests. At this revision, most kernel objects do not yet exist, so the majority of cases are **inferred risks / required future fixtures**, not observed runtime failures.

## Test rule

For every scenario below, the eventual fixture must be runnable using only repository/institution state supplied to the fixture. Hidden chat history, founder memory, specialist private context, or occupant identity must not be required to determine the expected result.

A fixture passes only when the resulting state and reason are reconstructable from stored institutional evidence.

## Priority matrix

| ID | Priority | Failure surface | Adversarial scenario | Pass oracle | Current evidence state |
|---|---|---|---|---|---|
| ADV-001 | P0 | Occupant replacement | Occupant A opens a claim, records partial work and uncertainty, then disappears before handoff. Occupant B enters the same lane from canonical state only. | B can identify the lane, active claim, base revision, partial artifacts, dependencies, evidence, uncertainty, and next legal action without private context. No history is erased or silently re-authored. | inferred requirement |
| ADV-002 | P0 | Stale revision | A packet is produced against revision N after revision N+1 has changed a referenced artifact or dependency. | Integration detects the base mismatch and either rejects, defers, or requests repair with an explicit reason. The stale packet cannot silently land on N+1. | inferred requirement |
| ADV-003 | P0 | Evidence collapse | A return packet claims `done` / `complete` but supplies only `implemented` or `not_tested` evidence where stronger evidence is required. | Validation/integration refuses to promote confidence language into evidence. Accepted status remains bounded by stored evidence requirements. | inferred requirement |
| ADV-004 | P0 | Parallel conflict | Two valid packets from the same epoch independently modify the same artifact or mutually dependent invariants. | The integration stage exposes the conflict; it does not choose a winner by lane rank, timestamp, occupant identity, model confidence, or write permission. Conflict and resolution reason remain explicit. | inferred requirement |
| ADV-005 | P0 | Uncertainty loss | Packet contains a material unresolved uncertainty. Integration otherwise succeeds. | The uncertainty survives into the next revision or receipt until explicitly resolved/superseded with evidence. Absence from the next state is a failure. | inferred requirement |
| ADV-006 | P0 | Provenance loss | Artifact A is modified into A2 by another occupant/revision. | A2 retains stable identity/version lineage, originating packet/claim/revision references, evidence provenance, and relation to A. A later occupant can reconstruct who/what changed it and why. | inferred requirement |
| ADV-007 | P0 | Hidden-context dependence | A fresh occupant receives the lane packet and repository state but none of the prior chat. A prior occupant had relied on an unstored semantic decision. | The fixture must expose the missing state rather than allowing a hidden assumption to become canonical. Correct continuation must be possible once the decision is stored explicitly. | observed design risk; runtime not yet testable |
| ADV-008 | P1 | Dependency invalidation | Artifact B depends on A. A is repaired or invalidated after B was produced. | B is surfaced as downstream-risk / stale / invalidated as defined by the contract; the dependency change is not lost. | inferred requirement |
| ADV-009 | P1 | Semantic claim overlap | Two lanes open differently worded claims that target the same semantic work surface. | The system at minimum reports possible overlap and preserves both claims for review; it must not imply exclusive ownership merely because strings differ. | inferred requirement |
| ADV-010 | P1 | Partial failure recovery | Occupant disappears after creating an artifact but before submitting a valid return packet. | The institution can distinguish orphaned/uncommitted work from integrated canonical state and provide a recoverable path without pretending completion. | inferred requirement |
| ADV-011 | P1 | Parallel vs sequential divergence | Same objective and lane contracts run as a parallel epoch and as sequential occupancy. Ordering changes one accepted result. | Divergence is measured and explained. The system must not claim equivalence merely because both runs completed. | inferred requirement |
| ADV-012 | P1 | Domain leakage | Game Studio introduces a kernel field such as `playtest_score`, `weapon_balance`, or another game-only primitive. | Universal kernel validation rejects or quarantines the field unless cross-domain evidence justifies promotion. Domain-specific state remains in the domain package. | inferred requirement |
| ADV-013 | P1 | Constitutional authority leakage | A packet/integration reason cites founder status, specialist title, model capability, schedule position, or Git permission as sufficient authority. | Integration reason is invalid/insufficient unless grounded in evidence, compatibility, state, and the four roots. Identity/rank alone cannot settle canonical truth. | inferred requirement |
| ADV-014 | P1 | Product/internal authority confusion | A user-facing package treats the product user's authority over their state as authority to rewrite AXM internal constitutional state, or treats AXM roots as permission to override the user's product state. | The two scopes remain explicit: product-level user merge authority is bounded to that product relationship; AXM internal canonical evolution remains root-grounded. | inferred requirement |
| ADV-015 | P2 | Evidence provenance mismatch | Evidence references a test/build/result generated for a different artifact version or base revision. | Validation surfaces the mismatch; evidence cannot silently attach to a new version because names look similar. | inferred requirement |
| ADV-016 | P2 | Replay incompleteness | Revision N+1 exists but one decision/input/receipt needed to explain its creation is missing. | Replay fails loudly as incomplete rather than reconstructing a plausible story. Missing provenance is itself represented as a failure. | inferred requirement |

## First fixture contract for Lane 02

The strongest minimum adversarial fixture set for the first executable kernel is:

1. **replacement_preserves_history** — covers ADV-001.
2. **stale_packet_is_not_integrated** — covers ADV-002.
3. **weak_evidence_cannot_become_done** — covers ADV-003.
4. **parallel_conflict_is_explicit** — covers ADV-004.
5. **uncertainty_survives_integration** — covers ADV-005.
6. **artifact_provenance_survives_revision** — covers ADV-006.
7. **dependency_change_marks_downstream_risk** — covers ADV-008.
8. **domain_specific_field_does_not_enter_kernel** — covers ADV-012.

These are requirements, not an implementation prescription. Lane 02 owns the technical representation.

## Required stored facts exposed by the scenarios

The scenarios collectively require the kernel to make these facts reconstructable from explicit state:

- lane id and lane contract version;
- occupancy identity/reference and entry base revision;
- claim id, scope, status, and base revision;
- artifact stable id, version, provenance, and dependencies;
- evidence record id, evidence state, target artifact/output version, and producing context;
- packet base revision and referenced claim/lane;
- unresolved uncertainty and blockers;
- downstream effects / invalidation signals;
- integration decision, reason, and resulting revision;
- supersession/invalidation relationships where state changes meaning;
- epoch/base relationship for parallel work.

The exact schemas remain a Lane 02 implementation concern, but omission of any reconstructability requirement must be justified against the continuity proof rather than hidden in chat.

## Observed repository finding at base revision

At `ec7f03f...`, the repository has the architectural contracts and one machine-readable `lane.schema.json`, but no executable occupancy, claim, artifact, evidence, return-packet, state-revision, or integration objects yet. Therefore:

- no occupant-replacement proof can currently be executed;
- no stale-base or parallel-conflict behavior can currently be measured;
- no provenance or uncertainty survival can currently be replayed;
- this is consistent with the repository being an initial scaffold, not a defect by itself.

The immediate value of Lane 03 is to freeze the failure oracles before implementation choices make them easy to accidentally redefine.

## Root implications

- **Truth:** never convert missing evidence or incomplete replay into a success story.
- **Agency / non-domination:** do not use role identity, founder status, or technical permission as conflict authority.
- **Continuity:** the next occupant must be able to reconstruct state without the vanished occupant.
- **Wisdom before speed:** prefer explicit blocked/deferred/conflict state over silent integration when evidence is incomplete.

## Next adversarial experiment

After Lane 02 lands the first canonical objects, instantiate ADV-001, ADV-002, ADV-003, and ADV-005 as executable fixtures before adding large runtime or adapter complexity. Those four expose whether continuity, stale-state detection, evidence precision, and uncertainty survival are real mechanics rather than documentation.