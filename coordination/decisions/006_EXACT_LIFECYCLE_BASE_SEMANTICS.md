# Decision 006 — Exact Lifecycle Base Semantics

Status: accepted Stage 3/4 precondition

## Context

Stage 2 established that an `axmref:v1` names one exact immutable object instance. Decision 005 then repaired canonical state revisions so their membership binds exact immutable instances rather than only logical ids.

The next lifecycle contracts still weaken that distinction at the point where work begins and returns:

- `occupancy.base_state_revision` is only a non-empty string;
- `work-claim.base_state_revision` is only a non-empty string;
- `return-packet.base_state_revision` is only a non-empty string.

Lane 03 froze this as `ADV-002-D`, `ADV-002-E`, and `ADV-002-F` in `STAGE3_EXACT_TARGET_STALE_BASE_AUDIT.json`.

Concrete counterexample:

1. state revision A and state revision B share logical id `revision.same-logical-id`;
2. A and B have different canonical content and therefore different immutable references;
3. an occupancy, work claim, or return packet stores only `revision.same-logical-id` as its base;
4. a replacement occupant or later integrator cannot prove whether that object was created from A or B;
5. stale-base or compatibility logic can therefore be wrong while all involved objects remain individually valid.

A hidden rule such as "use the newest revision with that id" would make recency or mutable repository state an undeclared authority over historical meaning. That is incompatible with replayable institutional continuity.

## Decision

Before Stage 4 may claim functioning occupancy, work-claim, return-packet, or stale-base lifecycle semantics, the three lifecycle base relationships must bind **one exact immutable `state-revision` reference**.

The repaired contracts must provide semantics equivalent to:

```text
occupancy.base_state_revision_ref       -> exact axmref:v1:state-revision
work-claim.base_state_revision_ref      -> exact axmref:v1:state-revision
return-packet.base_state_revision_ref   -> exact axmref:v1:state-revision
```

The implementation may retain the existing field spelling if evidence strongly favors compatibility, but the field must then be machine-constrained to the same exact typed reference semantics. A `_ref` spelling is preferred because it makes the semantic upgrade visible and avoids suggesting that an old logical revision id remains acceptable.

Logical revision ids may still exist inside the referenced revision object for navigation, display, or search. They are not sufficient as lifecycle compatibility bases.

## Scope boundary

This decision is intentionally narrower than a mass reference rewrite.

Do **not** automatically convert fields such as `lane_id`, `occupancy_id`, `claim_id`, `producer_lane_id`, or `actor_ref` merely for naming consistency. Some may remain logical/navigation identities if the exact base revision plus an explicit uniqueness rule can resolve the intended instance. If later evidence shows ambiguity, freeze that relationship separately.

`artifact.provenance.base_state_revision` remains the separate `ADV-002-C` obligation. It must become exact before canonical provenance/replay claims, but it is not required to block this narrow lifecycle-contract repair if combining it would broaden the lane unnecessarily.

Integration-receipt and epoch exact-reference repairs (`ADV-002-G/H`, `ADV-011-C/D/E`) remain later Stage 5/6 prerequisites.

## What this enables

After the repaired contracts and deterministic regressions are integrated, Stage 3 may proceed to the smallest work-ledger storage/coordination slice and Stage 4 may later implement lifecycle transitions against an exact base.

This decision itself does **not** implement:

- opening or closing claims;
- occupancy transitions;
- packet submission;
- semantic overlap detection;
- stale-base rejection or selective compatibility;
- integration receipts;
- epochs;
- replay.

## Required regression witnesses

At minimum, the repair must prove:

1. two state revisions with the same logical id but different canonical content receive different immutable refs;
2. substituting A's exact base ref for B's changes the immutable identity of an occupancy, work claim, and return packet;
3. a bare logical revision id is rejected in each repaired base field;
4. an immutable ref of the wrong kind is rejected in each repaired base field;
5. fixtures and schema tests preserve all existing lifecycle fields and evidence/uncertainty semantics while upgrading only the base relationship;
6. no runtime test or documentation silently claims stale-base enforcement merely because the contract can now name an exact base.

## Relationship to the integrated Stage 3 store

The immutable object store integrated from PR #13 can persist the repaired lifecycle objects through the existing Stage 2 identity path once their schemas are updated.

Two store limitations remain explicit and separate:

- `ADV-024-A`: `StoreWriteResult.referenced_members_verified` is transient call state, not a durable per-revision closure receipt. Storage alone never implies reference closure.
- `ADV-025-A`: historical lookup currently depends on the schema occupying the current stable schema filename. Historical schema-context resolution must be repaired before the first incompatible schema migration; long-term readability across such migration is not yet proven.

Neither limitation grants permission to weaken exact lifecycle-base semantics.

## Root grounding

### Truth

A lifecycle object that claims to begin from a base state must identify the exact state it means. A logical name that can denote multiple immutable revisions is insufficient evidence for compatibility or replay.

### Agency / non-domination

No current occupant, newest revision, mutable pointer, repository convention, or actor identity may silently decide which historical base a lifecycle object meant.

### Continuity

A replacement occupant must be able to recover the exact entry/work/packet base from institutional state alone, without private chat memory or recency guesses.

### Wisdom before speed

Repair the smallest contract ambiguity before building lifecycle runtime on top of it. Do not pull integration, epoch, or replay mechanics forward until their own exact-instance obligations become active.

## Evidence boundary

This is an architectural/cross-object contract decision grounded in the integrated Stage 2 identity layer, Decision 005, the current lifecycle schemas, and Lane 03's exact-target audit. It is **not** evidence that the schema repair, work ledger, lifecycle runtime, stale-base validator, integration engine, epoch runtime, or replay already exists.
