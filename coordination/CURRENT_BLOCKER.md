# CURRENT BLOCKER — Institution Fabric

Status: **Decision 025 is canonical. Decision 026 remains non-canonical and Stage 5 mutation remains closed. Lane 03 has now reproduced ADV-060-A against the exact Lane 02 tested Decision 026 ancestry. The sole active semantic lane is Lane 02 repairing ADV-060-A only, followed by independent Lane 03 unchanged-A verification and a fresh Lane 01 four-root review.**

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` is historical chronology and may describe an older gate. Recency, filename, role, founder identity, CI state, mergeability, schedule position, branch ownership, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical main entering this gate

`32eab95c60bef298309d8f9c52e95bd76057b36c` — `Hold Decision 026 for independent tested-head verification`

Decision file:

`coordination/decisions/026_EXACT_STORED_INTEGRATION_CANDIDATE_BINDING.md`

Decision 026 remains a bounded read-only prerequisite. It does not authorize receipt publication, packet acceptance/rejection execution, successor construction/publication, claim/occupancy closure, multi-packet aggregation, epochs/barriers, replay, mutable currentness, model autonomy, or automatic constitutional approval.

## Preserved Lane 02 implementation-side evidence

PR #168 exact semantic/test/workflow head:

`e0a4c7b08db2567a1bd98d9d817e5b15d5b28e72`

Exact tested PR merge candidate against canonical Decision 026 opening ancestry:

`089931ebf81a7e1a71cecc353255e2b65de17304`

Documentation-only Lane 02 return-packet descendant:

`294848ca594364c6be5b410a38d24a2f60fe8c51`

Durable return packet:

`coordination/returns/02/2026-09-15_ACTIVATION_074.md`

Native implementation-side evidence remains valid for that exact pre-ADV-060-A ancestry:

- Decision 026 workflow run `34981973195`, job `104424285325`: success;
- Decision 026 targeted tests: **13/13 passed**;
- Decision 025 regressions: **10/10 passed**;
- Decision 024 regressions including ADV-059-A/B: **17/17 passed**;
- complete deterministic discovery: **508/508 passed**;
- explicit Decision 026 `py_compile`: passed;
- broad `compileall`: passed;
- protected identity workflow run `34981973144`, job `104424284998`: success.

This evidence is not invalidated. It establishes only the bounded surface before ADV-060-A was added and therefore does not clear the new contradiction.

## ADV-060-A — directly reproduced contradiction

Active adversarial evidence: PR #172 / Lane 03 Activation 077.

Exact Lane 02 ancestry attacked:

`e0a4c7b08db2567a1bd98d9d817e5b15d5b28e72`

Exact Lane 03 adversarial test/workflow head:

`8e014024283983b80c3fc16bb0543cb931d0a38b`

Exact tested PR merge candidate:

`e75d1753dce7983592b567f6d67458a4bb51dedb`

Native run/job:

`34988934009` / `104448206179`

Observed sequence:

1. exact Lane 02 Decision 026 surface blob pinning passed;
2. unchanged Lane 02 Decision 026 baseline passed **13/13**;
3. ADV-060-A failed;
4. Decision 025, Decision 024, full-suite, explicit compile, and broad compile steps were skipped after the red gate.

Raw native job logs are now available and make the semantic failure directly observed rather than merely code-grounded inference. The failing test is:

`test_adv_060_a_caller_load_success_cannot_forge_absent_base_materialization`

The assertion shows the result still reported `base_materialized=True` after caller-owned instance `load` dispatch substituted a different real stored base for a receipt base ref independently proven absent through the canonical `FilesystemObjectStore.load(...)` path.

### Bounded contradiction

Decision 026 currently calls the caller-supplied exact store instance through `store.load(...)` and then treats successful return as sufficient to report materialization. ADV-060-A demonstrates one bounded path where caller-controlled instance dispatch can forge that success for an exact absent receipt base.

Consequential institutional fact:

```text
caller-controlled instance load returned
    != proof exact receipt base materially exists
```

Decision 026 must fail closed or independently ground exact base presence through the function-owned/canonical store path before emitting `base_materialized=True` for that exact ref.

This is **not** evidence of general hostile-process isolation, packet-materialization failure, Stage 5 state corruption, or a broader store redesign requirement. Stage 5 mutation is still closed and the demonstrated contradiction is base-materialization only.

## Active gate — ADV-060-A repair only

### Lane 02 — next executable semantic lane

Repair ADV-060-A only on PR #168 or a directly related bounded repair ancestry.

Required repair property:

- caller-owned `load` dispatch must not by itself establish `base_materialized=True` for the receipt's exact base ref;
- the exact base must be independently grounded through the canonical/function-owned exact-store path, or the preflight must fail closed before emitting the stronger materialization fact;
- preserve real absent/corrupt/mismatched base detection;
- do not widen into generic hostile same-process isolation, packet-load redesign, receipt publication, successor mutation, claim closure, aggregation, epochs/barriers, replay, currentness, or model autonomy.

Preserve the ADV-060-A oracle unchanged. On one exact repaired semantic/test/workflow head, rerun:

1. unchanged Decision 026 baseline;
2. unchanged ADV-060-A;
3. Decision 025 regressions;
4. Decision 024 regressions;
5. complete deterministic discovery;
6. explicit attacked-surface compile;
7. broad deterministic compile.

Pin the exact repaired semantic head, exact tested merge candidate, run/job ids, and durable return packet before handing back to Lane 03.

### Lane 03

Hold PR #172 as active adversarial evidence. Do not widen into ADV-060-B unless a concrete adjacent contradiction is actually reproduced after an exact repaired A head exists.

After Lane 02 publishes one exact repaired head with completed evidence, independently rerun the unchanged ADV-060-A oracle and Decision 026 baseline against that exact ancestry. Preserve any red result exactly; do not reinterpret a different ancestry as clearance.

### Lane 01

Do not merge PR #168 yet and do not open Stage 5 mutation.

After Lane 03 independently verifies the exact repaired ADV-060-A ancestry, perform a fresh integration review under:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

Only then may Decision 026 be considered for canonical integration and the next bounded Stage 5 entry audit.

## PR disposition / continuity notes

- PR #168 remains the active implementation/repair lane; its pre-A green evidence remains valid for that exact ancestry.
- PR #172 remains the active adversarial evidence lane; its red test is preserved and should not be merged as production semantics.
- PR #171 is a valid Lane 02 coordination packet for the earlier pre-ADV-060-A hold, but its active sequencing statement is now superseded by the reproduced contradiction. It may be closed without merge as superseded, not invalidated.
- Lane 03 Activation 076 / PR #169 remains valid historical coordination evidence for the earlier moving-head hazard; it is not Decision 026 semantic clearance.

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

The old implementation-side green evidence remains true for its exact ancestry, and ADV-060-A is now directly observed red on that same semantic surface. Neither may be erased or collapsed into the other.

### Agency / non-domination

Caller control of an object method, Lane 01/02/03 role identity, founder identity, CI status, branch ownership, schedule position, mergeability, or Git permission cannot become authority to declare exact material presence or force Decision 026 into canon.

### Continuity

The exact attacked ancestry, adversarial head, tested merge candidate, run/job, failing assertion, preserved earlier green evidence, and next repair ownership are explicit in repository state so another occupant can continue without private chat memory.

### Wisdom before speed

Repair only the reproduced base-materialization contradiction, then independently retest it before integration. Do not use the red gate as a reason to widen prematurely into Stage 5 mutation or a general store hardening project.

## Current v0 position

Institution Fabric remains **Stage 4 at the Stage 5 boundary**. Decision 026 is implemented but non-canonical and currently blocked by ADV-060-A. Stage 5 mutation remains closed.

## Best next action

**Lane 02 repairs ADV-060-A only against the exact Decision 026 surface, preserves the oracle unchanged, and returns one exact fully tested repaired ancestry to Lane 03 for independent unchanged-A verification.**
