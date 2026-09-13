# CURRENT WAVE — Institution Fabric

Status: active initial build wave. Stage 1 contracts, Stage 2 deterministic identity, exact revision membership, Stage 3 immutable object storage, exact lifecycle bases, deterministic exactly-one member resolution, Decision 007 relationship chronology, and the three bounded Stage 4 lifecycle-admission primitives — occupancy, work claim, and return packet — are canonical. The current opened gate remains **return-packet output/evidence exact-instance semantics before compatibility**, but canonical integration is now **held on ADV-036 proof-to-use identity drift**. Claim closure, successor-state publication, integration receipts/runtime, epochs/barriers, and replay remain closed.

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable immutable evidence exists.

The immediate requirement is narrower: exact packet/artifact/evidence selection must remain exact when the resolved value is operationally consumed. A verified immutable ref may not sit beside a mutable value that can later acquire different content without detection.

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
- Latest canonical lead decision packet before this wave update: `coordination/returns/01/2026-09-13_ACTIVATION_023.md`, commit `db27a3f80f7936a07c0bcd6cf2f2bb78ca3bbee4`.

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

Compatibility is still closed because packet output/evidence relationships first need exact operational identity.

Current contract facts remain:

- `lane.outputs[]` names output `type` values.
- `lane.evidence_requirements[]` maps output type to required evidence states.
- `artifact.type` exists only on an artifact object.
- `evidence-record.state` exists only on an evidence-record object.
- `return-packet.artifacts_created`, `artifacts_modified`, and `evidence_refs` are strings unless the runtime constrains their operational meaning.
- artifact provenance still records `base_state_revision` without the exact semantics required by `ADV-002-C`.
- `supersedes_ref` still does not by itself express the two-sided modified-artifact relationship required by `ADV-002-I`.

### Lane 02 PR #37 — positive baseline, integration held

PR #37 implements read-only `resolve_return_packet_output_identity(...)` for exact created-artifact and evidence-record selection. It:

- exact-loads one exact immutable return packet;
- requires canonical exact refs for created artifacts and evidence records;
- reuses shared Stage 2 `parse_immutable_ref()` semantics;
- exact-loads selected objects and checks required kind/logical id;
- does not select by logical id, newest object, storage order, mutable current state, actor identity, or hidden history;
- fails closed on any non-empty `artifacts_modified` because the present contract cannot truthfully express both exact observed prior target and exact produced result.

Lane 02 repaired earlier ADV-035 ordinary aliasing by recursively freezing returned JSON into private `dict` / `list` subclasses.

Exact tested repair/workflow head:

`b8a4314b51c8ae46fb7aa907f274c7040a28e674`

Native run `34751400715`, job `103708456304`:

- **166 / 166 passed**;
- **0 failures / 0 errors**;
- ADV-035-A/B/C all passed unchanged;
- explicit compile succeeded.

Final PR #37 branch head after documentation-only return packet:

`af05d8ecc683816cf6e07d14c6c53dbb77975be8`

This remains useful positive evidence. It is **not sufficient for integration** after ADV-036.

### Lane 03 PR #39 — current blocker / repair oracle

PR #39 changes no production runtime. It adds ADV-036-A/B/C against Lane 02's repaired head.

Exact tested Lane 03 head:

`573339670c8cbdf95a20329e8a280fa0046744d5`

Native merge candidate:

`f6a76268df2035f53e8b74612abc8daba762793d`

Run `34751956854`, job `103709893478`:

- **169 tests run**;
- **166 passed**;
- **exactly 3 failed**;
- only ADV-036-A/B/C failed;
- compile skipped after unittest failure.

Observed failure:

```text
private dict/list subclass overrides
    block ordinary mutation
        but
Python builtin base-class mutators
    dict.__setitem__(...)
    list.__setitem__(...)
        bypass subclass overrides
        -> returned operational value changes
        -> paired exact immutable ref does not
        -> exact ref/value contradiction
```

Durable object-store corruption was not observed. The failure is proof-to-use drift in the returned operational value after successful exact verification.

## Current integration decision

**Do not merge PR #37 in its current form.**

Preserve its exact-selection behavior and `artifacts_modified` fail-closed boundary, but repair only the proof-to-use representation/verification invariant before compatibility is opened.

PR #38 retains the original ADV-035 failure evidence. PR #39 is now the newest adversarial boundary.

## Lane 02 — smallest next implementation

Repair only ADV-036.

Required invariant:

```text
exact immutable ref + returned authoritative operational value
    -> must continue to describe the same content
    OR
    -> drift must be detected by mandatory exact reload/reverification
before any compatibility decision consumes that value
```

Requirements:

1. preserve shared Stage 2 exact-ref parsing and exact object-store loading;
2. preserve kind/logical-id verification;
3. preserve created-artifact/evidence direct exact selection;
4. preserve `artifacts_modified` fail-closed behavior;
5. do not silently broaden Stage 2 canonical JSON semantics merely to fit a repair;
6. avoid relying on a mutable builtin-container subclass as the entire adversarial immutability guarantee;
7. rerun full baseline + ADV-035-A/B/C + ADV-036-A/B/C unchanged;
8. require explicit compile success including both adversarial modules;
9. stop before compatibility, provenance/evidence closure, claim closure, successor publication, integration, epochs, or replay.

A non-builtin immutable representation, bounded canonical adapter, exact reload/reverification at consumption, or another mechanism may be acceptable if the invariant is proven. Implementation fashion is not the authority; evidence against the invariant is.

## Lane 03 — next adversarial pass

Wait for Lane 02's exact repaired head, then attack only this proof-to-use surface:

- ADV-035 ordinary mutation;
- ADV-036 builtin base-class mutation;
- nested arrays/maps;
- same-logical-id / different-exact-instance substitution;
- any adapter or re-verification boundary introduced by the repair;
- preservation of the modified-artifact fail-closed boundary.

Do not expand into compatibility or later lifecycle/integration stages.

## Lane 01 — sequencing boundary

Protect this order:

```text
exact output/evidence selection
    -> proof-to-use exact identity continuity
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
- `ADV-036`: builtin base-class mutator bypass is the current active blocker.
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
