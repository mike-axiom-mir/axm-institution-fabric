# Decision 005 — Exact Revision Membership

Status: accepted Stage 3 precondition

## Context

Stage 2 established a critical distinction:

- a logical object id is a stable human/institution-facing name;
- an immutable `axmref:v1` binds one exact validated canonical object instance.

The integrated `state-revision.schema.json` v0.1 does not apply that distinction consistently. It stores `objective_id`, `lane_ids`, `occupancy_ids`, `claim_ids`, `return_packet_ids`, `integration_receipt_ids`, and `parent_revision_id` as logical ids, while artifacts and evidence already use reference fields.

That is not sufficient for a replayable immutable snapshot once more than one valid instance may exist under the same logical id.

Concrete counterexample:

1. create objective instance A with `id = objective.alpha` and desired outcome X;
2. create objective instance B with the same logical `id = objective.alpha` and desired outcome Y;
3. both instances are independently valid and receive different Stage 2 immutable references because their canonical bytes differ;
4. a state revision containing only `objective_id = objective.alpha` has identical membership bytes regardless of whether A or B is intended.

A future store could impose a separate undocumented rule that logical ids are forever write-once, but no such invariant currently exists in the institution contract. Hidden store convention cannot repair an under-bound canonical revision.

The same issue applies to lane contracts and other revision members whose content can differ while retaining a logical identity. `parent_revision_id` also fails to identify one exact parent instance if revision logical ids are ever reused or reconstructed inconsistently.

## Decision

Before Stage 3 may claim a canonical state store, the state-revision contract must bind **exact immutable instances**, not only logical names.

The next state-revision contract should require the exact membership shape below or an equally explicit typed-reference equivalent:

```text
parent_revision_ref        nullable exact immutable state-revision ref
objective_ref              exact immutable objective ref
lane_refs                  exact immutable lane refs
occupancy_refs             exact immutable occupancy refs
claim_refs                 exact immutable work-claim refs
artifact_refs              exact immutable artifact refs
evidence_refs              exact immutable evidence-record refs
return_packet_refs         exact immutable return-packet refs
integration_receipt_refs   exact immutable integration-receipt refs
```

Logical ids may still exist inside the referenced objects and may be used for search, display, registries, overlap detection, or human navigation. They are **not** sufficient as canonical revision membership identity.

The revision's own logical `id` may remain a logical name. Its exact immutable identity is the Stage 2 typed reference produced from its validated canonical bytes.

## Stage boundary

This decision does **not** implement the state store and does not pull the full integration engine forward.

Stage 3 may implement:

- local/offline immutable persistence of validated canonical objects;
- exact lookup by immutable reference;
- immutable revision persistence after the repaired revision contract exists;
- a mutable convenience pointer/index such as `current` or `HEAD`, provided it is never treated as identity or merge authority;
- idempotent re-storage of byte-identical content;
- loud failure if an alleged exact reference does not resolve to the exact canonical bytes it names.

Stage 3 must not yet claim:

- stale-base transition enforcement is complete;
- claim/occupancy lifecycle is complete;
- packet integration is complete;
- supersession graph validity is complete;
- epoch progression is complete;
- replay of an accepted transition is complete.

Those remain later transition/integration obligations unless a concrete storage dependency requires a smaller prerequisite.

## Required regression witnesses

At minimum, the repaired contract/tests must prove:

1. two valid objectives with the same logical id but different content receive different immutable refs;
2. substituting one objective ref for the other changes the canonical state revision identity;
3. two valid lane contracts with the same logical id but different content cannot collapse to one revision membership identity;
4. parent revision membership uses one exact immutable parent ref, not only a logical revision id;
5. duplicate exact refs in fields that require unique membership fail according to the schema;
6. a fresh occupant can determine every exact member instance of a stored revision without private chat memory or an undocumented mutable-id convention.

## Downstream audit required

Several Stage 1 contracts also name a base/target revision by logical id. Lane 03 should use the Stage 3 stale-base oracle (`ADV-002-B`) to inventory those fields before Lane 02 implements transition semantics.

Do not silently convert every `*_id` field into a reference merely for naming consistency. Change a field only when exact-instance semantics are required by the relationship and preserve the reason in repository evidence.

## Root grounding

### Truth

A canonical snapshot must identify the exact objects it claims compose that snapshot. A logical name that can denote multiple valid instances is insufficient evidence of exact state.

### Agency / non-domination

This decision grants no actor or implementation authority. It removes hidden store convention from the meaning of canonical state, making the contract inspectable by any later occupant.

### Continuity

A replacement occupant must be able to reconstruct revision membership from repository/store state alone. Exact immutable references preserve that continuity across occupant and implementation changes.

### Wisdom before speed

Stage 3 storage is held at the smallest necessary boundary rather than building a work ledger on an ambiguous snapshot model and repairing persisted history afterward.

## Evidence boundary

This is an architectural/cross-object contract decision derived from the integrated Stage 2 identity semantics and the current v0.1 state-revision schema. It is **not** evidence that the repaired schema, state store, stale-base validator, integration engine, or replay runtime already exists.
