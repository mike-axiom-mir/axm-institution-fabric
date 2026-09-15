# CURRENT BLOCKER — Institution Fabric

Status: **Decision 025 is canonical. Decision 026 remains non-canonical and Stage 5 mutation remains closed. Lane 02 has repaired ADV-060-A on one exact tested ancestry and Lane 03 has independently cleared unchanged ADV-060-A there, but Lane 03 has now reproduced the adjacent bounded packet-materialization contradiction ADV-060-B. The sole active semantic lane is Lane 02 repairing ADV-060-B only, followed by independent Lane 03 unchanged A+B verification and a fresh Lane 01 four-root review.**

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` is historical chronology and may describe an older gate. Recency, filename, role, founder identity, CI state, mergeability, schedule position, branch ownership, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical main entering this gate

`5e5e296cd35e92396935927bb65c1d0c0052334c` — `Hold Decision 026 on ADV-060-A`

Decision file:

`coordination/decisions/026_EXACT_STORED_INTEGRATION_CANDIDATE_BINDING.md`

Decision 026 remains a bounded read-only prerequisite. It does not authorize receipt publication, packet acceptance/rejection execution, successor construction/publication, claim/occupancy closure, multi-packet aggregation, epochs/barriers, replay, mutable currentness, model autonomy, or automatic constitutional approval.

## Preserved pre-A implementation evidence

PR #168 originally established the Decision 026 implementation surface on exact semantic/test/workflow head:

`e0a4c7b08db2567a1bd98d9d817e5b15d5b28e72`

That ancestry had native green evidence for Decision 026 **13/13**, Decision 025 **10/10**, Decision 024 **17/17**, complete deterministic discovery **508/508**, explicit compile, broad compile, and the protected identity workflow. That evidence remains true for its exact pre-ADV-060-A surface. It was not retroactively invalidated by later adversarial findings.

## ADV-060-A — repaired and independently cleared on exact ancestry

Lane 02 bounded repair on PR #168:

- exact repaired semantic/test/workflow head: `be251c40ab8a0a1bfcb3a5ae0485f2b0c9a09bfa`;
- exact tested PR merge candidate against canonical `5e5e296...`: `4dbeb20ae887c498e29caa87656cfc3d69f30148`;
- documentation-only return-packet descendant: `5f196702dd6c59152e919d6be3480693b2a5f3d5`;
- durable packet: `coordination/returns/02/2026-09-15_ACTIVATION_076.md`;
- native Decision 026 workflow run/job `34993874425` / `104465102708`: **success**;
- protected identity workflow run/job `34993874351` / `104465090048`: **success**.

Observed Lane 02 repair evidence on the exact tested candidate:

- unchanged Decision 026 baseline: **13/13 passed**;
- unchanged ADV-060-A workflow step: **passed**;
- Decision 025 regressions: **10/10 passed**;
- Decision 024 regressions including ADV-059-A/B: **17/17 passed**;
- complete deterministic discovery: **522/522 passed**;
- explicit attacked-surface `py_compile`: **passed**;
- broad `compileall`: **passed**.

The A repair is deliberately narrow: caller-owned `store.load(base_ref, ...)` remains part of the composition path, but its success no longer establishes the stronger institutional fact by itself. Decision 026 independently reproduces the exact receipt base through `FilesystemObjectStore.load(store, base_ref, "state-revision.schema.json")` before `base_materialized=True` can be emitted. Typed absence/corruption/reference failures from that canonical path remain stronger facts and propagate.

Lane 03 Activation 078 then independently attacked exact repaired head `be251c40...` on PR #174.

Exact Lane 03 adversarial/test head:

`4a5824e7ef2713ad84343c58811f6ada1f0cc75c`

Exact tested PR merge candidate:

`5f6b8079340be47cf87e2e8886b9ec25066d322f`

Native run/job:

`34995524981` / `104470659778`

The native log directly records:

1. exact repaired Decision 026 production blob pin passed (`34cac51f8778a4365aa519d873dff879425eae4d`);
2. unchanged ADV-060-A oracle blob pin passed (`f0d812bf0a170cd2848842c36f30f70a983d02ed`);
3. unchanged ADV-060-A independently passed **1/1**;
4. unchanged Decision 026 baseline independently passed **13/13 in 35.587s**.

Therefore ADV-060-A is independently cleared on exact repaired ancestry `be251c40...`. The earlier ADV-060-A red evidence remains valid for exact pre-repair ancestry `e0a4c7b...`.

## ADV-060-B — directly reproduced contradiction

Active adversarial evidence: PR #174 / Lane 03 Activation 078.

Durable packet:

`coordination/returns/03/2026-09-15_ACTIVATION_078.md`

New oracle:

`tests/test_integration_candidate_binding_adversarial_b.py`

Exact test blob on the tested Lane 03 head:

`537ad75ef2aea5ea3eafeb68bde1ce6d68c762a6`

Failing test:

`test_adv_060_b_caller_load_success_cannot_forge_absent_packet_materialization`

Native sequence after A clearance and the 13/13 Decision 026 baseline:

- ADV-060-B: **failed 1/1 in 2.993s**;
- raw assertion: `unexpectedly identical: True : caller-shadowed load success must not forge material presence for an absent exact packet`;
- Decision 025, Decision 024, complete deterministic discovery, explicit compile, and broad compile were **skipped after the red gate**.

### Exact bounded counterexample

ADV-060-B constructs one ordinary eligible packet, then derives a different well-formed exact return-packet ref that is genuinely absent. The fixture independently proves that absence through `FilesystemObjectStore.load(store, absent_packet_ref, "return-packet.schema.json")`, which raises the canonical not-found failure. It then creates an accepted v0.2 receipt naming the real exact base but the absent exact packet ref.

Only the supplied store instance's `load` method is shadowed so that a request for the absent packet returns a different genuinely stored eligible packet. Every other load delegates to the canonical base-class path. On the repaired A ancestry, Decision 026 still reaches `packet_materialized=True` for the requested exact packet ref that the canonical base-class path proved absent.

Consequential institutional fact:

```text
caller-controlled instance packet load returned
    != proof exact receipt packet materially exists
```

This is the packet-materialization sibling of ADV-060-A. It is not evidence of general hostile-process isolation failure, a need to redesign the whole store, Stage 5 mutation corruption, or a broader packet policy problem.

## Active gate — ADV-060-B repair only

### Lane 02 — next executable semantic lane

Repair ADV-060-B only on PR #168 or a directly related bounded repair ancestry.

Required repair property:

- preserve the now-cleared ADV-060-A property unchanged;
- caller-owned `load` dispatch must not by itself establish `packet_materialized=True` for the receipt's exact packet ref;
- the exact receipt packet must be independently grounded through the canonical/function-owned exact-store path, or the preflight must fail closed before emitting the stronger packet-materialization fact;
- preserve real absent/corrupt/reference failures and exact same-logical/different-exact distinction;
- preserve the Decision 024 recomputation path and Decision 025 exact receipt identity rather than duplicating their policy;
- do not widen into receipt publication, successor mutation/publication, claim/occupancy closure, aggregation, epochs/barriers, replay, currentness, model autonomy, or generic hostile same-process isolation.

Preserve both ADV-060-A and ADV-060-B oracles unchanged. On one exact repaired semantic/test/workflow head, rerun:

1. unchanged Decision 026 baseline;
2. unchanged ADV-060-A;
3. unchanged ADV-060-B;
4. Decision 025 regressions;
5. Decision 024 regressions;
6. complete deterministic discovery;
7. explicit attacked-surface compile;
8. broad deterministic compile;
9. protected identity workflow where applicable.

Pin the exact repaired semantic head, exact tested merge candidate, oracle blob identities, run/job ids, and durable return packet before handing back to Lane 03.

### Lane 03

Hold PR #174 as active adversarial evidence. Do not widen into ADV-060-C unless a concrete adjacent contradiction is actually reproduced after one exact repaired B ancestry exists.

After Lane 02 publishes one exact fully tested repaired head, independently rerun unchanged ADV-060-A, unchanged ADV-060-B, and the unchanged Decision 026 baseline against that exact ancestry. Preserve any red result exactly; do not reinterpret another ancestry as clearance.

### Lane 01

Do not merge PR #168 yet and do not open Stage 5 mutation.

After Lane 03 independently verifies the exact repaired A+B ancestry, perform a fresh integration review under:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

Only then may Decision 026 be considered for canonical integration and the next bounded Stage 5 entry audit.

## PR disposition / continuity notes

- PR #168 remains the active implementation/repair lane. Its pre-A and A-repair evidence remain valid for their exact ancestries, but the A-repaired surface is now blocked by ADV-060-B.
- PR #174 remains the active adversarial evidence lane. It independently clears A and directly demonstrates B; its red fixture/workflow should not be merged as production semantics.
- Earlier ADV-060-A evidence remains preserved for exact ancestry `e0a4c7b...`; its failure is superseded by repair on `be251c40...`, not invalidated as historical evidence.
- Lane 03 Activation 078 is the current independent evidence packet for Decision 026. Later evidence must name the exact ancestry it tests.

## Stage 5 boundaries still closed

Decision 026 and this repair gate do not solve or authorize:

- automatic constitutional/root approval;
- receipt publication;
- canonical packet acceptance/rejection execution;
- successor state-revision construction/publication;
- claim closure or occupancy closure;
- multi-packet aggregation or partial-integration semantics;
- epochs/barriers;
- replay runtime or replay success;
- dependency admissibility/satisfaction/closure outside Decision 024's empty-dependency first slice;
- source trust, quality, relevance, completeness, or closure;
- mutable/global currentness;
- model autonomy;
- general hostile same-process isolation;
- full cross-language reproduction.

## Root grounding of the hold

### Truth

Lane 02's exact ADV-060-A repair evidence and Lane 03's independent A clearance remain true. ADV-060-B is separately and directly observed red on that same repaired semantic surface. Green A evidence cannot be used to erase red B evidence, and red B evidence does not retroactively invalidate the exact earlier green runs.

### Agency / non-domination

Caller control of an object method, receipt wording, Lane 01/02/03 role identity, founder identity, CI status, branch ownership, schedule position, mergeability, or Git permission cannot become authority to declare exact packet material presence or force Decision 026 into canon.

### Continuity

The exact repaired ancestry, independent adversarial head, oracle blobs, tested merge candidate, run/job, observed assertion, prior evidence standing, and next repair ownership are explicit in repository state so another occupant can continue without private chat memory.

### Wisdom before speed

Repair only the reproduced packet-materialization contradiction and independently retest unchanged A+B before integration. Do not use the new red gate as a reason to open Stage 5 mutation or a general store-hardening project.

## Current v0 position

Institution Fabric remains **Stage 4 at the Stage 5 boundary**. Decision 026 is implemented but non-canonical and currently blocked by ADV-060-B. Stage 5 mutation remains closed.

## Best next action

**Lane 02 repairs ADV-060-B only against exact repaired Decision 026 ancestry, preserves unchanged ADV-060-A/B oracles, and returns one exact fully tested repaired ancestry to Lane 03 for independent unchanged A+B verification.**
