# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts, Stage 2 deterministic identity, exact revision membership, Stage 3 immutable object store, exact lifecycle bases, semantic member-ref validation, exact-base exactly-one member resolution, Decision 007 lifecycle chronology, and created-after-base exact authoritative refs are integrated. The first Stage 4 occupancy-admission primitive is now canonical through PR #26, with Lane 03 ADV-032-A/B/C proof-to-write regressions canonical through PR #28. Claim opening is the next bounded Stage 4 slice. Return submission, successor-revision publication, integration, epochs, and replay remain closed.

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable evidence exists.

## Canonical integration state

Already integrated and still canonical:

- Stage 1 canonical contract pack.
- Decisions 001–004: root-grounded integration semantics, immutable identity/reference semantics, cross-runtime canonical portability, and exact canonical JSON string spelling.
- Stage 2 production identity at `11f8e9035d965aaaf4fe21bc857f1cf01a35ca10`.
- Decision 005 exact revision membership.
- Stage 3 immutable object store at `cab7ec2daf4d6e5f7ad5fb67c800c99cf14f7859`.
- Decision 006 exact lifecycle-base semantics through `4f51dea31bd494099266e0e5a13ab34f1b53958b`.
- Shared semantic state-revision member-ref validation at `090b8bde1638eacc277f4df27bf3f254b8225e86`.
- Read-only `resolve_exact_revision_member(...)` through PR #22 / `c28ca8e67afac1e5bdf0286e0e8b80acb6a851e1`, with Lane 03 adversarial regressions through `0dc9745bc3528543d2fb18f0253808399aa6e5af`.
- Decision 007 lifecycle relationship chronology at `05022e2d9f0d9ebcfcc61afdfcf0e8161e09f731`.
- Decision 007 created-after-base exact relationship refs through PR #24 / `10bc3f9e920e482de82f7c11cc17585d15f10a32`, with adversarial regressions through `2d4a3e9b6ede16b66adf202b69383da307d28c52`.
- First Stage 4 occupancy admission through PR #26 / merge `b7c68b7d9212562f159170f40c12d3be7bac86f0`.
- Lane 03 ADV-032-A/B/C occupancy proof-to-write regressions through PR #28 / merge `d3bddb783cf0a4c63405d790404d403b20cfe60c`.
- The obsolete intentionally-failing PR #27 is closed as superseded; its failure evidence remains preserved in canonical return packets rather than erased.

The integrated relationship boundary remains:

```text
pre-existing-at-base target
    -> exact base revision
    -> explicit member family / required kind
    -> exactly one logical-id match
    -> return that exact immutable member
    -> zero / multiple / missing / corrupt => explicit failure

created-after-base authoritative target
    -> bind exact immutable target ref directly
    -> canonical Stage 2 parser + required kind
    -> transition runtime must exact-load target before operational use
```

Forbidden hidden authority remains:

```text
newest version
recency
array order
mutable current/HEAD
occupant identity
schedule order
founder status
private chat memory
```

## Occupancy admission — integrated bounded success

Canonical `admit_occupancy(...)` now:

```text
snapshot one function-owned occupancy candidate
-> validate that same candidate
-> exact-load occupancy.base_state_revision_ref
-> resolve occupancy.lane_id exactly once from lane_refs in that base
-> persist that same exact candidate immutably
-> return exact occupancy_ref + resolved lane_ref
```

Evidence used for integration:

- Lane 02 repaired implementation/workflow head `5c00c5d63540a2e2ae828b3f3b12e91282fd83e5` had native GitHub Actions success on the current-main merge candidate: **114 tests passed / 0 failed / 0 errors**, plus explicit kernel/lifecycle/test `py_compile` success.
- Lane 03 stacked exact-head re-verification on test head `697315e8b5b65b76eb1025c326c2c1d84a50cea5` ran **116 tests / 116 passed / 0 failures / 0 errors**, with ADV-032-A, ADV-032-B, and ADV-032-C all passing and explicit compile succeeding.
- ADV-032-A checks lane relationship drift under final-write caller mutation.
- ADV-032-B checks exact-base rebinding drift under final-write caller mutation.
- ADV-032-C checks whole exact occupancy identity drift through a non-relationship identity-bearing field.
- No tested witness reproduced the earlier proof-to-write contradiction on the repaired implementation.

Bounded claim only: immutable occupancy persistence is **not** successor-revision publication and does not make the occupancy current/canonical institutional state.

## Active Stage 4 gate — first bounded work-claim admission

The next smallest runtime slice is work-claim admission only. This opens `ADV-031-A` for `work-claim.occupancy_ref` while preserving Decision 007 chronology.

### Lane 02 — Deterministic Kernel Engineer

Current claim: implement only a bounded `open_work_claim(...)` / equivalently named primitive. Do not open return submission or successor-state publication.

Required behavior:

1. create one function-owned detached claim candidate before validation/grounding, preserving the occupancy proof-to-write lesson;
2. validate the work-claim contract and require the transition candidate to represent an opening claim (`status == "open"`), without inventing mutable current-state authority;
3. exact-load `base_state_revision_ref` as the named immutable state revision; this proves existence of the claimed work base but does not implement global stale/current policy;
4. resolve `lane_id` exactly once from `lane_refs` in that exact claim base, required kind `lane`; this is the first tested use of Decision 007's pre-existing-at-base rule for a work claim rather than an assumption that every logical lane relation behaves identically;
5. exact-load `occupancy_ref` as the exact immutable occupancy instance before treating it as operationally valid (`ADV-031-A`); wrong-kind, missing, malformed, noncanonical, or corrupt targets must fail explicitly;
6. require the exact occupancy object's logical `lane_id` to equal the claim's `lane_id`; do **not** require occupancy entry base to equal claim base, because later-base claim semantics have not yet been disproven or standardized;
7. if checking occupancy `status`, treat `active` only as a necessary property of that exact snapshot, never as proof that the occupancy is globally current or unsuperseded; do not invent currentness/supersession policy in this slice;
8. do not use `occupancy.claim_ids` or `work-claim.overlap_with_claim_ids` as authoritative dereference/ownership rules; preserve them as snapshot/reporting data only;
9. persist the exact detached claim only after the above dependencies are grounded, return the exact claim ref plus exact occupancy/lane identities, and preserve idempotent same-object storage behavior;
10. add deterministic tests for missing/corrupt/wrong-kind occupancy target, ambiguous/missing lane in exact base, lane mismatch between occupancy and claim, caller mutation at final write, newer/same-logical-id objects elsewhere not rebinding the claim, and successful exact-target persistence;
11. run the complete native suite and explicit compile coverage, publish a bounded return packet, then stop.

Explicitly **not** part of this slice: overlap arbitration/locking, occupancy `claim_ids` mutation, currentness/stale-base policy, actor authorization, scheduler authority, claim supersession/closure, return-packet runtime, successor state revision publication, integration, epochs, or replay.

### Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Wait for Lane 02's exact work-claim-admission head, then attack only that bounded transition. Priority witnesses:

- exact-but-missing or wrong target occupancy cannot become operational merely because `occupancy_ref` is syntactically valid (`ADV-031-A`);
- a later occupancy with the same logical id cannot rebind the claim;
- claim base/lane selection cannot follow newest/current/array order;
- caller mutation after grounding cannot change the exact persisted claim or its occupancy/lane relation while success is returned;
- occupancy/claim lane mismatch cannot be silently accepted;
- overlap arrays and `occupancy.claim_ids` cannot become hidden ownership authority;
- green evidence must not be relabeled as proof of currentness, successor revision publication, integration, epochs, or replay.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, roots, evidence precision, and universal-vs-domain separation;
- keep the work-claim slice bounded to explicit exact-base lane grounding plus exact occupancy-target closure;
- do not let a green object-store mutation silently become a claim of canonical/current institutional state;
- integrate Lane 02 only after deterministic evidence and Lane 03 attack are sufficiently grounded;
- preserve unresolved currentness/stale-base, overlap, closure, provenance, successor-revision, integration, epoch, replay, durability, and portability obligations explicitly;
- keep repository coordination sufficient for a replacement occupant to continue without private chat memory.

Latest lead packet before this wave update: `coordination/returns/01/2026-09-13_ACTIVATION_017.md`.

## Work-claim admission success boundary

A future successful bounded claim-admission implementation may claim only:

```text
work-claim contract/semantic validity
+ exact work base exists and is loadable
+ claim lane resolves exactly once inside that base
+ exact occupancy target exists and exact-loads as occupancy
+ occupancy and claim name the same logical persistent lane
+ proof and publication bind the same exact claim candidate
+ exact work-claim object is immutably persisted
+ exact claim/occupancy/lane identities are returned/preserved
```

It must **not** claim:

```text
claim is canonical/current institutional state
occupancy is globally current/authorized
claim owns or locks scope
semantic overlap has been resolved
occupancy.claim_ids is authoritative
successor state revision exists
return packet accepted
integration happened
epoch/barrier happened
replay proof exists
```

## Frozen downstream obligations

- `ADV-002-C`: artifact provenance base revision must have exact-instance semantics before exact provenance/replay claims.
- `ADV-002-G/H`: integration receipts must bind exact base/result state revisions and exact packet instances before integration/replay claims.
- `ADV-011-C/D/E`: epochs must bind an exact base revision and exact packet membership, with exact or uniquely resolvable lane semantics, before parallel/sequential replay claims.
- `ADV-002-I`: selective stale-target compatibility for modified artifacts must derive or record the exact target instance observed from the packet base.
- `ADV-024-A`: durable closure/evidence state must be bound to an exact revision once closure checking can vary historically.
- `ADV-025-A`: historical schema context must be reconstructable before incompatible schema evolution can coexist with replayable immutable history.
- `ADV-031-A`: authoritative post-base refs must be exact-loaded/identity-verified at transition time before operational relationship claims; the next work-claim slice opens this only for `occupancy_ref`.
- occupancy supersession/currentness/stale-base semantics remain unresolved.
- `occupancy.claim_ids`: snapshot/chronology semantics remain unresolved; do not use as exact dereference authority yet.
- `work-claim.overlap_with_claim_ids`: report/navigation semantics remain unresolved; do not use as exact dereference or ownership authority yet.
- lifecycle successor-revision publication remains unimplemented and must not be implied by immutable object persistence.
- full cross-language reproduction of the identity/resolution stack remains not tested.
- filesystem power-loss durability, concurrent-writer stress, and non-Linux atomic-publication behavior remain not fully proven.

These are obligations, not evidence that the corresponding runtimes exist.

## Shared return-packet minimum

Each lane leaves: base inspected; bounded claim; files changed; evidence/tests; uncertainty/blockers; dependency/downstream effects; next action; and explicit evidence status (`proposed`, `implemented`, `compiled`, `automated_tested`, `runtime_tested`, `measured`, `inferred`, `blocked`, `not_tested`, etc.).

## Merge boundary

Inside AXM, the constitutional merge gate remains:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

No lane, founder, model, specialist, schedule position, CI result, or Git permission becomes authority by identity. When grounding is insufficient, preserve uncertainty or dissent instead of converting confidence into canon.
