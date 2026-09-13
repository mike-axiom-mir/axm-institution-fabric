# Decision 007 — Lifecycle Relationship Chronology

Status: accepted Stage 4 precondition

## Context

Decision 006 made every lifecycle object bind one exact immutable `state-revision` as its work/entry base. The integrated `resolve_exact_revision_member(...)` primitive now proves that a logical id can be resolved deterministically **inside one exact base revision** only when exactly one immutable member of the required kind matches.

That primitive is correct on its bounded surface, but it does not decide which lifecycle relationships are temporally allowed to resolve from the object's base revision.

The important chronology distinction is:

```text
object existed in the exact base
    -> base-local exactly-one resolution may be valid

object is created after the exact base was observed
    -> it cannot be truthfully resolved from that base
    -> bind the exact created instance directly instead
```

A hidden rule such as newest/current/array order would erase that distinction and make later repository state an undeclared authority over historical meaning.

## Concrete counterexample

1. revision N contains lane `lane-02`;
2. occupancy O is created to enter `lane-02` **from N**;
3. work claim C is then created by O, still describing work against N;
4. return packet P is later created for C, also preserving N as the work base;
5. O and C did not exist in N by construction;
6. therefore `C.occupancy_id` and `P.claim_id` cannot be resolved from N without consulting state that came later;
7. if two later occupancies or claims share one logical id across immutable versions, a newest/current guess can silently choose the wrong historical instance.

The exact base remains necessary, but it is not sufficient for relationships whose target is created after that base.

## Decision

Lifecycle relationship resolution must follow relationship chronology rather than one universal lookup rule.

### A. Pre-existing-at-base relationships

A logical relationship may remain a logical id when its contract requires the target to pre-exist in the exact base and the runtime proves exactly one matching immutable member there.

For the first Stage 4 slice:

```text
occupancy.lane_id
    -> resolve against occupancy.base_state_revision_ref
    -> member family lane_refs
    -> required kind lane
    -> exactly one match required
```

The same principle may later apply to `work-claim.lane_id` or `return-packet.lane_id`, but that wiring must be tested with their own transition semantics rather than assumed from this decision.

### B. Created-after-base relationships

A relationship whose target is created after the work base must bind the exact immutable target instance directly.

Before work-claim runtime may dereference its occupancy relationship:

```text
work-claim.occupancy_ref
    -> exact canonical axmref:v1:occupancy
```

Before return-packet runtime may dereference its claim relationship:

```text
return-packet.claim_ref
    -> exact canonical axmref:v1:work-claim
```

The existing logical-only `occupancy_id` and `claim_id` spellings are therefore insufficient as authoritative runtime relationships. The schema repair may rename them to `_ref` fields or equivalently constrain them to exact typed immutable refs; `_ref` is preferred because the temporal semantic change is material.

### C. Snapshot/index fields are not hidden authority

Fields such as `occupancy.claim_ids` and `work-claim.overlap_with_claim_ids` may remain useful snapshot, navigation, or reporting data for now. They must not silently become authoritative dereference rules until their chronology and exact-instance semantics are separately grounded.

## First relationship rule opened by this decision

The first lifecycle transition may rely on one grounded relationship only:

```text
new occupancy O
    has exact entry base N
    O.lane_id must resolve to exactly one lane in N
```

If zero or multiple lane instances match, occupancy admission must fail explicitly. Array order, newest version, mutable `current`/`HEAD`, schedule position, actor identity, founder status, or private chat may not choose the lane instance.

This decision does **not** yet define how a newly persisted occupancy becomes part of a successor institutional revision. A stored occupancy object is not automatically current/canonical state.

## Required contract repair before claim/return mutation

Lane 02 should repair only the two created-after-base authoritative relationships:

1. `work-claim.occupancy_id` -> exact typed occupancy reference semantics;
2. `return-packet.claim_id` -> exact typed work-claim reference semantics.

Required regressions:

- bare logical occupancy/claim ids are rejected in the repaired authoritative fields;
- wrong-kind immutable refs are rejected;
- noncanonical immutable ref spellings are rejected through the shared Stage 2 semantic parser, not an approximate second parser;
- two exact occupancy instances with the same logical id produce different work-claim identities when substituted;
- two exact claim instances with the same logical id produce different return-packet identities when substituted;
- a work claim may validly bind an exact occupancy created after its `base_state_revision_ref`;
- a return packet may validly bind an exact claim created after its `base_state_revision_ref`;
- no test or documentation claims those post-base objects were members of the earlier base revision;
- existing uncertainty, overlap-reporting, and handoff fields survive the narrow repair.

## Scope boundary

Do not use this decision to mass-convert every logical relationship into an immutable ref.

Still separate:

- occupancy `claim_ids` chronology/snapshot semantics;
- work-claim `overlap_with_claim_ids` semantics;
- artifact provenance exact-base repair (`ADV-002-C`);
- selective stale-target compatibility (`ADV-002-I`);
- integration receipt exact base/result/packet semantics (`ADV-002-G/H`);
- epoch exact base/member/lane semantics (`ADV-011-C/D/E`);
- durable closure evidence (`ADV-024-A`);
- historical schema reconstruction (`ADV-025-A`);
- lifecycle state-transition publication into successor revisions;
- integration/replay runtime.

## Root grounding

### Truth

A relationship cannot truthfully be resolved from a state that predates the target object's creation. Pre-base objects may use exact-base unique resolution; post-base objects must name the exact created instance.

### Agency / non-domination

No newest/current object, mutable pointer, actor identity, role rank, schedule order, founder status, or Git permission may silently choose which later immutable occupancy or claim a historical lifecycle object meant.

### Continuity

A replacement occupant can reconstruct both kinds of relationship from explicit immutable state: exact base plus deterministic base-local resolution for pre-existing objects, and direct exact refs for post-base objects.

### Wisdom before speed

Repair the temporal relationship contracts before implementing claim/return mutation. A small schema/runtime correction now is cheaper and safer than building a lifecycle engine whose historical references are ambiguous by construction.

## Evidence boundary

This decision is grounded in Decision 006, the integrated exact-base unique resolver, the current occupancy/work-claim/return-packet schemas, and Lane 03's chronology counterexample. It is not evidence that claim opening, packet submission, occupancy admission, successor-revision publication, stale-base enforcement, integration, epochs, or replay already work.
