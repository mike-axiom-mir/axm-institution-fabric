# Decision 012 — Modified Result Output Compatibility

Status: **accepted as the next bounded Stage 4 preflight**. Decision 011 now grounds the exact prior/result pair for a modification. This decision opens only the smallest read-only compatibility check for the exact **result** artifact of that pair. It does not assert logical lineage, valid supersession, packet acceptance, evidence closure, claim closure, successor publication, Stage 5 integration, epochs, or replay.

## Problem

Decision 011 proves only:

```text
exact packet P
  -> exact claim C
  -> exact claim base B

modified relation M
  -> exact prior artifact A0
     -> exact member of B
  -> exact result artifact A1
     -> exact-loads
     -> exact work-base / producer-lane provenance against B
```

That is enough to remove hidden endpoint selection for the bounded modification relation, but it does not yet answer whether `A1` is an output the exact historical lane was allowed to return or whether packet evidence explicitly supports `A1` under the same narrow single-required-state semantics already used for created outputs.

The current created-output compatibility path cannot simply be treated as modification compatibility. Its evidence-subject resolver is intentionally coupled to packet `artifacts_created[]`, and the older created-output identity surface still fails closed whenever `artifacts_modified[]` is non-empty. Silently treating a modification result as a created output would erase the distinction Decision 011 just made explicit.

## Decision

For the bounded v0 modification path, compatibility applies to the exact **result artifact** `A1` from each already-grounded Decision 011 pair.

The prior artifact `A0` remains evidence of the exact observed pre-work target. It does not become the subject of result-output compatibility merely because it is the prior endpoint.

For each exact modification result `A1`:

1. Decision 011 two-sided identity must succeed first;
2. `A1.type` must match exactly one `lane.outputs[]` entry in the exact claim-base lane;
3. that output type must match exactly one `lane.evidence_requirements[]` entry;
4. the bounded preflight supports only exactly one `required_states[]` value, preserving the existing created-output rule;
5. only exact packet evidence records whose `subject_ref` is the canonical exact immutable ref for `A1` may satisfy that requirement;
6. evidence about `A0`, another same-logical artifact, another exact result, a bare logical id, path, content reference, or non-exact subject must not satisfy `A1`;
7. `artifact.evidence_refs` remains non-authoritative for this compatibility slice;
8. conflicting or additional exact evidence remains explicit and must not be collapsed into evidence closure merely because one record satisfies the required state.

A compatibility result of `satisfied=True` means only that the exact historical lane contract has one matching output declaration, one evidence requirement with one supported required state, and at least one exact packet evidence record explicitly subject-bound to `A1` with that exact state.

It does **not** mean:

- `A0` and `A1` are the same logical artifact;
- `A1` supersedes `A0`;
- `A1` is current, newer, better, or authorized beyond the exact historical claim context;
- evidence is complete, conflict-free, high-quality, or non-invalidated;
- source/dependency refs are closed;
- the packet is accepted;
- the claim is closed;
- a successor revision may be published;
- integration, epochs, or replay are valid.

## Historical contract boundary

Return-packet v0.3 non-empty `artifacts_modified[]` remains operationally unresolved under Decision 011 and therefore cannot enter this compatibility preflight.

Return-packet v0.4 explicit prior/result relations may enter only through the exact Decision 011 preflight. No logical-id fallback, newest/current lookup, storage order, packet array order, artifact version, `supersedes_ref`, actor identity, scheduler position, founder status, or Git permission may manufacture a compatible result.

## Evidence-subject chronology

Decision 008's acyclic evidence chronology applies to the modification result without inventing reciprocal authority:

```text
exact result artifact A1
    -> exact evidence E selected by packet
    -> E.subject_ref must equal exact immutable ref A1
    -> exact packet P names E and the modification relation containing A1
```

`A0` does not satisfy `A1` evidence requirements, and `artifact.evidence_refs` does not override `E.subject_ref`.

## Required next implementation behavior

Lane 02 should implement only a **read-only modified-result compatibility preflight**.

Required bounded behavior:

1. consume the canonical Decision 011 `preflight_modified_artifact_identity(...)` result rather than reconstructing prior/result identity with new rules;
2. exact-load packet `evidence_refs[]` through the existing Stage 2 exact relation language and require kind `evidence-record`;
3. bind evidence to each exact modification result only when `evidence.subject_ref` exactly equals that result ref;
4. preserve non-exact/unrelated evidence explicitly as unmatched or fail closed on wrong-kind exact subjects; never assign by logical id, type, order, recency, or actor intent;
5. reconstruct/use the exact claim-base lane already grounded by Decision 011;
6. apply exactly the current created-output compatibility semantics for lane output type, one evidence requirement, and exactly one required state;
7. preserve conflicting exact evidence instead of treating one satisfying record as closure;
8. preserve all Decision 011 and ADV-035 through ADV-044 regressions;
9. remain read-only and stop before lineage/supersession policy, source/dependency closure, packet acceptance, claim closure, successor publication, integration, epochs, or replay.

Implementation may factor shared compatibility/evidence-binding helpers out of the created-output path if that reduces duplication without changing existing demonstrated semantics. Do not silently broaden the old created-output resolver's claim boundary in the same change unless tests and explicit repository reasoning show that broader refactor is required.

## Adversarial surface for Lane 03

Attack the exact Lane 02 head for:

- evidence about exact prior `A0` being laundered into support for exact result `A1`;
- same-logical-id/different-exact result evidence substitution;
- exact evidence for one modification result being pooled into another;
- bare logical id/path/content subject fallback;
- wrong-kind exact subject refs;
- `artifact.evidence_refs` overriding contradictory exact `subject_ref`;
- duplicate/missing output declarations or evidence requirements;
- multiple `required_states` accidentally gaining AND/OR/rank semantics;
- conflicting exact evidence being silently collapsed into closure;
- packet array order, newest/current, storage order, artifact version, `supersedes_ref`, actor, scheduler, founder, or Git authority;
- historical v0.3 modified entries entering compatibility;
- all ADV-035 through ADV-044 regressions remaining green.

## Root grounding

- **Truth:** exact prior/result identity is not relabelled as output compatibility; only exact result-subject evidence may satisfy the result's narrow contract.
- **Agency / non-domination:** no actor, recency, order, logical-id equivalence, version field, or technical permission chooses evidence or compatibility standing.
- **Continuity:** a replacement occupant can reconstruct the exact modification result, exact lane contract, and exact evidence subject relation from durable state.
- **Wisdom before speed:** extend only the already-grounded single-required-state compatibility surface and keep lineage, closure, acceptance, integration, epochs, and replay closed.
