# CURRENT WAVE — Institution Fabric

Status: active initial build wave. Stage 1 contracts, Stage 2 deterministic identity, exact revision membership, Stage 3 immutable object storage, exact lifecycle bases, deterministic exactly-one member resolution, Decisions 001–008, and the bounded Stage 4 occupancy / work-claim / return-packet admission primitives are canonical. The return-packet created-artifact/evidence exact-instance precondition is also canonical through PR #37, with ADV-035/036/037 repairs and ADV-038 materialization regressions preserved. The next opened gate is **exact evidence-to-created-artifact subject binding before packet output/evidence compatibility**. Claim closure, successor-state publication, integration receipts/runtime, epochs/barriers, and replay remain closed.

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable immutable evidence exists.

The immediate requirement is narrower: an exact evidence record may count toward an exact created output only when the evidence explicitly names that exact artifact as its subject. Exact evidence identity alone does not establish evidence relevance.

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
- ADV-034-A/B/C/D return-packet continuity regressions on canonical-main integration head `13ceeac1b5930b00458a66dd6db85913c311752c`: native run `34748872041`, job `103701628200`, 151/151 passed, explicit compile success.
- Exact return-packet created-artifact/evidence identity precondition through PR #37 / merge `bf20e7bd1fa641dab7c5c51bee608ed541171a80`.
- ADV-038 materialization regressions and Lane 03 Activation 026 preserved through PR #42 / merge `63b9b80c5d25a85cd477a721fb5286fcbee5ded1`.
- Decision 008 evidence subject chronology through PR #43 / merge `3c04a38033cd2c10fc5d6daf88abc0ae9b9f32c5`.

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

## Canonical return-packet output/evidence identity precondition

`resolve_return_packet_output_identity(...)` is now canonical for the demonstrated created-artifact/evidence surface. It:

- exact-loads one exact immutable return packet;
- treats `artifacts_created[]` as direct canonical exact immutable `artifact` refs;
- treats packet `evidence_refs[]` as direct canonical exact immutable `evidence-record` refs;
- reuses shared Stage 2 immutable-reference parsing;
- exact-loads and verifies required kind/logical id;
- returns canonical-byte-backed immutable operational views whose demonstrated direct-use and bounded materialization paths remain exact;
- fails closed on any non-empty `artifacts_modified[]` because the current contract cannot truthfully express both the exact observed prior artifact and exact produced result.

### Repair / adversarial evidence retained

- ADV-035: ordinary post-resolution alias mutation was demonstrated and repaired.
- ADV-036: builtin base-class mutator bypass was demonstrated and repaired.
- ADV-037: tuple-backed operational views could serialize through stdlib JSON into arrays of keys; repaired by the canonical-byte-backed representation, where unsupported ordinary transport may reject rather than silently change meaning.
- ADV-038-A/B/C: mapping/list/canonical materialization re-attacked the repaired representation; no contradiction reproduced.

Lane 02 exact repaired implementation/workflow head `627a878dbcdade96c0602efddb2f5e06974a3442` directly recorded **171/171 passed** plus explicit compile success before its documentation-only final commit.

Lane 03 exact tested ADV-038 head `a3a119f6c5b62bd2b982ff54ab05cd8984b39ccf` had native run `34757374230` with full test discovery success and explicit compile success. Its numerical total `174` remains a source-accounting inference from the prior observed 171 plus exactly three added unittest methods, not relabelled as directly observed stdout.

Lane 01 then reapplied those exact ADV-038 fixtures on a fresh current-main branch after PR #37 merged. Native run `34758666774`, job `103727428236`, exact head `5b98fc8043965a1053784352901ff33f566502cd` completed with:

- full deterministic unittest discovery: **success**;
- explicit compile including ADV-038: **success**;
- complete job: **success**.

PR #42 integrated those regressions and the Lane 03 return packet without changing production runtime.

Historical failing adversarial PRs #38, #39, and #40 are closed without merging; their failure evidence remains preserved. Stacked successful PR #41 is also closed as superseded by canonical PR #42 rather than rewritten or deleted.

## Active gate — exact evidence subject binding before compatibility

Decision 008 records the next missing institutional fact:

```text
exact evidence identity
    != evidence that this exact record supports this exact output
```

Current contract facts:

- `lane.outputs[]` declares output `type` values;
- `lane.evidence_requirements[]` declares required evidence states for an output type;
- an `artifact` has `type` and `evidence_refs[]`;
- an `evidence-record` has `subject_ref` and `state`;
- the current evidence schema permits `subject_ref` to be a general string;
- the packet identity resolver can now bind exact created-artifact and exact evidence-record instances.

A type/state-only compatibility check could therefore launder unrelated passing evidence into support for an output.

Decision 008 opens only this acyclic Stage 4 subject chronology:

```text
exact created artifact A
    -> exact evidence E created/selected later
    -> E.subject_ref must be the canonical exact artifact ref A
    -> exact packet P names A and E
```

For this bounded path, `artifact.evidence_refs` does not become authoritative for post-artifact evidence compatibility. Requiring both A to exact-ref E and E to exact-ref A would create a content-addressed reciprocal dependency; the kernel must not invent recency/currentness to escape that cycle.

Evidence whose subject is a path, logical id, content reference, or other non-exact string may remain a valid evidence object for other purposes, but it cannot satisfy exact created-artifact output compatibility without a later grounded relation.

## Lane 02 — smallest next implementation

Implement only a **read-only exact evidence-subject resolver** around the already-grounded packet output/evidence identity result.

Required behavior:

1. use the shared Stage 2 immutable-reference parser for candidate `evidence.subject_ref` values;
2. require kind `artifact` when an evidence record is being considered against a created artifact;
3. bind evidence only to the exact created-artifact ref it names;
4. expose unmatched/non-artifact subject evidence explicitly or fail closed — never assign by output type, array order, newest version, storage order, or logical id;
5. preserve `artifacts_modified` fail-closed behavior;
6. remain read-only; do not close claims, publish successor revisions, integrate packets, or mutate evidence;
7. keep ADV-035/036/037/038 green.

Required regressions:

- exact subject A binds to exact created artifact A;
- same logical artifact id / different exact artifact ref does not bind;
- bare logical id, path, or content string does not count as exact artifact subject evidence;
- wrong-kind exact subject ref fails closed for artifact compatibility;
- exact packet evidence about unrelated artifact B cannot satisfy artifact A even when type/state appear compatible;
- `artifact.evidence_refs` cannot override a contradictory exact evidence subject;
- no recency/current/array-order/actor authority enters selection.

Stop after subject binding. Do **not** decide the semantics of multiple `required_states`, full compatibility, provenance/evidence closure, claim closure, successor publication, integration, epochs, or replay in the same lane.

## Lane 03 — next adversarial pass

Attack the exact Lane 02 subject-binding head only:

- same-logical-id/different-exact artifact substitution;
- unrelated passing-evidence laundering;
- wrong-kind exact subject refs;
- non-exact subject strings accidentally accepted through fallback logic;
- `artifact.evidence_refs` attempting to override contradictory subject identity;
- multiple evidence records with conflicting states for the same exact subject;
- nested/materialized views still preserving ADV-035/036/037/038 invariants.

Do not expand into full lane compatibility or later lifecycle/integration stages.

## Lane 01 — sequencing boundary

Protect this order:

```text
exact packet/artifact/evidence selection
    -> proof-to-use/materialization continuity
    -> exact evidence-to-output subject binding
    before
packet output/evidence compatibility semantics
    before
claim closure / successor revision publication
    before
integration / epochs / replay
```

Do not promote domain-specific output policy into the universal kernel.

## Frozen downstream obligations

- Semantics of multiple lane `required_states` remain unresolved; do not assume conjunctive/alternative/ordered meaning yet.
- Evidence method/source quality beyond current schema validation remains unresolved.
- Artifact `evidence_refs` chronology/exact semantics remains unresolved and is not compatibility authority in the current slice.
- `ADV-002-C`: artifact provenance base revision needs exact-instance semantics before exact provenance/replay claims.
- `ADV-002-I`: modified-artifact semantics must represent/derive both exact observed prior target and exact produced result; stale-target compatibility remains unresolved.
- `ADV-002-G/H`: integration receipts must bind exact base/result revisions and exact packet instances before integration/replay claims.
- `ADV-011-C/D/E`: epochs must bind exact base revision and exact packet membership before parallel/sequential replay claims.
- `ADV-024-A`: durable closure/evidence state must bind an exact revision once closure checking can vary historically.
- `ADV-025-A`: historical schema context must remain reconstructable before incompatible schema evolution coexists with replayable history.
- `ADV-031-A`: authoritative post-base refs must be exact-loaded/identity-verified before operational relationship use.
- `ADV-033-A/B/C`: exact lifecycle object presence does not prove the object's historical relationships; later transitions re-ground relationships they rely on unless a future explicit closure proof supersedes that mechanism.
- `ADV-034-A/B/C/D`: packet admission remains exact-base/exact-claim grounded and detached handoff content remains stable through publication.
- ADV-035/036/037/038 exact operational/materialization regressions must remain green as later consumers are added.
- occupancy/claim global currentness, supersession, authorization, and stale-base semantics remain unresolved.
- multiple exact packets for one claim need explicit future selection/conflict semantics.
- packet output/evidence compatibility remains unimplemented beyond the exact-identity and subject-binding preconditions.
- claim closure/status-transition publication remains unimplemented.
- successor state revision publication remains unimplemented.
- integration runtime, epochs/barriers, and replay remain unimplemented.
- full cross-language reproduction remains untested.
- filesystem power-loss durability, concurrent-writer stress, and non-Linux atomic-publication behavior remain not fully proven.

These are obligations, not evidence that the corresponding runtimes exist.

## Shared return-packet minimum

Each specialist leaves repository evidence containing: base inspected; bounded claim; files/behavior changed; exact evidence/tests; uncertainty/blockers; dependency/downstream effects; next action; and explicit evidence status (`proposed`, `implemented`, `compiled`, `automated_tested`, `runtime_tested`, `measured`, `inferred`, `blocked`, `not_tested`, etc.).
