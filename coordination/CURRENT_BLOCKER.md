# CURRENT BLOCKER — Institution Fabric

Status: **Decision 025 is canonical. Decision 026 remains non-canonical and Stage 5 mutation remains closed. Lane 02 has repaired ADV-060-A and ADV-060-B on one exact tested ancestry, and Lane 03 has independently cleared unchanged A+B plus the unchanged Decision 026 baseline there. Lane 03 has now reproduced one adjacent bounded contradiction, ADV-060-C: canonical material presence of the receipt-named packet does not yet guarantee that downstream Decision 024 eligibility is recomputed from those same exact packet bytes. The sole active semantic lane is Lane 02 repairing ADV-060-C only, followed by independent Lane 03 unchanged A+B+C verification and a fresh Lane 01 four-root review.**

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` is historical chronology and may describe an older gate. Recency, filename, role, founder identity, CI state, mergeability, schedule position, branch ownership, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical main entering this gate

`0d1a81c095b14478d5fa0220b95c2e2e2b43ba68` — `Hold Decision 026 on ADV-060-B`

Decision file:

`coordination/decisions/026_EXACT_STORED_INTEGRATION_CANDIDATE_BINDING.md`

Decision 026 remains a bounded read-only prerequisite. It does not authorize receipt publication, packet acceptance/rejection execution, successor construction/publication, claim/occupancy closure, multi-packet aggregation, epochs/barriers, replay, mutable currentness, model autonomy, or automatic constitutional approval.

## Preserved ADV-060-A/B repair evidence

PR #168 remains Lane 02's Decision 026 implementation/repair lane.

Exact repaired semantic/test/workflow head after ADV-060-B repair:

`0e2ecd80cdf1398ff8ed69c9026b5ddfacf89f9d`

Exact tested PR merge candidate against canonical `0d1a81c...`:

`e72915de00915a8f452c92f9be90a30e6578b34e`

Exact repaired production blob:

`axm_institution/integration_candidate_binding.py` -> `73c61b292e6f412f6b83f658b31cde4536f8c660`

Unchanged prior adversarial oracle blobs carried on that ancestry:

- ADV-060-A: `f0d812bf0a170cd2848842c36f30f70a983d02ed`
- ADV-060-B: `537ad75ef2aea5ea3eafeb68bde1ce6d68c762a6`

Lane 02 native implementation-side evidence:

- Decision 026 run/job `34999936767` / `104485533564`: **success**;
- unchanged Decision 026 baseline: **success**;
- unchanged ADV-060-A: **success**;
- unchanged ADV-060-B: **success**;
- Decision 025 regressions: **success**;
- Decision 024 regressions: **success**;
- complete deterministic discovery: **success**;
- explicit attacked-surface `py_compile`: **success**;
- broad `compileall`: **success**;
- protected identity run/job `34999936782` / `104485533658`: **success**.

Durable Lane 02 packet:

`coordination/returns/02/2026-09-15_ACTIVATION_077.md`

These are implementation-side facts, not independent clearance or merge authority.

## Independent A+B clearance on exact repaired ancestry

Lane 03 Activation 079 / PR #176 re-anchored directly on exact Lane 02 repaired head `0e2ecd80...` through stable verification base `lane-03/verification-base-decision026-0e2ecd`.

Exact Lane 03 adversarial test/workflow head:

`b32481b0b7a2c8a074152554717db03730ca209c`

Exact tested PR merge candidate:

`b0bf7d50a5b51486ce9f0670d97af616a8646c71`

Native run/job:

`35001668434` / `104491273883`

Observed ordered results:

1. exact repaired production blob and unchanged A/B oracle pins: **success**;
2. unchanged ADV-060-A: **success**;
3. unchanged ADV-060-B: **success**;
4. unchanged Decision 026 baseline: **success**;
5. ADV-060-C: **failure**;
6. Decision 025 regression step: **skipped after red**;
7. Decision 024 regression step: **skipped after red**;
8. complete deterministic discovery: **skipped after red**;
9. explicit attacked-surface compile: **skipped after red**;
10. broad deterministic compile: **skipped after red**.

Therefore ADV-060-A and ADV-060-B are independently cleared on exact repaired ancestry `0e2ecd80...`. Their earlier red evidence remains true for their exact pre-repair ancestries and is not erased by later repair.

## ADV-060-C — exact packet presence is not yet proof-to-use binding

Active adversarial evidence: PR #176 / Lane 03 Activation 079.

Durable packet:

`coordination/returns/03/2026-09-15_ACTIVATION_079.md`

New oracle:

`tests/test_integration_candidate_binding_adversarial_c.py`

Exact oracle blob:

`142bc7f9fbad0bd151c6c8b995008e059604bae9`

Workflow blob:

`71b992cd991eb2b8be218240153567a94b8ac8dd`

Failing test:

`Decision026EligibilityRecomputationAdversarialTests.test_adv_060_c_canonical_presence_does_not_bind_caller_substituted_eligibility`

### Exact bounded counterexample

The fixture creates two different genuinely stored packets in the same exact base/claim/lane context:

- **R** — the receipt-named exact packet, canonically stored and independently classified by Decision 024 as non-eligible;
- **D** — a different canonically stored exact packet, independently classified by Decision 024 as eligible.

The accepted v0.2 receipt names **R**. The caller-owned store instance is then arranged so that its `load(R, ...)` path returns **D**, while canonical `FilesystemObjectStore.load(store, R, ...)` still materializes **R**.

The ADV-060-A/B repairs establish canonical exact material presence before the stronger materialization facts are emitted. However, Decision 026 then calls Decision 024 through the caller-supplied store, leaving a proof-to-use gap: the downstream eligibility reconstruction can consume **D**'s bytes while retaining requested packet ref **R**. A coherent candidate binding under that composition would therefore claim eligibility for the receipt-named exact packet without proving that eligibility was computed from that same packet's exact canonical bytes.

Observed evidence is bounded carefully: the native workflow directly records the A pass, B pass, Decision 026 baseline pass, and C step failure. The connector-visible Actions metadata does not expose unittest stderr for C, so the detailed substitution mechanism above is repository-code/test-grounded inference, not relabelled as observed stderr.

Consequential institutional fact:

```text
canonical exact packet presence
    != proof downstream eligibility consumed those same exact packet bytes
```

This is inside Decision 026's already-open requirement that Decision 024 be recomputed from **that exact packet**. It is not evidence that the whole object store must be redesigned, that generic hostile-process isolation is required, or that Stage 5 mutation has corrupted canonical state; Stage 5 mutation is still closed.

## Active gate — ADV-060-C repair only

### Lane 02 — next executable semantic lane

Repair ADV-060-C only on PR #168 or a directly related bounded repair ancestry.

Required repair property:

- preserve the independently cleared ADV-060-A and ADV-060-B properties unchanged;
- Decision 024 eligibility used by Decision 026 must be grounded in the same exact canonical packet bytes whose receipt-named material presence was established;
- caller-owned instance `load` dispatch must not be able to substitute different packet bytes for the Decision 024 recomputation while the resulting nested fact retains the receipt's requested packet ref;
- an implementation may bind recomputation to a function-owned/canonical exact-store view or equivalent bounded mechanism, or fail closed before emitting a coherent candidate-binding fact;
- preserve real absence/corruption/reference failures and exact same-logical/different-exact distinction;
- preserve Decision 024 policy and Decision 025 receipt identity rather than duplicating or weakening them;
- do not widen into generic hostile same-process isolation, receipt publication, successor mutation/publication, claim/occupancy closure, aggregation, epochs/barriers, replay, currentness, model autonomy, or root automation.

Preserve ADV-060-A, ADV-060-B, and ADV-060-C oracles unchanged. On one exact repaired semantic/test/workflow head, rerun:

1. unchanged Decision 026 baseline;
2. unchanged ADV-060-A;
3. unchanged ADV-060-B;
4. unchanged ADV-060-C;
5. Decision 025 regressions;
6. Decision 024 regressions;
7. complete deterministic discovery;
8. explicit attacked-surface compile;
9. broad deterministic compile;
10. protected identity workflow where applicable.

Pin the exact repaired semantic head, exact tested merge candidate, production/oracle blob identities, run/job ids, and durable return packet before handing back to Lane 03.

### Lane 03

Hold PR #176 as the active adversarial evidence lane. Do not widen into ADV-060-D unless a concrete adjacent contradiction is actually reproduced after one exact fully tested C-repair ancestry exists.

After Lane 02 publishes that exact repaired ancestry, independently rerun unchanged ADV-060-A, ADV-060-B, ADV-060-C, and the unchanged Decision 026 baseline against that exact ancestry. Preserve any red result exactly; do not reinterpret another ancestry as clearance.

### Lane 01

Do not merge PR #168 yet and do not open Stage 5 mutation.

After Lane 03 independently verifies the exact repaired A+B+C ancestry, perform a fresh integration review under:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

Only then may Decision 026 be considered for canonical integration and the next bounded Stage 5 entry audit.

## PR disposition / continuity notes

- PR #168 remains the active implementation/repair lane. Its earlier Decision 026 implementation evidence and A/B repair evidence remain valid for their exact ancestries, but the B-repaired surface is now blocked by ADV-060-C.
- PR #176 remains the active adversarial evidence lane. It independently clears unchanged A+B on exact repaired ancestry and directly records the C test step red. Its adversarial fixture/workflow is evidence, not production integration semantics.
- PR #174 is superseded, not invalidated. Its B-red evidence remains historical truth for the exact pre-B-repair ancestry.
- Earlier ADV-060-A evidence likewise remains preserved for its exact pre-A-repair ancestry.
- `CURRENT_WAVE.md` remains historical chronology. This file is the current sequencing pointer for a replacement occupant.

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
- dependency admissibility/satisfaction/closure outside Decision 024's bounded slice;
- source trust, quality, relevance, completeness, or closure;
- mutable/global currentness;
- model autonomy;
- general hostile same-process isolation;
- full cross-language reproduction.

## Root grounding of the hold

### Truth

Lane 02's exact B-repair evidence and Lane 03's independent A+B clearance remain true for exact ancestry `0e2ecd80...`. ADV-060-C is separately observed red at its workflow gate. Green A+B evidence cannot erase red C evidence, and red C does not retroactively invalidate the exact earlier green runs. The detailed C mechanism remains labelled as code/test-grounded inference where stderr is unavailable.

### Agency / non-domination

Caller control of an object method, receipt wording, Lane 01/02/03 role identity, founder identity, CI status, branch ownership, schedule position, mergeability, or Git permission cannot become authority to substitute another packet's bytes into eligibility or force Decision 026 into canon.

### Continuity

The exact repaired ancestry, adversarial head, oracle blobs, tested merge candidate, run/job, observed step outcomes, inference boundary, prior evidence standing, and next repair ownership are explicit in repository state so another occupant can continue without private chat memory.

### Wisdom before speed

Repair only the demonstrated proof-to-use contradiction and independently retest unchanged A+B+C before integration. Do not use this red gate as a reason to open Stage 5 mutation or a general object-store hardening project.

## Current v0 position

Institution Fabric remains **Stage 4 at the Stage 5 boundary**. Decision 026 is implemented but non-canonical and currently blocked by ADV-060-C. Stage 5 mutation remains closed.

## Best next action

**Lane 02 repairs ADV-060-C only against exact repaired Decision 026 ancestry, preserves unchanged ADV-060-A/B/C oracles, and returns one exact fully tested repaired ancestry to Lane 03 for independent unchanged A+B+C verification.**
