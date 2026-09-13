# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts, Stage 2 deterministic identity, exact revision membership, Stage 3 immutable object store, exact lifecycle bases, semantic member-ref validation, exact-base exactly-one member resolution, Decision 007 lifecycle chronology, created-after-base exact authoritative refs, and the first Stage 4 occupancy-admission primitive are canonical. The first bounded work-claim admission exists in PR #29 but is **held** on Lane 03 ADV-033-A/B: exact occupancy object presence is not yet enough proof that the occupancy's own entry-base/lane relationship is grounded. Return submission, successor-revision publication, integration, epochs, and replay remain closed.

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
- Lane 03 Activation 020 ADV-033-A/B blocker packet is preserved on canonical `main` at `coordination/returns/03/2026-09-13_ACTIVATION_020.md`; its adversarial tests remain stacked in PR #30 until the production repair is grounded.

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

The new ADV-033 finding sharpens the second rule for lifecycle objects:

```text
exact target object exists
    != proof that the target's own lifecycle relationships were grounded

operational use of exact occupancy
    -> exact-load occupancy object
    -> exact-load occupancy.base_state_revision_ref
    -> resolve occupancy.lane_id exactly once in that entry base
    -> only then may later work-claim logic rely on that occupancy relation
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
historical call-path assumption
```

## Occupancy admission — integrated bounded success

Canonical `admit_occupancy(...)` remains:

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

Bounded claim only: immutable occupancy persistence is **not** successor-revision publication and does not make the occupancy current/canonical institutional state.

## Active Stage 4 gate — work-claim admission held on ADV-033-A/B

Lane 02 PR #29 implements the first bounded `open_work_claim(...)` candidate. Its current head is `edd41765742343aeff665db0e37e75d6c8209cc7` and current-head GitHub Actions is green. Lane 02's tested implementation baseline reports **133 / 133 passed**, explicit compile success, and preserves exact claim-base lane resolution, exact `occupancy_ref` loading, lane equality, local active-snapshot checking, exact detached-candidate persistence, anti-rebinding, idempotence, and final-write mutation resistance.

Lane 03 PR #30 is stacked directly on PR #29 and adds two adversarial witnesses without production changes. Current head `70d19819b034cf632dbe2ad2e59096d5102a1c7c` reproduces the same contradiction in fresh native CI run `34743103176`, job `103686053386`:

- **135 tests run / 133 passed / 2 failed**;
- failing only ADV-033-A and ADV-033-B;
- ADV-033-A: `ObjectNotFoundError` was not raised for an occupancy whose own exact entry base is missing;
- ADV-033-B: `RevisionMemberAmbiguityError` was not raised for an occupancy whose own entry base contains two exact lane instances sharing the occupancy's logical `lane_id`;
- explicit compile step was skipped because the unittest step failed first.

This is a bounded production blocker, not a rejection of PR #29's existing 133-test baseline.

### Lane 02 — Deterministic Kernel Engineer

Current claim: repair **only ADV-033-A/B on PR #29**. Do not open return submission or successor-state publication.

Required repair boundary:

1. preserve the existing detached work-claim candidate and all already-green PR #29 behavior;
2. after exact-loading `occupancy_ref`, exact-load that occupancy's own `base_state_revision_ref` as `state-revision`;
3. resolve that occupancy's `lane_id` exactly once from the occupancy entry base's `lane_refs`, required kind `lane`;
4. preserve the separate exact claim-base lane resolution already implemented;
5. preserve the claim/occupancy logical lane equality check and local `occupancy.status == "active"` prerequisite without relabeling either as global currentness or authorization;
6. **do not require occupancy entry base == claim base**; legitimate later claim bases remain permitted under Decision 007 chronology;
7. add/adopt ADV-033-A/B regressions into the repaired production branch and keep the existing test proving later claim base may differ from occupancy entry base;
8. run the full native suite and explicit compile coverage, publish a bounded return packet, then stop.

A small read-only helper may be introduced if it genuinely reduces semantic duplication, but do not call a mutating admission routine merely to verify an existing occupancy and do not broaden this repair into lifecycle redesign.

Explicitly **not** part of this repair: occupancy currentness/supersession, actor authorization, scheduler authority, overlap arbitration/locking, occupancy `claim_ids` mutation, claim closure/supersession, return-packet runtime, successor state revision publication, integration, epochs, or replay.

### Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Wait for Lane 02's exact repaired PR #29 head, then rerun the same ADV-033-A/B witnesses against it together with the full native suite. Also verify that:

- legitimate claim base != occupancy entry base remains accepted;
- later same-logical-id occupancy cannot rebind the exact target;
- claim base/lane selection cannot follow newest/current/array order;
- caller mutation after grounding cannot change the exact persisted claim or its occupancy/lane relation;
- overlap arrays and `occupancy.claim_ids` do not become hidden ownership authority;
- green evidence is not relabeled as currentness, authorization, successor revision publication, integration, epochs, or replay.

Do not expand into a new adversarial surface until this repair is evaluated.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- hold PR #29 narrowly on ADV-033-A/B while preserving its successful evidence;
- preserve Lane 03's blocker packet in canonical repository state without merging the stacked intentionally failing PR #30 into production;
- keep the repair scoped to re-grounding the exact occupancy's own entry-base/lane relationship before operational use;
- do not let generic immutable-store presence inherit lifecycle-admission authority from hidden call-path convention;
- do not let a future green object-store mutation silently become a claim of canonical/current institutional state;
- integrate only after Lane 02 repair evidence and Lane 03 exact-head re-attack are sufficiently grounded;
- preserve unresolved currentness/stale-base, overlap, closure, provenance, successor-revision, integration, epoch, replay, durability, and portability obligations explicitly;
- keep repository coordination sufficient for a replacement occupant to continue without private chat memory.

Latest lead packet before this wave update: `coordination/returns/01/2026-09-13_ACTIVATION_018.md`.

## Work-claim admission success boundary

A future successful bounded claim-admission implementation may claim only:

```text
work-claim contract/semantic validity
+ exact work base exists and is loadable
+ claim lane resolves exactly once inside that base
+ exact occupancy target exists and exact-loads as occupancy
+ occupancy's own exact entry base exists and is loadable
+ occupancy lane resolves exactly once inside its own entry base
+ occupancy and claim name the same logical persistent lane
+ proof and publication bind the same exact claim candidate
+ exact work-claim object is immutably persisted
+ exact claim/occupancy/lane identities are returned/preserved
```

It must **not** claim:

```text
claim is canonical/current institutional state
occupancy is globally current/authorized/unsuperseded
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
- `ADV-031-A`: authoritative post-base refs must be exact-loaded/identity-verified at transition time before operational relationship claims; the work-claim slice opens this only for `occupancy_ref`.
- `ADV-033-A/B`: exact occupancy object presence does not prove the occupancy's own historical entry-base/lane relationship; operational work-claim use must re-ground that relationship unless a future explicit durable closure proof supersedes this mechanism.
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
