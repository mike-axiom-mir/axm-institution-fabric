# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts, Stage 2 deterministic identity, exact revision membership, Stage 3 immutable object store, exact lifecycle bases, semantic member-ref validation, exact-base exactly-one member resolution, Decision 007 lifecycle chronology, created-after-base exact authoritative refs, and the first two bounded Stage 4 transitions — occupancy admission and work-claim admission — are canonical. Return-packet submission is the next opened Stage 4 gate. Successor-revision publication, integration, epochs/barriers, and replay remain closed.

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
- First bounded Stage 4 work-claim admission through PR #29 / merge `db769438a2dfdcd7e17a8acc4a116b7a37b32855`.
- Lane 03 ADV-033-C compound work-claim continuity regression and Activation 021 evidence preserved through PR #32 / merge `26c3c89400a1cfbc314d1742d575ebd1063d5d70`.
- Lane 03 Activation 020 preserves the original ADV-033-A/B failing witness in canonical history. The obsolete intentionally failing PR #30 and the superseded stacked PR #31 are closed without force-rewriting their history.

There are currently no open PRs.

## Integrated relationship boundary

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
    -> transition runtime exact-loads target before operational use

exact lifecycle object exists
    != proof that the target's own historical lifecycle relationships were grounded

operational use of an exact lifecycle object
    -> exact-load the object
    -> reconstruct the specific historical relationships the next transition relies on
    -> only then may later lifecycle logic rely on those relationships
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
technical write permission
```

## Occupancy admission — canonical bounded success

Canonical `admit_occupancy(...)`:

```text
snapshot one function-owned occupancy candidate
-> validate that same candidate
-> exact-load occupancy.base_state_revision_ref
-> resolve occupancy.lane_id exactly once from lane_refs in that base
-> persist that same exact candidate immutably
-> return exact occupancy_ref + resolved lane_ref
```

Evidence used for integration:

- Lane 02 repaired implementation/workflow head `5c00c5d63540a2e2ae828b3f3b12e91282fd83e5`: **114 tests passed / 0 failed / 0 errors**, plus explicit kernel/lifecycle/test `py_compile` success.
- Lane 03 exact-head re-verification on test head `697315e8b5b65b76eb1025c326c2c1d84a50cea5`: **116 / 116 passed**, with ADV-032-A/B/C passing and explicit compile succeeding.

Bounded claim only: immutable occupancy persistence is **not** successor-revision publication and does not make the occupancy current/canonical institutional state.

## Work-claim admission — canonical bounded success

Canonical `open_work_claim(...)` now:

```text
snapshot one function-owned work-claim candidate
-> validate candidate and require local status == open
-> exact-load claim.base_state_revision_ref
-> resolve claim.lane_id exactly once from that claim base
-> exact-load authoritative exact occupancy_ref
-> exact-load occupancy.base_state_revision_ref
-> resolve occupancy.lane_id exactly once from the occupancy entry base
-> require occupancy and claim to name the same persistent logical lane
-> require only the exact occupancy snapshot's local status == active
-> persist the same exact detached claim candidate
-> return exact claim_ref + occupancy_ref + claim-base lane_ref
```

Important chronology rule: occupancy entry base may differ from claim base. Each relationship is grounded against its own exact historical base.

Evidence used for integration:

- Lane 02 repaired implementation/workflow head `0d7d45c9b92386c0f487e4ade507454d2c5c162c` had native Actions run `34744810285`, job `103690636832`: **135 / 135 passed, 0 failures, 0 errors**, including ADV-033-A/B and the later-claim-base chronology regression; explicit compile succeeded.
- Lane 03 Activation 021 independently re-attacked the repaired surface and added ADV-033-C. Its native CI succeeded for the full deterministic test step and explicit compile. The numeric count of **136** is source-accounted from the observed 135-test Lane 02 baseline plus exactly one new discovered test method, rather than directly exposed stdout.
- After PR #29 became canonical, Lane 01 reapplied exactly the ADV-033-C test content and preserved Lane 03's packet on a fresh main-based PR #32 rather than force-rewriting the specialist branch. Fresh run `34746504043`, job `103695295361`, succeeded in both the full deterministic-test step and explicit compile before PR #32 was integrated.

ADV-033-C verifies that:

- occupancy entry base and later claim base can remain distinct exact revisions;
- each base resolves its own exact lane relation;
- array order and a newer same-logical-id lane elsewhere do not choose the claim lane;
- a later same-logical-id occupancy cannot rebind the exact `occupancy_ref`;
- `occupancy.claim_ids` and `work-claim.overlap_with_claim_ids` remain preserved snapshot/reporting data rather than ownership authority.

Bounded claim only: immutable work-claim persistence is **not** successor-revision publication and does not establish global currentness, authorization, scope ownership, overlap arbitration, or claim closure.

## Active Stage 4 gate — bounded return-packet admission

The next smallest transition is return-packet admission only. Do not open successor-state publication or integration in the same lane.

Decision 006 already requires `return-packet.base_state_revision_ref` to name one exact revision. Decision 007 already requires `return-packet.claim_ref` to bind the exact work-claim instance created after that base. `NEXT_BUILD.md` also requires packet/base mismatch detection. The next runtime must therefore prove the relationships it relies on rather than inherit them from generic object-store presence.

### Lane 02 — Deterministic Kernel Engineer

Current claim: implement only a bounded return-packet admission primitive, then stop for adversarial review.

Required boundary:

1. create one function-owned deep snapshot of the caller's return-packet candidate before validation or dependency grounding;
2. validate `return-packet.schema.json`, preserving all changes, artifact lists, evidence refs, uncertainties, failures/blockers, downstream effects, and requested follow-up exactly;
3. exact-load `packet.base_state_revision_ref` as a state revision;
4. exact-load authoritative `packet.claim_ref` as a work claim;
5. require `packet.base_state_revision_ref == claim.base_state_revision_ref`; a packet for a claim must preserve that claim's exact work base rather than silently rebase the handoff;
6. require `packet.lane_id == claim.lane_id`;
7. before operationally relying on the exact claim, re-ground the claim relation rather than assuming the claim must previously have passed `open_work_claim(...)`:
   - exact-load the claim's own base;
   - exactly-one resolve claim `lane_id` from that base's `lane_refs`;
   - exact-load claim `occupancy_ref`;
   - exact-load the occupancy's entry base;
   - exactly-one resolve occupancy `lane_id` from that entry base;
   - require occupancy and claim logical lane equality;
8. require the exact claim snapshot's local `status == "open"` and exact occupancy snapshot's local `status == "active"` only as local prerequisites; do **not** relabel them as global currentness, authorization, or unsuperseded state;
9. persist the same exact detached return-packet candidate immutably;
10. return exact packet/claim/occupancy/lane identities sufficient for the next transition to verify what was grounded;
11. do not mutate the immutable claim to `submitted` and do not synthesize a successor revision in this slice.

Required regressions should include at least:

- missing/wrong-kind/corrupt exact `claim_ref` fails before packet publication;
- packet base != exact claim base fails explicitly;
- packet lane != claim lane fails explicitly;
- a schema-valid claim direct-stored with missing/ambiguous historical base/lane relation cannot become operational merely because the exact claim object exists;
- the claim's exact occupancy relation is re-grounded, including the occupancy's own historical entry-base/lane relation;
- later same-logical-id claims, occupancies, or lanes cannot rebind exact historical relationships;
- caller mutation during final publication cannot change the packet whose relationships were proved;
- idempotent re-admission of the same exact packet remains deterministic;
- uncertainty, blockers, evidence refs, changes, downstream effects, requested follow-up, and artifact arrays survive exactly;
- no test gives `occupancy.claim_ids`, `work-claim.overlap_with_claim_ids`, storage recency, array order, or newest/current pointers hidden authority.

Explicitly outside this slice:

- artifact provenance closure or artifact modification compatibility;
- dereferencing/validating artifact or evidence refs beyond what the existing contract already proves structurally;
- full lane output-type compatibility and evidence-requirement satisfaction;
- global occupancy/claim currentness or supersession;
- actor authorization or scheduler authority;
- overlap ownership/arbitration/locking;
- claim closure/status transition publication;
- successor state-revision publication;
- integration receipt generation;
- epochs/barriers;
- replay.

If implementing this packet relation reveals that lane-output/evidence compatibility cannot be truthfully separated, preserve that as a blocker/return packet rather than inventing domain-specific kernel behavior.

### Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Wait for Lane 02's exact return-packet admission head. Then attack only that surface before later stages open.

Primary attack targets:

- exact packet claim binding cannot be replaced by logical-id/newest/current lookup;
- direct immutable-store presence of a claim cannot launder an ungrounded claim or occupancy relationship;
- packet base mismatch cannot be silently treated as a rebase;
- packet lane cannot be borrowed from another base or array position;
- proof-to-write caller aliasing cannot alter the persisted packet after grounding;
- uncertainty/failure/evidence/downstream arrays cannot be dropped or normalized away;
- artifact/evidence arrays must not silently acquire closure or quality authority not actually verified;
- local `open`/`active` snapshots must not be relabeled as authorization/currentness;
- green packet evidence must not be relabeled as successor revision, integration, epoch, or replay proof.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- keep return-packet admission bounded to exact lifecycle grounding and proof-to-write continuity;
- prevent generic immutable-store presence from becoming lifecycle authority;
- preserve the distinction between packet persistence and canonical successor-state publication;
- do not force artifact provenance, evidence closure, lane output compatibility, integration, epoch, or replay semantics into this transition without separate evidence;
- integrate only after Lane 02's exact-head evidence and Lane 03's adversarial re-attack are sufficiently grounded;
- keep repository coordination sufficient for a replacement occupant to continue without private chat memory.

Latest lead packet after the work-claim integration: `coordination/returns/01/2026-09-13_ACTIVATION_020.md`.

## Work-claim admission success boundary

Canonical work-claim admission may claim only:

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
- `ADV-031-A`: authoritative post-base refs must be exact-loaded/identity-verified at transition time before operational relationship claims; work-claim admission applies this to `occupancy_ref`, and return-packet admission must apply it to `claim_ref`.
- `ADV-033-A/B/C`: exact lifecycle object presence does not prove its historical relationships; operational use must re-ground the relationships the next transition relies on unless a future explicit durable closure proof supersedes this mechanism.
- occupancy and claim supersession/currentness/stale-base semantics remain unresolved.
- `occupancy.claim_ids`: snapshot/chronology semantics remain unresolved; do not use as exact dereference authority yet.
- `work-claim.overlap_with_claim_ids`: report/navigation semantics remain unresolved; do not use as exact dereference or ownership authority yet.
- lifecycle successor-revision publication remains unimplemented and must not be implied by immutable object persistence.
- packet output/evidence compatibility remains a separate Stage 4 obligation after exact packet admission unless evidence requires coupling.
- full cross-language reproduction of the identity/resolution stack remains not tested.
- filesystem power-loss durability, concurrent-writer stress, and non-Linux atomic-publication behavior remain not fully proven.

These are obligations, not evidence that the corresponding runtimes exist.

## Shared return-packet minimum

Each specialist lane leaves: base inspected; bounded claim; files changed; evidence/tests; uncertainty/blockers; dependency/downstream effects; next action; and explicit evidence status (`proposed`, `implemented`, `compiled`, `automated_tested`, `runtime_tested`, `measured`, `inferred`, `blocked`, `not_tested`, etc.).

## Merge boundary

Inside AXM, the constitutional merge gate remains:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

No lane, founder, model, specialist, schedule position, CI result, or Git permission becomes authority by identity. When grounding is insufficient, preserve uncertainty or dissent instead of converting confidence into canon.
