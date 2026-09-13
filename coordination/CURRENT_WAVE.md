# CURRENT WAVE — Institution Fabric

Status: active initial build wave. Stage 1 contracts, Stage 2 deterministic identity, exact revision membership, Stage 3 immutable object storage, exact lifecycle bases, deterministic exactly-one member resolution, Decision 007 relationship chronology, and all three bounded Stage 4 lifecycle-admission primitives — occupancy, work claim, and return packet — are now canonical. Lane 03 ADV-034 return-packet continuity regressions are also canonical. The next opened gate is **return-packet output/evidence exact-instance semantics before compatibility**. Claim closure, successor-state publication, integration receipts/runtime, epochs/barriers, and replay remain closed.

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable immutable evidence exists.

## Canonical integration spine

Canonical milestones remain:

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
- Bounded work-claim admission through PR #29 / `db769438a2dfdcd7e17a8acc4a116b7a37b32855`, with ADV-033-C and Lane 03 Activation 021 through PR #32 / `26c3c89400a1cfbc314d1742d575ebd1063d5d70`.
- Bounded return-packet admission through PR #33 / merge `62a1533e901e6ecef825a0b103ecf87e6a23e620`.
- Lane 03 ADV-034-A/B/C/D exact return-packet adversarial regressions, preserved on fresh canonical-main integration head `13ceeac1b5930b00458a66dd6db85913c311752c` after the original stacked PR #34 became awkward to retarget. Native Actions run `34748872041`, job `103701628200`: **151 / 151 passed, 0 failures, 0 errors**, plus explicit compile success. PR #34 is closed as superseded without rewriting its specialist history.

Latest lead integration packet: `coordination/returns/01/2026-09-13_ACTIVATION_021.md`.

There are currently no open production/integration PRs after PR #34 closure.

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

Canonical `submit_return_packet(...)` now:

```text
snapshot one function-owned packet candidate
-> validate packet contract
-> exact-load packet base
-> exact-load exact packet.claim_ref
-> require packet base == exact claim base
-> require packet lane == exact claim lane
-> reconstruct claim base / exactly-one claim lane
-> exact-load claim exact occupancy_ref
-> reconstruct occupancy entry base / exactly-one occupancy lane
-> require occupancy and claim logical-lane equality
-> require only local exact claim status == open
-> require only local exact occupancy status == active
-> persist the same detached packet candidate
-> return exact packet / claim / occupancy / lane identities
```

Native integration evidence:

- Lane 02 exact tested implementation/workflow head `a4a8b9ff0dcd59a62fbc41d448e2b4cc5019641c`: **147 / 147 passed**, explicit compile success.
- Lane 03 ADV-034 stacked candidate: **151 / 151 passed**, explicit compile success.
- Fresh canonical-main ADV-034 integration head `13ceeac1b5930b00458a66dd6db85913c311752c`: Actions run `34748872041`, job `103701628200`, **151 / 151 passed in 167.934s**, ADV-034-A/B/C/D all passed, explicit compile success.

Bounded claim only: immutable packet persistence is **not** packet acceptance, evidence closure, claim closure, successor-state publication, or integration.

## Why compatibility is not opened directly

`NEXT_BUILD.md` and the build plan require packet output/evidence compatibility before later integration, but the current contracts do not yet provide enough exact-instance semantics to make that check truthful.

Observed current contract facts:

- `lane.outputs[]` names output `type` values.
- `lane.evidence_requirements[]` maps an output type to required evidence states.
- `artifact.type` exists only on an artifact object.
- `evidence-record.state` exists only on an evidence-record object.
- `return-packet.artifacts_created`, `return-packet.artifacts_modified`, and `return-packet.evidence_refs` are currently arrays of unconstrained nonempty strings, not exact typed immutable references.
- artifact provenance currently records `base_state_revision` as a non-exact string.
- artifact `supersedes_ref` is not yet constrained to an exact artifact instance.

Therefore a compatibility runtime would currently need an undeclared lookup rule to turn packet strings into artifact/evidence objects. Logical id, newest object, storage order, confidence, or hidden chat may not become that authority.

The next gate is an exact-instance relationship precondition, not compatibility itself.

## Active gate — return-packet output/evidence exact-instance semantics

### Lane 02 — Deterministic Kernel Engineer

Take only this bounded precondition lane before implementing packet compatibility.

Required work:

1. inspect chronology for `artifacts_created`, `artifacts_modified`, and `evidence_refs` relative to the packet's exact work base;
2. construct deterministic counterexamples with the same logical artifact/evidence id naming different immutable instances;
3. determine which packet relationships must bind direct exact refs before output type/evidence state can be used operationally;
4. distinguish created artifact result identity from modified-artifact **observed target** identity; do not silently collapse both into one logical id;
5. inspect `artifact.provenance.base_state_revision` and `artifact.supersedes_ref` against frozen ADV-002-C / ADV-002-I before claiming modified-artifact compatibility;
6. if a small contract repair is unambiguous, implement only that repair with shared Stage 2 exact-ref validation and deterministic tests;
7. if modified-artifact semantics cannot yet represent both exact prior target and exact produced result, preserve a precise blocker/decision packet rather than guessing;
8. do not implement compatibility, claim closure, successor revision publication, integration receipt generation, epochs, or replay in this lane.

Minimum regressions for any implemented exact-ref repair:

- bare logical ids are rejected where the relationship becomes authoritative;
- wrong-kind and noncanonical refs fail through the shared semantic parser;
- same-logical-id/different-exact-instance substitution changes packet identity where appropriate;
- exact evidence selection cannot follow a newer same-id evidence record with a different state;
- exact artifact selection cannot follow a newer same-id artifact with a different type/provenance;
- no test treats storage recency or array order as authority;
- uncertainty/blocker/downstream fields survive unchanged.

### Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Wait for Lane 02's exact head or decision packet, then attack only this identity/precondition surface.

Primary attack targets:

- same logical artifact id with conflicting exact types/provenance;
- same logical evidence id with conflicting exact evidence states;
- later/newer evidence must not upgrade historical evidence quality;
- modified-artifact stale-target ambiguity must not be hidden by `supersedes_ref` or provenance strings;
- direct object-store presence must not become provenance/closure proof;
- schema evolution must not erase historical interpretation requirements;
- no output/evidence exact-ref repair may silently claim compatibility or integration.

### Lane 01 — Institution Architect / Integration Lead

Protect this sequencing boundary:

```text
exact output/evidence identity
    before
packet output/evidence compatibility
    before
claim closure / successor revision publication
    before
integration/replay
```

Do not promote a domain-specific output policy into the universal kernel. Integrate only relationships and validation rules that are universal and evidence-grounded.

## Frozen downstream obligations

- `ADV-002-C`: artifact provenance base revision needs exact-instance semantics before exact provenance/replay claims.
- `ADV-002-I`: selective stale-target compatibility for modified artifacts must derive or record the exact target instance observed from the packet base.
- `ADV-002-G/H`: integration receipts must bind exact base/result state revisions and exact packet instances before integration/replay claims.
- `ADV-011-C/D/E`: epochs must bind exact base revision and exact packet membership, with exact or uniquely resolvable lane semantics, before parallel/sequential replay claims.
- `ADV-024-A`: durable closure/evidence state must bind an exact revision once closure checking can vary historically.
- `ADV-025-A`: historical schema context must remain reconstructable before incompatible schema evolution can coexist with replayable history.
- `ADV-031-A`: authoritative post-base refs must be exact-loaded/identity-verified before operational relationship use.
- `ADV-033-A/B/C`: exact lifecycle object presence does not prove the object's historical relationships; later transitions must re-ground what they rely on unless a future explicit closure proof supersedes that mechanism.
- `ADV-034-A/B/C/D`: packet admission must remain exact-base/exact-claim grounded, resist recency laundering, and preserve detached handoff content through final publication.
- occupancy/claim global currentness, supersession, authorization, and stale-base semantics remain unresolved.
- multiple distinct exact packets for one claim still need explicit future selection/conflict semantics; there is no implicit "the packet" rule.
- `occupancy.claim_ids` and `work-claim.overlap_with_claim_ids` remain snapshot/reporting data, not exact dereference or ownership authority.
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

## Merge boundary

Inside AXM, the constitutional merge gate remains:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

No lane, founder, model, specialist, schedule position, CI result, or Git permission becomes authority by identity. When grounding is insufficient, preserve uncertainty or dissent instead of converting confidence into canon.
