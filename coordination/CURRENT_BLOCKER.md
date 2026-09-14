# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current canonical source precursor: **Decision 022 — Exact Source Runtime Capability Facts**
Current executable source gate: **Decision 023 — Exact Source Live Observation Facts**
Current disposition: **Decision 023 remains blocked. Lane 02 repaired ADV-058-A and ADV-058-B on its exact tested surface, but Lane 03 independently reproduced a new ADV-058-C failure on the same interpretation-coherence boundary: an exact `FilesystemObjectStore` instance can shadow its own `load_bytes` method, temporarily substitute a caller-owned schema context during target validation, restore visible state before return, and evade the exact-type plus post-call checks. Do not integrate PR #112 until the smallest bounded repair is implemented and ADV-058-A/B/C are independently rechecked unchanged.**

This file is the current sequencing pointer. Earlier overlays, red and green specialist runs, Decisions 020–023, and return packets remain historical evidence and are not invalidated or rewritten. `coordination/CURRENT_WAVE.md` remains historical chronology and must not override newer repository state.

## Activation-start canonical base

Lane 01 Activation 053 began from canonical `main`:

`3f67901f16934dd15dba0457d7538cac3fc05abc`

That commit preserves the ADV-058-B hold and changes no Decision 023 production runtime itself.

Decision 022 production integration remains:

`ae2a4171dac0c6bb56b86ac11fc4b987924b4a94`

Decision 022 still establishes only bundled-runtime interpretation capability for one exact typed source occurrence. Runtime capability is not target existence, availability, retrieval, integrity, provenance causality, trust, closure, acceptance, integration, epoch completion, or replay correctness.

## Decision 023 contract that remains in force

Decision 023 remains a bounded live mutable local-store observation contract. It still requires:

- one exact typed `exact_axm_object` declaration occurrence;
- Decision 022 capability derived for that same exact occurrence;
- no target I/O for unsupported kinds;
- exact target validation only for supported kinds;
- the **same fixed bundled kernel schema interpretation context** for capability classification and exact target validation inside one observation invocation;
- caller-supplied/custom `schema_dir` rejected before target I/O;
- no logical-id, newest-version, recency, locator, search, network, package, adjacent-source, actor, CI, branch, Git, or schedule fallback;
- exact occurrence identity preserved;
- explicit availability/retrieval/integrity dimensions;
- `context_standing = live_mutable_store`;
- `reexecution_standing = not_established`.

Decision 023 still does **not** authorize immutable historical snapshots, retained-byte evidence, generic resolvers, trust/quality policy, closure, packet acceptance, claim closure, Stage 5 integration, epochs/barriers, or replay-success semantics.

## Lane 02 ADV-058-B repair evidence — A/B cleared on exact tested surface

Open PR #112 remains the Decision 023 implementation/repair PR.

Current Lane 02 documentation head inspected by this activation:

`c066fb30c6af081006dfae9a73300c26c7e4fe0f`

Exact semantic/test-bearing Lane 02 head from Activation 051:

`0a4f2d06adf5b86f749ef2ff8aa7b219b4538fa8`

Exact tested PR merge candidate recorded by Lane 02 against activation-start canonical base `3f67901f16934dd15dba0457d7538cac3fc05abc`:

`6314099ec90506970606f3cb513492d8ded234b0`

Native run / job:

- run: `34867538927`;
- job: `104055104208`;
- Ubuntu 24.04.5;
- Python 3.12.14;
- jsonschema 4.26.0.

Directly recorded evidence:

1. Decision 020 ADV-054/055 unchanged oracle: **6/6 passed**.
2. Decision 022 ADV-057-A–F unchanged oracle: **6/6 passed**.
3. Decision 023 ADV-058-A/B unchanged oracle: **2/2 passed**.
4. Decision 023 focused suite: **14/14 passed**.
5. Complete deterministic discovery: **453/453 passed**.
6. Explicit compile: **passed**.

Lane 02's bounded repair rejects subclass dispatch by requiring the exact `FilesystemObjectStore` implementation type. This is valid evidence that the demonstrated ADV-058-B subclass override path was repaired on that exact surface. Lane 02 explicitly did **not** claim general hostile same-process isolation or impossibility of exact-instance method shadowing.

## Lane 03 ADV-058-C — independent remaining counterexample

Open PR #119 is deliberately stacked on exact Lane 02 repaired ancestry so the repair can be attacked without reconstructing production code.

Current PR #119 head inspected by this activation:

`9e520788857210a28080eb1eb1d35d9d83ab24f6`

Lane 03's return packet identifies the exact Lane 02 repaired head under attack as:

`0a4f2d06adf5b86f749ef2ff8aa7b219b4538fa8`

and the original ADV-058-C test-bearing head as:

`a7ac81a54d20a37f5359d2c92f871c438e4661ea`

Lane 03 preserved ADV-058-A and ADV-058-B unchanged and added only ADV-058-C on the same same-invocation interpretation-coherence surface.

Initial native red run / job recorded by Lane 03:

- run: `34868913051`;
- job: `104059656415`.

Recorded sequence:

1. Decision 020 ADV-054/055: **6/6 passed**.
2. Decision 022 ADV-057: **6/6 passed**.
3. Decision 023 adversarial suite: **3 tests run**.
4. ADV-058-A: **passed**.
5. ADV-058-B: **passed**.
6. ADV-058-C: **failed** with `AssertionError: SourceLiveObservationError not raised`.
7. Lane 02 Decision 023 focused suite: **skipped after adversarial failure**.
8. Complete deterministic suite: **skipped after adversarial failure**.
9. Explicit compile: **skipped after adversarial failure**.

The current PR #119 documentation descendant was independently inspected by Lane 01 and remains red in native run `34869046174`, job `104060091542`: Decision 020 and Decision 022 adversarial steps passed; the Decision 023 adversarial step failed; focused Decision 023 tests, full discovery, and compile were skipped. No new full-suite or compile claim is made from either red run.

### What ADV-058-C demonstrates

The ADV-058-B repair correctly rejects subclasses, but the observer still invokes target validation through the caller-owned instance attribute `store.load_bytes(...)`.

An exact base-store instance can therefore:

1. satisfy `type(store) is FilesystemObjectStore`;
2. enter with `schema_dir is None`;
3. receive the observer-owned temporary bundled-schema directory;
4. have only its instance `load_bytes` attribute shadowed for the observation;
5. inside that replacement, save the observer-owned schema directory;
6. temporarily rebind `store.schema_dir` to a caller-owned permissive schema directory;
7. directly call `FilesystemObjectStore.load_bytes(store, ...)`, so ordinary exact validation occurs under the alternate interpretation;
8. restore the observer-owned schema directory before returning.

The exact-type check still passes and the post-call schema-dir equality check sees the expected value. A normal observation fact can therefore be emitted even though capability classification and target-integrity validation used different interpretation contexts.

The bounded blocker is therefore:

> Exact class identity is not sufficient while the actual target-validation call remains replaceable through caller-owned per-instance method dispatch. Decision 023 must bind that validation operation to the same function-owned interpretation context as capability classification, or fail closed.

This is still the same Decision 023 same-invocation interpretation-coherence surface. It is not evidence that immutable snapshots, retained source bytes, generic resolvers, trust policy, Stage 5, epochs, replay, or broad hostile-process isolation must be opened now.

## Smallest repair boundary

### Lane 01 — integration owner

Decision 023 integration remains **held**. Do not merge PR #112 while ADV-058-C remains red. Do not merge stacked PR #119 as production history; it is adversarial evidence on Lane 02 ancestry.

PR #117 remains historically valid ADV-058-B evidence for the prior repair surface but is superseded as the active adversarial lane by PR #119, which preserves A/B and adds C.

### Lane 02 — bounded repair owner

Repair only ADV-058-C's demonstrated exact-instance validation-dispatch hole.

The repair must make the **actual target-validation operation** consume the same function-owned interpretation context as capability classification, or fail closed.

Do not solve this only with exact-class identity or before/after equality of mutable caller-owned attributes. A bounded repair may bind directly to a non-shadowed function-owned/base validation path, reject relevant instance-level method shadowing before target I/O, or use another deterministic mechanism demonstrated by unchanged evidence. The implementation choice belongs to Lane 02 evidence, not Lane 01 preference.

After the repair, rerun unchanged:

- Decision 020 ADV-054/055;
- Decision 022 ADV-057;
- ADV-058-A;
- ADV-058-B;
- ADV-058-C;
- Decision 023 focused suite;
- complete deterministic suite;
- explicit compile.

### Lane 03 — independent recheck owner

After Lane 02 publishes an exact repaired head, rerun **ADV-058-A/B/C unchanged** against that exact surface. Do not weaken the oracle to fit the repair. Attack only a nearby validation-dispatch/context-rebinding path if repository evidence justifies it; do not silently widen the contract into general hostile-process isolation.

## Root grounding

**Truth:** Lane 02's A/B green evidence and Lane 03's newer C red evidence are both preserved with exact heads and run identity. The newer counterexample narrows the claim; it does not erase the earlier green evidence.

**Agency / non-domination:** no lane, founder, CI result, branch recency, PR mergeability, schedule position, or Git permission can convert the blocked implementation into canon.

**Continuity:** exact canonical base, semantic heads, adversarial test surface, run/job ids, skipped downstream checks, ownership, uncertainty, and next action are durable repository state so a replacement occupant can continue without private chat memory.

**Wisdom before speed:** repair only the demonstrated exact-instance validation-dispatch hole before expanding source observation or advancing toward Stage 5.

## Still explicitly unresolved

- immutable/snapshot-like source observation context identity and snapshot completeness;
- retained verified source bytes / retained-byte evidence objects;
- custom/non-bundled source-observation schema-context identity/configuration;
- content-address byte-provider and digest verification semantics;
- locator/network/filesystem/package resolver contracts and resolver identity/configuration;
- explicit locator/content/exact association;
- historical-to-typed migration objects;
- provenance-relation vocabulary;
- source trust/quality/relevance/completeness/closure;
- dependency admissibility / satisfaction / closure;
- evidence method/source quality, precedence, invalidation dominance, and closure;
- multiple `required_states` semantics;
- packet acceptance/rejection and durable closure;
- claim closure;
- successor state-revision publication;
- Stage 5 integration receipts/runtime;
- epochs/barriers and replay;
- cross-language graph/reachability/frontier/source-observation reproduction;
- exact self/mutual-cycle authorability through ordinary content-addressed publication;
- stronger filesystem durability/concurrency evidence;
- hostile same-process code isolation beyond the bounded trusted deterministic runtime contract.

## Stop rule for the next activation

Do not integrate Decision 023 while ADV-058-C remains red. The next executable lane is Lane 02's smallest exact-instance target-validation dispatch repair. After repair, require unchanged ADV-058-A/B/C plus full deterministic and compile evidence, followed by an independent Lane 03 recheck, before Lane 01 reconsiders canonical integration.
