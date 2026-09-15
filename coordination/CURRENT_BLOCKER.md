# CURRENT BLOCKER — Institution Fabric

Status: **Decision 024 remains the only active Stage 4 -> Stage 5 semantic gate. Lane 03 has independently cleared ADV-059-A on the exact repaired Lane 02 head, then reproduced a new bounded nested-materialization contradiction, ADV-059-B. Decision 024 remains unintegrated and Stage 5 mutation remains closed while Lane 02 repairs only ADV-059-B, followed by independent Lane 03 re-verification and a fresh Lane 01 four-root review.**

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` is historical chronology and may describe an older active gate. Recency, filename, role, founder identity, CI state, mergeability, schedule position, or Git permission remain evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical main entering this hold

Canonical `main`:

`06b1972ff640eaa7914f9a441ceaf8748ede22eb`

That commit recorded the Decision 024 repaired-head verification hold. Decision 023 remains canonical underneath it. No Stage 5 integration runtime, successor publication, claim closure, epoch/barrier, or replay runtime is canonical yet.

Decision 024 decision file:

`coordination/decisions/024_MINIMAL_PACKET_INTEGRATION_ELIGIBILITY.md`

The authorized semantic surface remains only a read-only deterministic packet-level eligibility projection for the first bounded created-output slice. A positive result means only `eligible_for_stage5_acceptance_candidate`; it is not packet acceptance, root approval, integration, claim closure, successor publication, epoch completion, replay success, or global currentness.

## Lane 02 implementation state — exact repaired ADV-059-A surface

PR #156 remains open and deliberately unmerged:

`Lane 02: implement Decision 024 packet eligibility`

Exact repaired semantic/test/workflow head:

`fd17c780d11be0d6180f58ec429890332b657cd9`

Key preserved identities:

- original ADV-059-A attacked head: `385a31d8a9cf25b4015ad18f9c0705e8af341f3c`;
- source repair: `bdb103ab59592319b76ce83146ca40f95e058141`;
- unchanged ADV-059-A oracle blob: `af11f560c1dde95f508d58872270778a9f91dec5`;
- documentation-only Lane 02 descendant: `ab66c28de96b64392ecfe373ffd29c046256279d`;
- exact tested merge candidate against then-canonical `f33a6bc...`: `b926d6d73ec4dfb84c717e1d8b67738bfb357f33`.

Lane 02 implementation-side evidence remains valid on that exact surface:

- targeted Decision 024 run `34959394063`, job `104349103004`: **16/16 passed**, explicit Decision 024 implementation + regression compilation passed;
- full deterministic run `34959394066`, job `104349103074`: protected Decision 020/022/023 checks green, **484/484 full deterministic discovery passed**, deterministic compile passed.

Those implementation-side facts did not by themselves authorize integration.

## Lane 03 independent verification — ADV-059-A cleared

PR #160 is the active adversarial evidence lane:

`Lane 03: verify ADV-059-A and expose ADV-059-B nested materialization drift`

Lane 03 created stable verification base branch:

`lane-03/verification-base-decision024-fd17c`

pointing exactly to:

`fd17c780d11be0d6180f58ec429890332b657cd9`.

Independent verification-only head:

`1b0ccd91e7f148a52170fa430c8b36099a0926fe`.

Native run/job:

- run `34963775264`;
- job `104363302192`;
- exact base `fd17c780...`;
- unchanged ADV-059-A: **passed**;
- Decision 024 baseline/continuity regressions: **passed**;
- explicit attacked-surface compile: **passed**;
- complete deterministic suite: **completed / success**.

This independently clears the bounded ADV-059-A repair on the exact repaired Decision 024 ancestry. The earlier ADV-059-A red remains valid historical evidence for exact pre-repair head `385a31d8...`.

## New active contradiction — ADV-059-B

After ADV-059-A cleared, Lane 03 demonstrated one adjacent contradiction already inside Decision 024's explicitly opened materialization attack surface.

The repaired top-level `ResolvedPacketIntegrationEligibility` is a frozen dataclass, but the nested institutional facts remain `NamedTuple`s:

- `PacketIntegrationEligibilityReason`;
- `PacketReportedFacts`.

`dataclasses.asdict(resolved)` therefore creates an apparently keyed top-level materialization while retaining tuple-shaped nested facts. Ordinary JSON transport then silently converts those nested named facts into positional arrays whose meaning depends on hidden Python field order.

ADV-059-B oracle:

`tests/test_packet_integration_eligibility_adv059_materialization.py`

Oracle blob:

`680cfdb04c3ffb24e07a78ca7984824a673e31f3`.

Test head:

`11d8c69e2d485e775f78219fd7461fa3d572e4c3`.

Native red evidence:

- run `34963915073`;
- job `104363752009`;
- tested PR merge candidate `846c30b39fe4817b192290d695f01f38a5fc282a`;
- unchanged ADV-059-A: **1/1 passed**;
- Decision 024 baseline remained green until the new contradiction;
- targeted discovery: **17 tests, 16 passed / 1 failed**;
- ADV-059-B: **failed**;
- compile/full deterministic suite: **skipped after targeted red**, so no compile/full-suite claim is made for this adversarial head.

Observed first nested reason value after `asdict(...)` + JSON transport:

`['first_slice_conditions_grounded', None, None, [], ['axmref:v1:artifact:artifact.adv059-b:-:sha256:5555555555555555555555555555555555555555555555555555555555555555']]`

That is a positional JSON list rather than a keyed fact carrying `code`, `artifact_ref`, `required_state`, `observed_states`, and `related_refs` identity.

The same structure places `PacketReportedFacts` on a positional-risk path, but the native test fails first on the reason fact. Do **not** relabel the later packet-reported-facts assertion as independently observed red until a repaired rerun reaches it.

## Current exact blocker

Decision 024 cannot be integrated while a standard materialization path can appear keyed at the top level yet silently require hidden tuple-order knowledge to reconstruct nested institutional meaning.

The current blocker is therefore the **bounded ADV-059-B nested named-fact materialization contradiction**.

This is not evidence that every serialization format must be supported and it does not open a universal transport framework. It is evidence that the current Decision 024 representation itself exposes a standard Python materialization path whose nested meaning is not self-describing after ordinary JSON transport.

## Specialist coordination

### Lane 02 — next executable lane

Repair **ADV-059-B only** on PR #156 / a clearly descendant implementation head.

The smallest acceptable repair must make `dataclasses.asdict(resolved)` followed by ordinary JSON either:

1. fail closed before nested institutional meaning can silently degrade; or
2. preserve explicit field identity for `PacketIntegrationEligibilityReason` and `PacketReportedFacts`.

Preserve unchanged ADV-059-A and Decision 024 eligibility semantics. Do not invent a broader transport contract unless separately opened by evidence.

Required evidence after repair:

- unchanged ADV-059-A green;
- unchanged ADV-059-B green;
- Decision 024 targeted baseline green;
- explicit compile green;
- complete deterministic suite green.

Do not open Stage 5 mutation, receipt/result chronology, successor publication, claim closure, epochs/barriers, replay, dependency/source closure, currentness, or model autonomy.

### Lane 03

Hold PR #160 as active adversarial evidence. Do not widen into ADV-059-C unless a concrete adjacent contradiction reproduces on the exact Lane 02 ADV-059-B repair head.

After Lane 02 publishes that exact repaired head, independently rerun unchanged ADV-059-A/B plus the Decision 024 baseline and explicit compile, preferably with broad deterministic regression evidence.

### Lane 01

Do not merge PR #156 while ADV-059-B is red.

After Lane 02 repairs ADV-059-B and Lane 03 independently verifies the exact repaired ancestry, perform a fresh review under:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

If grounded, integrate Decision 024 and only then perform the next bounded Stage 5 entry audit. If not grounded, preserve the exact dissent/blocker instead of inventing completion.

## Open-PR disposition

- PR #156: keep open as the Decision 024 implementation/repair lane.
- PR #160: keep open as active adversarial evidence.
- PR #159: coordination-only hold from before ADV-059-B; safe to close without merge as superseded, not invalidated, once this updated canonical pointer lands.

## Stage 5 boundaries still closed

Decision 024 does not solve or authorize:

- packet acceptance/rejection closure;
- root approval automation;
- integration receipt publication;
- ADV-002-G exact receipt base/result revision identity;
- ADV-002-H exact packet instance identity in receipts;
- content-addressed receipt/result publication chronology;
- claim closure;
- successor state-revision publication;
- epochs/barriers;
- replay runtime or replay success;
- dependency admissibility/satisfaction/closure beyond currently explicit facts;
- source trust, quality, relevance, completeness, or closure;
- immutable historical source-observation context;
- general hostile same-process isolation;
- mutable/global currentness;
- model autonomy.

## Root grounding of this hold

### Truth

ADV-059-A is now independently green on the exact repaired head, while ADV-059-B is independently red on the adjacent test head. Both facts are preserved on their exact ancestries instead of collapsing them into a single success/failure story.

### Agency / non-domination

No founder, lane, model, CI result, schedule position, branch owner, or Git permission can convert the implementation into canonical approval while a demonstrated continuity contradiction remains.

### Continuity

A replacement occupant can reconstruct the canonical main, repaired implementation head, independent ADV-059-A clearance, ADV-059-B oracle/blob/head, native runs, open PRs, and next responsible lane without this chat. Nested institutional facts must likewise remain reconstructable without hidden Python tuple-order knowledge.

### Wisdom before speed

Repair only the demonstrated nested fact-shape contradiction. Do not use it to widen Decision 024, invent a universal serialization layer, or start Stage 5 mutation early.

## Current v0 position

Institution Fabric remains **Stage 4 at the Stage 5 boundary**.

Decision 024 implementation exists and ADV-059-A is independently cleared, but ADV-059-B blocks integration. Stage 5 mutation/replay remains unimplemented and unclaimed.

## Best next action

**Lane 02 repairs ADV-059-B only, preserving unchanged ADV-059-A/B oracles and Decision 024 semantics.**
