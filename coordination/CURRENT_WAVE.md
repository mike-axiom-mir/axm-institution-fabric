# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts integrated; Stage 2 deterministic identity integrated; exact revision membership integrated; Stage 3 immutable object store integrated; Decision 006 exact lifecycle bases integrated; shared semantic member-ref validation integrated; exact-base exactly-one member resolution integrated; Decision 007 lifecycle chronology and created-after-base exact authoritative refs integrated. The first Stage 4 occupancy-admission implementation now exists in PR #26, but **integration is held narrowly on ADV-032-A proof-to-write continuity**. The stacked Lane 03 challenge in PR #27 found the production failure, and its regression harness itself needs one repair so it can accept a legitimate detached-candidate fix. Claim opening, return submission, successor-revision publication, integration, epochs, and replay remain closed.

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

## Active Stage 4 gate — occupancy admission held on ADV-032-A

### Lane 02 PR #26 baseline

PR #26 implements only bounded occupancy admission:

```text
validate proposed occupancy
-> exact-load occupancy.base_state_revision_ref
-> resolve occupancy.lane_id exactly once from lane_refs in that base
-> persist occupancy immutably
-> return exact occupancy_ref + resolved lane_ref
```

Its native baseline evidence remains useful:

- tested implementation/workflow head `09d40747015004c524668801510332d57fd83783`;
- **113 tests passed / 0 failed / 0 errors** observed by Lane 03 from the native job log;
- explicit lifecycle/kernel/test `py_compile` succeeded;
- final PR head `8d2ab4484d4d4c3a6f330af01780842c8cadb3e5` adds only its return packet after the tested implementation head.

That evidence does **not** close proof-to-publication continuity.

### ADV-032-A — observed production blocker

Lane 03 PR #27 added a deterministic final-write mutation witness against the exact PR #26 implementation.

Observed native challenge evidence:

- run `34735767696`, job `103666797891`;
- **114 tests run / 1 failure**;
- the only failure is ADV-032-A;
- observed contradiction: admission grounded `lane-02` but persisted occupancy `lane_id = lane-decoy`;
- compile step skipped because the failing unittest step stopped the job.

The failure exists because `validate_instance(...)` validates but returns the same caller-owned mutable mapping. PR #26 then uses that mapping for relationship grounding and later publication. A caller-side mutation between proof and store publication can therefore make durable state disagree with the returned grounded lane identity.

This is a blocking continuity failure. Successful admission must bind proof and publication to one exact candidate or reject drift explicitly.

### Lane 01 evidence-quality finding on PR #27

The ADV-032-A **finding remains valid**, but the current adversarial regression is not yet suitable as canonical repair evidence.

`AliasingProbeStore.store(...)` currently requires:

```text
value is caller_occupancy
```

and raises `AssertionError` when the production function passes a detached/function-owned snapshot to the store.

That contradicts the test's own stated acceptable repaired outcome: a successful admission using an internal frozen/snapshotted candidate. A correct snapshot repair would still fail the current probe for the wrong reason.

Required evidence-only repair for PR #27:

```text
mutate caller_occupancy at the final write boundary
DO NOT require store(value) to receive the same object identity

aliased implementation
    -> mutation reaches published candidate
    -> invariant fails

function-owned detached candidate
    -> caller mutation cannot alter published candidate
    -> invariant passes

explicit identity-drift rejection
    -> fail closed before contradictory publication
    -> acceptable
```

This test-harness issue does not reduce the production blocker; it only prevents the current regression from fairly verifying one of the allowed repairs.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, roots, evidence precision, and universal-vs-domain separation;
- hold PR #26 narrowly on ADV-032-A rather than discarding its grounded baseline work;
- require PR #27 to become repair-safe before its regression is canonicalized;
- avoid duplicating Lane 02 production implementation or Lane 03 adversarial implementation while those specialists are active;
- keep claim opening, packet submission, successor-revision publication, integration, epoch runtime, and replay closed;
- preserve `ADV-024-A`, `ADV-025-A`, `ADV-031-A`, provenance, stale-target, integration-receipt, epoch, portability, and cross-language obligations explicitly;
- maintain repository state so another occupant can reconstruct the hold without private chat memory.

Latest lead packet: `coordination/returns/01/2026-09-13_ACTIVATION_016.md`.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **repair only ADV-032-A on PR #26 after the adversarial regression is made repair-safe; do not open further lifecycle stages.**

Required bounded repair:

1. start from the exact current PR #26 occupancy-admission behavior;
2. freeze/detach one function-owned occupancy candidate before dependency grounding;
3. use the same candidate through contract validation, exact base load, lane resolution, exact identity derivation, and final publication;
4. alternatively/additionally derive and bind an exact expected occupancy reference so later identity drift becomes explicit failure;
5. do not let caller mutation after grounding silently change authoritative `base_state_revision_ref`, `lane_id`, or any other identity-bearing occupancy content before publication;
6. preserve all existing 113-test baseline behavior;
7. include the repair-safe ADV-032-A regression in normal test/compile coverage;
8. rerun the complete native suite and explicit compilation;
9. publish a bounded return packet and stop.

Do **not** generalize this into locks, actor authorization, scheduler semantics, stale-base/currentness policy, occupancy supersession, claim creation, successor revision publication, integration, epochs, or replay.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Immediate current claim: **repair only the ADV-032-A regression harness in PR #27; do not change production runtime.**

Required evidence-only repair:

1. remove the requirement that the value passed to `store()` be the original caller-owned mapping;
2. mutate only `caller_occupancy` at the final occupancy write boundary;
3. preserve the durable invariant check that persisted occupancy + exact base must reconstruct the same exact `lane_ref` returned by admission;
4. verify the current aliased PR #26 implementation still fails for the real contradiction;
5. stop.

After Lane 02 repairs PR #26, Lane 03 should attack the exact repaired production head again. Required success evidence must show both the original baseline behavior and ADV-032-A are green without opening later lifecycle stages.

## Occupancy-admission success boundary

Once ADV-032-A is repaired and adversarially reverified, success may claim only:

```text
occupancy contract/semantic validity
+ exact base exists and is loadable
+ occupancy lane resolves exactly once inside that base
+ proof and publication bind the same exact occupancy candidate
+ exact occupancy object is immutably persisted
+ exact resolved lane identity is returned/preserved
```

Success must **not** claim:

```text
occupancy is now canonical/current institutional state
successor state revision exists
claim ledger exists
claim opened
return packet accepted
artifact/dependency mutation occurred
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
- `ADV-031-A`: authoritative post-base refs must be exact-loaded/identity-verified at transition time before operational relationship claims.
- `occupancy.claim_ids`: snapshot/chronology semantics remain unresolved; do not use as exact dereference authority yet.
- `work-claim.overlap_with_claim_ids`: report/navigation semantics remain unresolved; do not use as exact dereference authority yet.
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
