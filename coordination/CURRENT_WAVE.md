# CURRENT WAVE — Institution Fabric

Status: active initial build wave. Stage 1 contracts, Stage 2 deterministic identity, exact revision membership, Stage 3 immutable object storage, exact lifecycle bases, deterministic exactly-one member resolution, Decision 007 relationship chronology, and the three bounded Stage 4 lifecycle-admission primitives — occupancy, work claim, and return packet — are canonical. The current opened gate remains **return-packet output/evidence exact-instance semantics before compatibility**, but canonical integration is now **held on ADV-037 proof-to-use JSON transport drift**. Claim closure, successor-state publication, integration receipts/runtime, epochs/barriers, and replay remain closed.

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable immutable evidence exists.

The immediate requirement is narrower: exact packet/artifact/evidence selection must remain exact when the resolved value is operationally consumed or transported. A verified immutable ref may not sit beside an authoritative value that can later be emitted as different semantic content without explicit failure.

## Constitutional merge boundary

Inside AXM, the constitutional merge gate remains:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

No lane, founder, model, specialist, schedule position, CI result, or Git permission becomes authority by identity. When grounding is insufficient, preserve uncertainty or dissent instead of converting confidence into canon.

## Canonical integration spine

Key canonical milestones remain:

- Stage 1 canonical contract pack.
- Decisions 001–004: root-grounded integration, immutable identity/reference semantics, cross-runtime canonical portability, and canonical string spelling.
- Stage 2 production identity: `11f8e9035d965aaaf4fe21bc857f1cf01a35ca10`.
- Decision 005 exact revision membership.
- Stage 3 immutable object store: `cab7ec2daf4d6e5f7ad5fb67c800c99cf14f7859`.
- Decision 006 exact lifecycle-base semantics through `4f51dea31bd494099266e0e5a13ab34f1b53958b`.
- Shared semantic state-revision member-ref validation: `090b8bde1638eacc277f4df27bf3f254b8225e86`.
- Read-only exact-base exactly-one resolver through PR #22 / `c28ca8e67afac1e5bdf0286e0e8b80acb6a851e1`, with Lane 03 regression evidence through `0dc9745bc3528543d2fb18f0253808399aa6e5af`.
- Decision 007 lifecycle relationship chronology: `05022e2d9f0d9ebcfcc61afdfcf0e8161e09f731`.
- Created-after-base exact occupancy/claim relationship refs through PR #24 / `10bc3f9e920e482de82f7c11cc17585d15f10a32`, with Lane 03 adversarial evidence through `2d4a3e9b6ede16b66adf202b69383da307d28c52`.
- Bounded occupancy admission through PR #26 / `b7c68b7d9212562f159170f40c12d3be7bac86f0`, with ADV-032-A/B/C through PR #28 / `d3bddb783cf0a4c63405d790404d403b20cfe60c`.
- Bounded work-claim admission through PR #29 / `db769438a2dfdcd7e17a8acc4a116b7a37b32855`, with ADV-033-C through PR #32 / `26c3c89400a1cfbc314d1742d575ebd1063d5d70`.
- Bounded return-packet admission through PR #33 / `62a1533e901e6ecef825a0b103ecf87e6a23e620`.
- ADV-034-A/B/C/D return-packet continuity regressions on canonical-main integration head `13ceeac1b5930b00458a66dd6db85913c311752c`: native run `34748872041`, job `103701628200`, **151/151 passed**, explicit compile success.
- Latest canonical lead decision packet: `coordination/returns/01/2026-09-13_ACTIVATION_024.md`, commit `c715798f0e619f76bacf7d45a4d373aa86692cf6`.

## Integrated lifecycle relationship boundary

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
    != proof that its own historical relationships were grounded

operational use of exact lifecycle object
    -> exact-load object
    -> reconstruct each historical relationship relied on by the transition
    -> only then use it operationally
```

Forbidden hidden authority remains:

```text
newest version
storage recency
array order
mutable current / HEAD
occupant identity
schedule order
founder status
private chat memory
historical call-path assumption
technical write permission
```

## Stage 4 lifecycle admission — canonical bounded success

### Occupancy

`admit_occupancy(...)` freezes one candidate, validates it, exact-loads its entry base, exactly-one resolves its lane in that base, persists that same detached candidate, and returns exact occupancy/lane identities.

It does **not** publish a successor revision or establish global currentness/authorization.

### Work claim

`open_work_claim(...)` freezes one claim candidate, validates it, exact-loads its claim base, exactly-one resolves the claim lane, exact-loads authoritative `occupancy_ref`, reconstructs the occupancy's own entry-base/lane relation, requires claim/occupancy logical-lane consistency and the exact occupancy snapshot's local `active` state, persists the same detached candidate, and returns exact claim/occupancy/lane identities.

Occupancy entry base may differ from later claim base. Snapshot fields such as `occupancy.claim_ids` and `work-claim.overlap_with_claim_ids` remain non-authoritative.

### Return packet

`submit_return_packet(...)` snapshots one function-owned packet candidate; validates it; exact-loads the packet base, exact claim, claim historical lane relation, exact occupancy, and occupancy historical entry-lane relation; requires the local exact claim to be `open` and occupancy `active`; persists the same detached packet candidate; and returns exact packet/claim/occupancy/lane identities.

Bounded claim only: immutable packet persistence is **not** packet acceptance, evidence closure, claim closure, successor-state publication, or integration.

## Active gate — return-packet output/evidence exact-instance semantics

Compatibility is still closed because packet output/evidence relationships first need exact operational identity across use and transport boundaries.

Current contract facts remain:

- `lane.outputs[]` names output `type` values.
- `lane.evidence_requirements[]` maps output type to required evidence states.
- `artifact.type` exists only on an artifact object.
- `evidence-record.state` exists only on an evidence-record object.
- `return-packet.artifacts_created`, `artifacts_modified`, and `evidence_refs` are strings unless the runtime constrains their operational meaning.
- artifact provenance still records `base_state_revision` without the exact semantics required by `ADV-002-C`.
- `supersedes_ref` still does not by itself express the two-sided modified-artifact relationship required by `ADV-002-I`.

### Lane 02 PR #37 — exact selection + ADV-036 repair, integration still held

PR #37 implements read-only `resolve_return_packet_output_identity(...)` for exact created-artifact and evidence-record selection. It:

- exact-loads one exact immutable return packet;
- requires canonical exact refs for created artifacts and evidence records;
- reuses shared Stage 2 `parse_immutable_ref()` semantics;
- exact-loads selected objects and checks required kind/logical id;
- does not select by logical id, newest object, storage order, array order, current/HEAD state, actor identity, or hidden history;
- fails closed on any non-empty `artifacts_modified` because the present contract cannot truthfully express both exact observed prior target and exact produced result.

Lane 02 first repaired ADV-035 ordinary aliasing with recursively frozen builtin-container subclasses. ADV-036 then demonstrated that builtin base-class mutators could bypass those overrides.

Lane 02 Activation 023 repaired ADV-036 using tuple-backed non-`dict` / non-`list` operational views plus a bounded `__class__` compatibility view for the existing Stage 2 `isinstance(..., dict/list)` path.

Exact tested repair/workflow head:

`88836bc6ff47a1010ca4080102d0a447055fff9a`

Final documentation head:

`69b741bbc22c006289fccb2d27ed7c75b3703588`

Native run `34753966159`, job `103715090370`:

- complete unittest discovery: **success**;
- ADV-035-A/B/C and adopted ADV-036-A/B/C: **green through unchanged discovery**;
- explicit compile: **success**;
- numerical `169` count: **source-accounting inference**, not directly observed stdout on that run.

This is valid positive evidence for the demonstrated mutation paths. It is **not sufficient for integration** after ADV-037.

### Lane 03 PR #40 — current blocker / repair oracle

PR #40 changes no production runtime. It adds ADV-037-A/B against Lane 02's tuple-backed repair.

The tests accept either:

1. explicit stdlib JSON serialization rejection; or
2. successful JSON transport that round-trips to the same exact immutable ref.

They fail only on silent semantic drift.

Exact tested Lane 03 head:

`fbdb2ea4f56a53e03854f0bf0efb61d3d604ee3e`

Native merge candidate:

`11f34721881ea5e4ad5be7e515049f2176f2ac79`

Run `34754749509`, job `103717127039` directly reports:

- **171 tests run**;
- **169 passed**;
- **exactly 2 failed**;
- only ADV-037-A/B failed;
- prior ADV-035-A/B/C and ADV-036-A/B/C remained green;
- compile skipped after unittest failure.

Observed failure:

```text
tuple-backed _FrozenDict
    -> exact identity path reads it through __class__ compatibility view
    -> Python stdlib json.dumps accepts real tuple-backed runtime type
    -> serializes iteration as JSON array of keys
    -> values / nested relationship meaning are discarded
    -> json.loads returns array, not object
    -> original exact immutable ref cannot be reproduced
```

Representative artifact transport output:

```text
["content_ref","dependency_refs","evidence_refs","id","provenance","schema_version","type","version"]
```

Representative packet transport output:

```text
["artifacts_created","artifacts_modified","base_state_revision_ref","changes","claim_ref","downstream_effects","evidence_refs","failures_or_blockers","id","lane_id","requested_followup","schema_version","uncertainties"]
```

Durable object-store corruption was not observed. The failure is proof-to-use/transport drift after successful exact verification.

## Current integration decision

**Do not merge PR #37 in its current form.**

Preserve its exact-selection behavior, ADV-035/ADV-036 closure, and `artifacts_modified` fail-closed boundary, but repair only the exposed JSON transport contradiction before compatibility is opened.

**Treat PR #40 as adversarial evidence / repair oracle, not production runtime.** Its witnesses do not require generic JSON-transport support; explicit rejection is acceptable. They only forbid successful transport into different meaning.

PR #38 retains the original ADV-035 failure evidence. PR #39 retains the ADV-036 failure evidence. They are historical/adversarial evidence, not current production candidates.

## Lane 02 — smallest next implementation

Repair only ADV-037.

Required invariant:

```text
exact immutable ref + authoritative operational value
    -> exposed ordinary JSON transport must either
       A. reject explicitly before emitting different meaning
       OR
       B. round-trip to the same exact immutable ref
```

Requirements:

1. preserve shared Stage 2 exact-ref parsing and exact object-store loading;
2. preserve kind/logical-id verification;
3. preserve created-artifact/evidence direct exact selection;
4. preserve ADV-035 ordinary-mutation closure;
5. preserve ADV-036 builtin-base-class mutation closure;
6. preserve `artifacts_modified` fail-closed behavior;
7. adopt/rerun ADV-037-A/B unchanged;
8. rerun full native unittest discovery and explicit compile;
9. stop before compatibility, provenance/evidence closure, claim closure, successor publication, integration, epochs, or replay.

A dedicated immutable mapping/sequence representation, bounded exact transport adapter, exact reload/reverification around materialization, explicit unsupported-transport rejection, or another mechanism may be acceptable if the invariant is proven. Implementation fashion is not authority; evidence against the invariant is.

## Lane 03 — next adversarial pass

Wait for Lane 02's exact ADV-037 repaired head, then attack only this proof-to-use/transport surface:

- ADV-035 ordinary mutation;
- ADV-036 builtin base-class mutation;
- ADV-037 JSON transport drift;
- nested arrays/maps;
- same-logical-id / different-exact-instance substitution;
- any adapter/materialization/reverification boundary introduced by the repair;
- preservation of the modified-artifact fail-closed boundary.

Do not expand into compatibility or later lifecycle/integration stages.

## Lane 01 — sequencing boundary

Protect this order:

```text
exact output/evidence selection
    -> proof-to-use exact identity continuity
    -> proof-to-transport exact identity continuity or explicit rejection
    before
packet output/evidence compatibility
    before
claim closure / successor revision publication
    before
integration / epochs / replay
```

Do not promote domain-specific output policy into the universal kernel.

## Frozen downstream obligations

- `ADV-002-C`: artifact provenance base revision needs exact-instance semantics before exact provenance/replay claims.
- `ADV-002-I`: modified-artifact semantics must represent/derive both exact observed prior target and exact produced result; stale-target compatibility remains unresolved.
- `ADV-002-G/H`: integration receipts must bind exact base/result revisions and exact packet instances before integration/replay claims.
- `ADV-011-C/D/E`: epochs must bind exact base revision and exact packet membership before parallel/sequential replay claims.
- `ADV-024-A`: durable closure/evidence state must bind an exact revision once closure checking can vary historically.
- `ADV-025-A`: historical schema context must remain reconstructable before incompatible schema evolution coexists with replayable history.
- `ADV-031-A`: authoritative post-base refs must be exact-loaded/identity-verified before operational relationship use.
- `ADV-033-A/B/C`: exact lifecycle object presence does not prove the object's historical relationships; later transitions re-ground relationships they rely on unless a future explicit closure proof supersedes that mechanism.
- `ADV-034-A/B/C/D`: packet admission remains exact-base/exact-claim grounded and detached handoff content remains stable through publication.
- `ADV-035`: ordinary proof-to-use aliasing must remain closed after any new repair.
- `ADV-036`: builtin base-class mutator bypass must remain closed after any new repair.
- `ADV-037`: successful JSON transport must not silently change exact operational meaning; explicit rejection remains acceptable.
- occupancy/claim global currentness, supersession, authorization, and stale-base semantics remain unresolved.
- multiple exact packets for one claim need explicit future selection/conflict semantics.
- artifact/evidence closure remains unimplemented.
- packet output/evidence compatibility remains unimplemented.
- claim closure/status-transition publication remains unimplemented.
- successor state revision publication remains unimplemented.
- integration runtime, epochs/barriers, and replay remain unimplemented.
- full cross-language reproduction remains untested.
- filesystem power-loss durability, concurrent-writer stress, and non-Linux atomic-publication behavior remain not fully proven.

These are obligations, not evidence that the corresponding runtimes exist.

## Shared return-packet minimum

Each specialist leaves repository evidence containing: base inspected; bounded claim; files/behavior changed; exact evidence/tests; uncertainty/blockers; dependency/downstream effects; next action; and explicit evidence status (`proposed`, `implemented`, `compiled`, `automated_tested`, `runtime_tested`, `measured`, `inferred`, `blocked`, `not_tested`, etc.).