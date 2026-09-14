# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Current canonical main after Lane 01 integration: **`ae2a4171dac0c6bb56b86ac11fc4b987924b4a94`**
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current canonical source gate: **Decision 022 — Exact Source Runtime Capability Facts**
Current bounded research gate: **Decision 021 — Source Observation Boundary / observation-context identity**
Current disposition: **Decision 022 is canonical on its bounded no-target-I/O runtime-capability surface. Actual exact-source target observation remains held. Lane 01 must first finish the Decision 021 observation-context / re-execution research boundary; Lane 02 must not implement a target observer yet.**

This file is the current sequencing pointer. Earlier overlays, failed and successful specialist runs, Decisions 020–022, and return packets remain historical evidence and are not invalidated or rewritten by this update. `coordination/CURRENT_WAVE.md` remains historical chronology and must not override newer repository state.

## Canonical Decision 022 boundary

Decision 022 now provides a deterministic fact for one exact Decision 020 `exact_axm_object` declaration occurrence:

- exact containing-object identity;
- exact declaration key;
- exact authored target `object_ref`;
- parsed target kind;
- `runtime_capability = supported | unsupported_kind` for the fixed bundled kernel schema context only.

The projection performs no target source-object lookup. `supported` establishes only that this bundled runtime has a valid interpretation contract for the target kind. It does not establish target existence, availability, retrieval, integrity, provenance causality, trust, relevance, completeness, closure, acceptance, integration, epoch completion, or replay correctness.

Missing inferred bundled schema remains `unsupported_kind`. An inferred bundled schema that exists but is non-regular, unreadable, undecodable, unparsable, or invalid fails closed through `SourceRuntimeCapabilityContextError`; it is not relabelled as unsupported or source corruption.

Custom/mutable schema directories remain outside Decision 022.

## Preserved evidence chain

### Historical green baseline

Before the adversarial counterexample, Lane 02 had a directly observed green baseline for the bounded implementation: **431/431 deterministic tests passed** plus explicit compile. That result remains valid for its exact candidate but did not override later red evidence.

### Historical ADV-057-A red evidence

Lane 03 then demonstrated that an existing regular bundled schema containing invalid UTF-8 leaked raw `UnicodeDecodeError` instead of the dedicated Decision 022 capability-context failure. ADV-057-B through F passed while ADV-057-A errored; later full-suite and compile stages were correctly skipped. This red result remains historical truth for its exact pre-repair candidate.

### Lane 02 bounded repair

Lane 02 repaired only the demonstrated failure-normalization boundary. Exact repaired test-bearing head:

`b4aeafc236d4abb426bbd0bd78ca4780675fabab`

Fresh-main PR merge candidate tested:

`a78ff60a4dd2721e24ab0eedd6b3f9e8f7ff896b`

Run/job:

`34832341654` / `103938318383`

Directly observed on Ubuntu 24.04.5 / Python 3.12.14 / jsonschema 4.26.0:

- preserved Decision 020 ADV-054/055: **6/6 passed**;
- unchanged ADV-057-A through F: **6/6 passed**;
- full deterministic discovery: **437/437 passed, 0 failures, 0 errors** in 383.638s;
- explicit enumerated `py_compile`: **passed**;
- complete native job: **success**.

The repair only extends the local Decision 022 bundled-capability wrapper so Unicode decode failures normalize through `SourceRuntimeCapabilityContextError`. It does not change shared schema-loader semantics or open source target I/O.

### Lane 03 independent unchanged-oracle recheck

Lane 03 branched from the exact repaired head and preserved the ADV-057 oracle byte-for-byte (blob `d5a855e9883d1ed42df39379f3ab8b34126477be`). Exact independent test head:

`9a881a433b1973a893b6d8501cd39b93c79de4b9`

Exact PR merge candidate tested:

`4c709c088eaa1babcbcaad17ed4daf32120f22b4`

Run/job:

`34833589216` / `103942279133`

Directly observed on the same demonstrated runtime family:

- Decision 020 ADV-054/055: **6/6 passed**;
- unchanged ADV-057-A through F: **6/6 passed**;
- full deterministic discovery: **437/437 passed, 0 failures, 0 errors** in 298.555s;
- explicit enumerated `py_compile`: **passed**;
- complete native job: **success**.

No production Python, schema, fixture, or ADV-057 oracle was changed by Lane 03 to obtain this result. Its branch-only workflow allowlist entry is not itself institutional semantics.

### Canonical integration

Lane 01 squash-merged PR #101 as:

`ae2a4171dac0c6bb56b86ac11fc4b987924b4a94`

The four-root integration disposition is therefore:

- **Truth:** preserve the exact sequence green baseline → red counterexample → bounded repair → independent unchanged-oracle green recheck. No later green run erases the red history.
- **Agency / non-domination:** Lane 02, Lane 03, Lane 01, founder identity, CI success, branch order, and Git permission are evidence/execution facts, not constitutional authority.
- **Continuity:** exact declaration occurrence identity, bounded failure semantics, exact heads, merge candidates, runs, and specialist handoffs are durable outside private chat.
- **Wisdom before speed:** integrate only the no-target-I/O capability fact and keep actual source observation held until its context/re-execution meaning is grounded.

## Decision 021 research finding after Decision 022

Inspection of the current `FilesystemObjectStore` establishes a useful boundary:

1. `load_bytes(reference)` and `load(reference)` use exact `axmref:v1` identity and, on success, verify stored raw bytes against canonical schema validation and the requested immutable reference.
2. The filesystem **store root is mutable runtime state**. A path label does not become immutable context identity merely because exact object names beneath it are content-addressed.
3. `ObjectNotFoundError` therefore means only that the exact object was not present in the inspected store context at that observation. It cannot truthfully mean global nonexistence.
4. `ObjectCorruptionError` means the bytes found at that exact path failed the exact identity contract in that inspected context. It is not a trust or acceptance verdict.
5. A successful observation can later be replayed from retained verified bytes if those bytes are made part of a future explicit observation record, but the current kernel has **no durable immutable identity for the live store context itself**.
6. A negative live-store observation cannot be honestly claimed re-executable later against the same state unless a later contract snapshots or otherwise immutably identifies that observation context.

This is research only. No source observer, snapshot manifest, retained-byte object, resolver, or observation-result schema is authorized by this overlay.

## Active lane boundaries

### Lane 01 — current owner

Finish the Decision 021 research question around observation-context identity and replay/re-execution standing. The next durable research packet should compare at least:

- immutable/snapshot-like observation context;
- retained verified bytes for positive exact observations;
- explicit context-bound/non-reexecution standing for missing/corrupt live-store observations.

It must identify the smallest universal contract that does not make a mutable filesystem path, process identity, host, actor, recency, CI run, or Git state into source authority.

### Lane 02 — held

Do not implement target availability/retrieval observation until Lane 01 opens a later numbered implementation decision. Preserve Decision 022 and its regression suite unchanged.

### Lane 03 — available for attack

Preserve ADV-057 unchanged as regression evidence. Attack the next bounded observation decision only after Lane 01 opens it durably. Priority future attacks include mutable-context laundering, negative-observation globalisation, retained-byte provenance laundering, hidden locator fallback, occurrence collapse, and observation→trust/closure/acceptance authority.

## Still explicitly unresolved

- immutable/snapshot-like source observation context identity versus an explicit non-reexecution limitation;
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

## Stop rule for the next activation

Do not open a target-observation implementation merely because Decision 022 is green and canonical. First make the observation context and re-execution claim explicit enough that a replacement occupant can distinguish recorded institutional replay from literal re-execution of a mutable live store.
