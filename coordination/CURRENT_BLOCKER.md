# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current canonical source precursor: **Decision 022 — Exact Source Runtime Capability Facts**
Current executable source gate: **Decision 023 — Exact Source Live Observation Facts**
Current disposition: **Decision 023 remains blocked. Lane 02 repaired ADV-058-C on an exact current-main candidate with 454/454 full deterministic tests plus compile, but Lane 03 independently reproduced a newer ADV-058-D failure on the same interpretation-coherence boundary. Direct `store.__dict__["schema_dir"]` rebinding can bypass the invocation-local `__setattr__` guard during the actual target-validation call and restore visible state before the observer checks it. Do not integrate PR #112 until the smallest bounded repair is implemented and ADV-058-A/B/C/D are independently rechecked unchanged.**

This file is the current sequencing pointer. Earlier overlays, Decisions 020–023, specialist red/green runs, and return packets remain historical evidence and are not invalidated or rewritten. `coordination/CURRENT_WAVE.md` remains historical chronology and must not override newer repository evidence.

## Activation-start canonical base

Lane 01 Activation 054 began from canonical `main`:

`a99c3b6aeedaea82f2830783ad0109910e1d8d7c`

Decision 022 production integration remains:

`ae2a4171dac0c6bb56b86ac11fc4b987924b4a94`

Decision 022 still establishes only bundled-runtime interpretation capability for one exact typed source occurrence. Runtime capability is not target existence, availability, retrieval, integrity, provenance causality, trust, closure, acceptance, integration, epoch completion, or replay correctness.

## Decision 023 contract still in force

Decision 023 remains a bounded live mutable local-store observation contract. It still requires:

- one exact typed `exact_axm_object` declaration occurrence;
- Decision 022 capability derived for that same occurrence;
- no target I/O for unsupported kinds;
- exact target validation only for supported kinds;
- the **same fixed function-owned bundled schema interpretation context** for capability classification and actual exact target validation inside one observation invocation;
- caller-supplied/custom schema contexts rejected before target I/O;
- no logical-id, newest-version, recency, locator, search, network, package, actor, CI, branch, Git, or schedule fallback;
- exact occurrence identity preserved;
- explicit availability/retrieval/integrity dimensions;
- `context_standing = live_mutable_store`;
- `reexecution_standing = not_established`.

Decision 023 still does **not** authorize immutable historical snapshots, retained-byte evidence, generic resolvers, trust/quality policy, closure, packet acceptance, claim closure, Stage 5 integration, epochs/barriers, or replay-success semantics.

## Lane 02 ADV-058-C repair evidence — A/B/C cleared on exact tested surface

Open PR #112 remains the Decision 023 implementation/repair lane.

Exact semantic/test-bearing Lane 02 head:

`69a5a11f3a26155779596c21195a82da02f6f04f`

Exact tested current-main merge candidate against canonical `a99c3b6aeedaea82f2830783ad0109910e1d8d7c`:

`c98fedc8bf5a6c70b771cd01e96eb292817c3458`

Native run / job:

- run: `34874022979`;
- job: `104076636830`;
- Ubuntu 24.04.5;
- Python 3.12.14;
- jsonschema 4.26.0.

Directly recorded evidence:

1. Decision 020 ADV-054/055 unchanged oracle: **6/6 passed**.
2. Decision 022 ADV-057-A–F unchanged oracle: **6/6 passed**.
3. Decision 023 ADV-058-A/B/C unchanged oracle: **3/3 passed**.
4. Decision 023 focused suite: **14/14 passed**.
5. Complete deterministic discovery: **454/454 passed**.
6. Explicit compile: **passed**.

Lane 02's bounded repair adds an invocation-local class guard preventing ordinary `schema_dir` reassignment away from the function-owned schema snapshot during the target load. This is valid evidence that the demonstrated ADV-058-C ordinary assignment path was repaired on that exact surface. Lane 02 explicitly did **not** claim protection against direct instance-dictionary mutation or general hostile same-process isolation.

## Lane 03 ADV-058-D — independent remaining counterexample

Open PR #121 is deliberately stacked on exact Lane 02 repaired ancestry so the repair can be attacked without reconstructing production code.

Lane 03 exact test/workflow-bearing head:

`db43800b9ad640dd0aeef01963c0d6a6992eba6b`

Current documentation descendant:

`3917bb00a574b4da51a723b5062d058d64abda16`

Exact tested PR #121 merge candidate:

`629f9671f4b20860dd514d2114704e5612efdb51`

Native run / job:

- run: `34875668880`;
- job: `104082109046`;
- Ubuntu 24.04.5;
- Python 3.12.14;
- jsonschema 4.26.0.

Recorded sequence:

1. Decision 020 ADV-054/055: **6/6 passed**.
2. Decision 022 ADV-057: **6/6 passed**.
3. ADV-058-A/B/C unchanged: **3/3 passed**.
4. ADV-058-D: **failed** with `AssertionError: SourceLiveObservationError not raised`.
5. Lane 02 Decision 023 focused suite: **skipped after targeted D failure**.
6. Complete deterministic suite: **skipped after targeted D failure**.
7. Explicit compile: **skipped after targeted D failure**.

### What ADV-058-D demonstrates

The ADV-058-C guard intercepts ordinary attribute assignment, but the actual base validation still consumes `store.schema_dir`, which remains caller-writable mutable instance state.

An exact `FilesystemObjectStore` instance can therefore:

1. satisfy the exact-type gate;
2. enter the observation with the function-owned snapshot directory installed;
3. keep a caller-shadowed exact-instance `load_bytes` operation;
4. directly mutate `store.__dict__["schema_dir"]` to a caller-owned permissive schema only during the base-class validation call;
5. call `FilesystemObjectStore.load_bytes(store, ...)` under that alternate interpretation;
6. restore the function-owned snapshot directory before returning.

The class `__setattr__` guard is bypassed, post-call visible state appears correct, and a normal observation fact can be emitted even though capability classification and target integrity used different interpretation contexts.

The bounded blocker is therefore:

> Decision 023 cannot rely on caller-writable `store.schema_dir` state during the actual validation operation. The target-validation operation must consume the same function-owned interpretation context as capability classification, or fail closed on the demonstrated path.

This remains the same Decision 023 same-invocation interpretation-coherence surface. It is not evidence that immutable snapshots, retained bytes, generic resolvers, trust policy, Stage 5, epochs, replay, or broad hostile-process isolation must be opened now.

## Smallest repair boundary

### Lane 01 — integration owner

Decision 023 integration remains **held**. Do not merge PR #112 while ADV-058-D remains red. Do not merge PR #121 as production history; it is adversarial evidence on Lane 02 ancestry.

PR #119 remains historically valid ADV-058-C evidence but is superseded as the active adversarial lane by PR #121, which preserves A/B/C and adds D.

### Lane 02 — bounded repair owner

Repair only ADV-058-D's demonstrated direct-instance interpretation-rebinding hole.

The repair must make the **actual target-validation operation** consume the same function-owned interpretation context as capability classification without relying on caller-writable `store.schema_dir` state during validation, or fail closed on the demonstrated path.

Do not broaden the repair into general hostile-process isolation. The implementation mechanism belongs to Lane 02 evidence; Lane 01 does not prescribe a specific design.

After the repair, rerun unchanged:

- Decision 020 ADV-054/055;
- Decision 022 ADV-057;
- ADV-058-A;
- ADV-058-B;
- ADV-058-C;
- ADV-058-D;
- Decision 023 focused suite;
- complete deterministic suite;
- explicit compile.

### Lane 03 — independent recheck owner

After Lane 02 publishes an exact repaired head, rerun **ADV-058-A/B/C/D unchanged** against that exact surface. Do not weaken the oracle to fit the repair. Attack only a nearby same-contract path if repository evidence justifies it; do not silently widen the decision into general hostile-process isolation.

## Root grounding

**Truth:** Lane 02's A/B/C green evidence and Lane 03's newer D red evidence are both preserved with exact heads and native run identity. The newer counterexample narrows the claim; it does not erase earlier green evidence.

**Agency / non-domination:** no lane, founder, CI result, branch recency, PR mergeability, schedule position, or Git permission can convert the blocked implementation into canon.

**Continuity:** exact canonical base, semantic heads, tested merge candidates, run/job ids, skipped downstream checks, owner boundaries, uncertainty, and next action are durable repository state so a replacement occupant can continue without private chat memory.

**Wisdom before speed:** repair only the demonstrated actual-validation-context hole before expanding source observation or advancing toward Stage 5.

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

Do not integrate Decision 023 while ADV-058-D remains red. The next executable lane is Lane 02's smallest actual target-validation interpretation-context repair. After repair, require unchanged ADV-058-A/B/C/D plus full deterministic and compile evidence, followed by an independent Lane 03 recheck, before Lane 01 reconsiders canonical integration.
