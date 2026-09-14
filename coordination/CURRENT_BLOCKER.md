# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Current canonical base inspected by Lane 01: **`391cc0dcc77f2a16b04f93ea51d4082d114260cc`**
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current bounded gate: **Decision 022 — Exact Source Runtime Capability Facts**
Current disposition: **HOLD on ADV-057-A. Lane 02's bounded Decision 022 implementation has a directly observed green baseline, but Lane 03 independently demonstrated one narrow failure-semantics counterexample for an existing regular bundled schema containing invalid UTF-8. Decision 022 must not be integrated until Lane 02 repairs only that context-error boundary and Lane 03 reruns the unchanged adversarial oracle successfully.**

This file is the current sequencing pointer. Earlier detailed overlays, Decisions 020–022, specialist return packets, commits, and failed/successful CI evidence remain historical evidence and are **not invalidated or rewritten** by this shorter current overlay. `coordination/CURRENT_WAVE.md` remains historical chronology and must not override newer repository state.

## Preserved source-declaration boundary

Decision 020 remains canonical with exactly four typed source declaration classes for new artifact/evidence versions:

- `opaque_label`;
- `exact_axm_object`;
- `content_address`;
- `locator`.

Historical `source_refs[]` strings retain their authored opaque meaning. Declaration occurrence identity remains:

`exact containing object identity + declaration key`.

A declaration establishes target identity syntax only at its class's bounded strength. It does not establish target existence, retrieval, integrity, causal provenance, trust, relevance, completeness, closure, acceptance, integration, epoch completion, or replay correctness.

Decision 021 remains a research hold on actual exact-target observation. Runtime capability, target availability/corruption, and mutable observation-context/re-execution standing remain separate facts.

## Lane 02 PR #101 — baseline green, not integrated

PR #101 (`Lane 02: exact source runtime capability facts`) implements Decision 022 only on canonical base `391cc0dcc77f2a16b04f93ea51d4082d114260cc`.

Exact semantic/test head:

`4e4f2f3d93eb77c8745074654a9fb95dceb67814`

Final branch head after documentation-only return packet:

`ba07d3feba8269c00c2444e0c44550f09c01e461`

Directly inspected native PR merge candidate:

`a600e385fe5ad170df88f8ed2d35214aeebf12ce`

GitHub Actions run/job:

`34827117857` / `103921717936`

Observed results:

- Python 3.12.14 / jsonschema 4.26.0;
- preserved ADV-054/ADV-055 oracle: **6/6 passed**;
- complete deterministic discovery: **431/431 passed, 0 failures, 0 errors** in 481.470s;
- all 14 new Decision 022 regressions passed within that discovery;
- explicit enumerated `py_compile`: **passed**;
- complete job: **success**.

The bounded implementation preserves exact containing-object identity plus exact declaration-key occurrence, exact target ref/kind, and only `runtime_capability = supported | unsupported_kind`. It accepts no source store, resolver, custom schema directory, ambient observation context, or target path parameter and does not load the declared source target.

This baseline remains valid evidence for that exact candidate. It is **not** sufficient for integration after the newer ADV-057-A counterexample.

## Lane 03 PR #102 — ADV-057-A red blocker

PR #102 (`Lane 03: adversarially verify Decision 022 capability context`) is stacked on PR #101 and changes only the adversarial test/workflow/return-packet surface for this attack.

Exact adversarial test/workflow head:

`caf8f8e1b8befc5cffad25aef981d8c801a05b6d`

Final branch head after return packet:

`f3f30fcc6c9f9be37adff2212bbe39a1685aad0d`

Exact tested merge candidate:

`5e8d7df3193113b399a3ce60d4c133459d1109e9`

GitHub Actions run/job:

`34828726747` / `103926751207`

Directly observed results:

- preserved ADV-054/ADV-055: **6/6 passed**;
- ADV-057-A through F: **6 ran; 5 passed; ADV-057-A errored**;
- ADV-057-B/C/D/E/F passed;
- full deterministic discovery: **skipped after focused failure**;
- explicit compile: **skipped after focused failure**.

### Exact blocker

ADV-057-A supplies an **existing regular bundled** `artifact.schema.json` whose bytes are invalid UTF-8. Decision 022 already requires existing unreadable/invalid bundled schema state to fail closed as a dedicated runtime capability-context failure.

The implementation instead leaks raw:

`UnicodeDecodeError`

through:

`project_exact_source_runtime_capability(...)`
→ `_bundled_runtime_capability(...)`
→ `_identity.load_schema(...)`
→ `Path.read_text(encoding="utf-8")`.

This is a narrow runtime-context failure-normalization defect. It is **not** evidence that the declared source target is absent, corrupt, untrusted, irrelevant, incomplete, rejected, or non-canonical.

The earlier draft adversarial idea that treated an entirely missing schema root as context failure was corrected before blocker disposition. Under Decision 022, absence of the inferred bundled schema file remains `unsupported_kind`; the demonstrated blocker concerns an **existing but unreadable** schema.

## Integration disposition

Do **not** merge PR #101 while ADV-057-A is unresolved.

Do **not** merge PR #102's red stacked adversarial branch as canonical production history.

Do **not** implement the repair in Lane 01 while Lane 02 owns the bounded production lane.

Green CI, Git mergeability, lane role, founder identity, schedule order, or technical permission do not override the demonstrated counterexample. The four AXM roots remain the internal constitutional merge gate.

## Active lane boundaries

### Lane 01 — sequencing / integration

Hold Decision 022. Preserve both the 431/431 baseline and ADV-057-A red evidence. Review integration only after an exact Lane 02 repaired candidate and unchanged independent Lane 03 green rerun exist. Do not open actual target observation, source resolution, integrity, trust, closure, Stage 5, epochs, or replay in parallel.

### Lane 02 — smallest repair owner

Repair **only** Decision 022's existing-bundled-schema failure boundary so an existing unreadable/undecodable bundled schema fails through `SourceRuntimeCapabilityContextError` rather than leaking a lower-level decode/read exception.

Preserve all current semantics:

- missing inferred bundled schema file → `unsupported_kind`;
- existing readable valid bundled schema → `supported`;
- existing non-regular/unreadable/unparsable/invalid bundled schema → fail closed as runtime capability-context failure;
- no target source object I/O;
- no custom/ambient schema context;
- no resolver, availability, integrity, trust, closure, acceptance, Stage 5, epoch, or replay semantics.

Then run unchanged ADV-054/055, unchanged ADV-057-A through F, the full deterministic suite, and explicit compile. Leave exact heads/run evidence in a durable return packet.

### Lane 03 — independent recheck after repair

Rerun ADV-057-A through F **unchanged** against Lane 02's exact repaired head. If green, run full deterministic discovery and explicit compile. Preserve any new counterexample rather than weakening the oracle after seeing the repair.

## Still explicitly unresolved

- immutable/snapshot-like source observation context identity or an explicit non-reexecution limitation;
- exact target availability/existence observation;
- source loading/retrieval semantics and retained bytes;
- digest/integrity verification and retained integrity evidence;
- locator/network/filesystem/package resolvers;
- explicit locator/content/exact association;
- historical-to-typed migration objects;
- provenance-relation vocabulary;
- source trust/quality/relevance/completeness/closure;
- dependency admissibility / satisfaction / closure;
- actual production chronology / scheduler order;
- evidence method/source quality, precedence, invalidation dominance, and closure;
- multiple `required_states` semantics;
- logical lineage and `supersedes_ref` validity;
- global occupancy/claim currentness, supersession, and authorization;
- multiple-packet conflict/selection semantics;
- packet acceptance/rejection and durable closure;
- claim closure;
- successor state-revision publication;
- Stage 5 integration receipts/runtime;
- epochs/barriers and replay;
- cross-language graph/reachability/frontier/source reproduction;
- exact self/mutual-cycle authorability through ordinary content-addressed publication;
- stronger filesystem durability/concurrency evidence;
- hostile same-process code isolation beyond the trusted deterministic runtime boundary.

## Four-root gate

- **Truth:** the earlier 431/431 baseline remains true for its exact candidate, and the later ADV-057-A failure remains true for its exact candidate; neither erases the other.
- **Agency / non-domination:** no actor, lane, founder, CI result, branch, schedule position, runtime host, or Git permission gains authority over the demonstrated evidence.
- **Continuity:** exact heads, merge candidates, runs, failure semantics, lane ownership, and downstream hold are now recoverable from repository state rather than private chat.
- **Wisdom before speed:** repair the demonstrated context-error boundary and independently recheck it before integrating Decision 022 or opening actual source observation.
