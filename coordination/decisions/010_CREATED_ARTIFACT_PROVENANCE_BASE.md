# Decision 010 — Exact Created-Artifact Provenance Base

Status: accepted as the next bounded Stage 4 continuity boundary after created-output compatibility preflight.

## Context

The created-output compatibility preflight can now reconstruct an exact packet/claim/lane context and evaluate one exact packet-created artifact against one exact lane output contract and one exact required evidence state.

That does not yet make the created artifact's provenance replayable.

The current artifact contract still records:

```text
provenance.producer_lane_id
provenance.base_state_revision
```

where `base_state_revision` is only a non-empty string. Current compatibility fixtures therefore can use a logical revision id even while packet/claim lifecycle state uses canonical exact immutable `state-revision` refs.

This is the unresolved `ADV-002-C` class of problem: a provenance base that can later resolve by logical id, newest version, storage recency, mutable current state, or private actor memory cannot support an exact replay claim.

## Decision

For the bounded v0 path where a return packet declares an artifact in `artifacts_created[]`, any provenance relation later used for packet acceptance, successor publication, or replay must be grounded to the same exact immutable work base that governed the packet's exact claim.

The required invariant is:

```text
exact packet P
  -> exact claim C
  -> exact claim base revision B
  -> exact claim lane L

exact created artifact A named by P
  -> A.provenance.producer_lane_id == L.id
  -> A provenance base names exact immutable state revision B
```

This is a bounded created-artifact rule. It does not define modified-artifact provenance, source-ref semantics, dependency closure, evidence closure, supersession/currentness, or packet acceptance.

## Representation boundary

The existing `artifact.schema.json` v0.1 field `provenance.base_state_revision` is not sufficient for an exact-base claim because its schema accepts any non-empty string.

Lane 02 may choose the smallest explicit contract repair that preserves historical meaning, for example a schema-versioned exact-ref field such as `base_state_revision_ref`, provided that:

- the canonical Stage 2 immutable-ref grammar is reused;
- required kind is `state-revision`;
- the exact target is loaded and identity-verified before operational use;
- no logical-id/current/newest/array-order fallback is introduced;
- historical v0.1 artifacts are not silently reinterpreted as exact when they are not;
- schema/version migration behavior is explicit and tested.

This decision does not require that exact field spelling. It requires the exact semantic relation.

## Why equality to the claim base is grounded for `artifacts_created[]`

In the current Stage 4 model, the packet is a handoff from one exact open claim against one exact work base. An artifact asserted as created by that handoff must not silently claim a different work base while still being treated as output of the claim.

Inputs from earlier revisions or external sources may later be represented through explicit source/dependency relations. They must not overload the artifact's work-base provenance relation.

If later evidence demonstrates a universal need for created outputs whose authoritative work base differs from the claim base, that must become a new explicit chronology rule rather than an implicit exception.

## Non-decisions

Decision 010 does **not** decide:

- whether `source_refs[]` must be exact immutable refs;
- whether `dependency_refs[]` are closed or exact;
- how modified artifacts represent exact observed-prior and exact produced-result identities (`ADV-002-I` remains open);
- whether conflicting evidence invalidates an otherwise satisfied required state;
- semantics of multiple `required_states`;
- packet acceptance or rejection policy;
- claim closure;
- successor state publication;
- integration receipts/runtime;
- epochs/barriers or replay implementation;
- global currentness, authorization, or ownership.

## Root grounding

### Truth

A provenance base used to justify an artifact cannot remain a logical string while the surrounding lifecycle claims exact immutable history. The relation must be exact or remain explicitly unresolved.

### Agency / non-domination

No occupant, caller, scheduler, founder, storage order, or mutable current pointer gains authority to choose which historical revision a vague provenance string meant.

### Continuity

A replacement occupant must be able to reconstruct the artifact's work base from durable exact state without private chat or actor memory.

### Wisdom before speed

Open only the created-artifact exact-base precondition. Do not bundle source closure, modified artifacts, evidence conflict policy, acceptance, integration, epochs, or replay into the same step.

## Next implementation boundary

Lane 02 should implement only the smallest schema/runtime/test repair needed to make packet-created artifact provenance exact and reproducible:

1. preserve canonical created-output compatibility behavior and ADV-035 through ADV-042;
2. represent the created artifact provenance base as one canonical exact immutable `state-revision` ref;
3. exact-load and verify that provenance base;
4. require it to equal the exact claim base reconstructed for the packet;
5. require `producer_lane_id` to equal the exact claim-base lane logical id;
6. fail closed on non-exact, wrong-kind, missing, or different-base provenance;
7. remain read-only beyond any necessary schema-version migration and do not accept packets or close claims;
8. leave `artifacts_modified[]` fail-closed.

Lane 03 should then attack same-logical-id/different-exact base substitution, wrong-kind refs, stale/different exact base, producer-lane mismatch, historical-schema ambiguity, and hidden newest/current fallback while preserving the existing regression spine.
