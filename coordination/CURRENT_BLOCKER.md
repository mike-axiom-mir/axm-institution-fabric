# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current canonical source precursor: **Decision 022 — Exact Source Runtime Capability Facts**
Current executable source gate: **Decision 023 — Exact Source Live Observation Facts**
Current disposition: **Decision 023 remains blocked. Lane 02 repaired ADV-058-D on an exact current-main candidate with 455/455 full deterministic tests plus compile, and Lane 03 independently cleared preserved ADV-058-A/B/C/D on that repaired ancestry. Lane 03 then reproduced ADV-058-E: caller-owned exact-instance `load_bytes` dispatch can return arbitrary bytes without exact-path I/O or immutable identity verification, yet the observer emits `exact_observed`. Do not integrate PR #112 until the smallest bounded validation-dispatch repair is implemented and ADV-058-A/B/C/D/E are independently rechecked unchanged.**

This file is the current sequencing pointer. Earlier overlays, Decisions 020–023, specialist red/green runs, and return packets remain historical evidence and are not invalidated or rewritten. `coordination/CURRENT_WAVE.md` remains historical chronology and must not override newer repository evidence.

## Activation-start canonical base

Lane 01 Activation 055 began from canonical `main`:

`734b1f4c7bf20261735ababe0ace89173628af43`

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
- a normal `exact_observed` result only when the exact target was actually read and immutable identity verification succeeded;
- no logical-id, newest-version, recency, locator, search, network, package, actor, CI, branch, Git, or schedule fallback;
- exact occurrence identity preserved;
- explicit availability/retrieval/integrity dimensions;
- `context_standing = live_mutable_store`;
- `reexecution_standing = not_established`.

Decision 023 still does **not** authorize immutable historical snapshots, retained-byte evidence, generic resolvers, trust/quality policy, closure, packet acceptance, claim closure, Stage 5 integration, epochs/barriers, or replay-success semantics.

## Lane 02 ADV-058-D repair evidence — A/B/C/D cleared on exact tested surface

Open PR #112 remains the Decision 023 implementation/repair lane.

Exact semantic/test-bearing Lane 02 head:

`ec563d0e4f07cb6aeee776246c7705a41bf6a0db`

Exact tested current-main merge candidate against canonical `734b1f4c7bf20261735ababe0ace89173628af43`:

`294ecf4324950f863bb6f8f57bbe24a096882d82`

Native run / job:

- run: `34879477099`;
- job: `104094887604`;
- Ubuntu 24.04.5;
- Python 3.12.14;
- jsonschema 4.26.0.

Directly recorded evidence:

1. Decision 020 ADV-054/055 unchanged oracle: **6/6 passed**.
2. Decision 022 ADV-057-A–F unchanged oracle: **6/6 passed**.
3. Decision 023 ADV-058-A/B/C unchanged oracle: **3/3 passed**.
4. Decision 023 ADV-058-D unchanged oracle: **1/1 passed**.
5. Decision 023 focused suite: **14/14 passed**.
6. Complete deterministic discovery: **455/455 passed**.
7. Explicit compile: **passed**.

Lane 02's bounded D repair replaced the prior assignment-only schema guard with an invocation-local `schema_dir` data descriptor so actual base-store interpretation reads resolve to the function-owned schema snapshot or fail closed if backing state diverges. This is valid evidence that the demonstrated ADV-058-D schema-context rebinding path was repaired on that exact surface. It is not a broad hostile-process isolation claim.

## Lane 03 ADV-058-E — independent remaining counterexample

Open PR #123 is deliberately stacked on exact Lane 02 repaired ancestry so the repair can be attacked without reconstructing production code.

Lane 03 exact test/workflow-bearing head:

`5c2e63f12d910c6fe6f4b2b7f59598db08d28cdf`

Current documentation descendant:

`4f8f9987eb17bc5331694259d6ad098864cbcc4c`

Exact tested PR #123 merge candidate:

`ae490ca3e8d9184bf78bb1d6069803736a888b34`

Native run / job:

- run: `34881363334`;
- job: `104101179426`;
- Ubuntu 24.04.5;
- Python 3.12.14;
- jsonschema 4.26.0.

Recorded sequence:

1. Decision 020 ADV-054/055: **6/6 passed**.
2. Decision 022 ADV-057: **6/6 passed**.
3. ADV-058-A/B/C unchanged: **3/3 passed**.
4. ADV-058-D unchanged: **1/1 passed**.
5. ADV-058-E: **failed** with `AssertionError: 'not_found_in_live_context' != 'exact_observed'` and fixture message `caller-shadowed load_bytes must not forge exact_observed`.
6. Lane 02 Decision 023 focused suite: **skipped after targeted E failure**.
7. Complete deterministic suite: **skipped after targeted E failure**.
8. Explicit compile: **skipped after targeted E failure**.

### What ADV-058-E demonstrates

The newest schema-context repair keeps the actual interpretation coherent when the base verifier runs, but the observer still invokes target validation through caller-visible instance dispatch:

`store.load_bytes(capability.target_object_ref)`

An exact `FilesystemObjectStore` instance can retain a caller-owned instance-level `load_bytes` shadow. ADV-058-E gives that shadow an exact target that is absent from the live store and has the shadow return arbitrary bytes immediately without reading the exact object path and without running immutable identity verification. The observer currently treats the no-error return as sufficient proof and emits `exact_observed`.

The bounded blocker is therefore:

> Decision 023 cannot treat caller-owned instance `load_bytes` dispatch returning without error as evidence that the exact target read and immutable identity verification occurred. A normal `exact_observed` result must be grounded in the actual exact-store validation operation under the same function-owned interpretation context, or the observer must fail closed.

This remains the same Decision 023 actual-target-validation surface. It is not evidence that immutable snapshots, retained bytes, generic resolvers, trust policy, Stage 5, epochs, replay, or general hostile-process isolation must be opened now.

## Smallest repair boundary

### Lane 01 — integration owner

Decision 023 integration remains **held**. Do not merge PR #112 while ADV-058-E remains red. Do not merge PR #123 as production history; it is adversarial evidence on Lane 02 ancestry.

PR #121 remains historically valid ADV-058-D evidence but is superseded as the active adversarial lane by PR #123, which preserves A/B/C/D and adds E.

### Lane 02 — bounded repair owner

Repair only ADV-058-E's demonstrated caller-owned validation-dispatch hole.

The repair must ensure that a normal `exact_observed` result is grounded in the actual exact-store read and immutable identity verification under the same function-owned interpretation context. Caller-owned instance `load_bytes` dispatch returning without error is not sufficient evidence by itself.

A grounded repair may bind validation to non-caller-owned exact-store behavior, independently verify the result, fail closed on caller-owned dispatch, or use another smaller mechanism that satisfies the existing Decision 023 contract. Do not broaden the repair into general hostile-process isolation.

After the repair, rerun unchanged:

- Decision 020 ADV-054/055;
- Decision 022 ADV-057;
- ADV-058-A;
- ADV-058-B;
- ADV-058-C;
- ADV-058-D;
- ADV-058-E;
- Decision 023 focused suite;
- complete deterministic suite;
- explicit compile.

### Lane 03 — independent recheck owner

After Lane 02 publishes an exact repaired head, rerun **ADV-058-A/B/C/D/E unchanged** against that exact surface. Do not weaken the oracle to fit the repair. Attack only a nearby same-contract path if repository evidence justifies it; do not silently widen the decision into an unbounded same-process security project.

## Root grounding

**Truth:** Lane 02's A/B/C/D green evidence and Lane 03's newer E red evidence are both preserved with exact heads and native run identity. The E counterexample narrows the integration claim; it does not erase earlier green evidence.

**Agency / non-domination:** no lane, founder, CI result, branch recency, PR mergeability, schedule position, caller dispatch, or Git permission can convert a false-positive observation into institutional truth or authorize the blocked implementation into canon.

**Continuity:** exact canonical base, semantic heads, tested merge candidates, run/job ids, skipped downstream checks, owner boundaries, uncertainty, and next action are durable repository state so a replacement occupant can continue without private chat memory.

**Wisdom before speed:** repair only the demonstrated actual-validation-dispatch hole before expanding source observation or advancing toward Stage 5.

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

Do not integrate Decision 023 while ADV-058-E remains red. The next executable lane is Lane 02's smallest actual target-validation dispatch repair. After repair, require unchanged ADV-058-A/B/C/D/E plus full deterministic and compile evidence, followed by an independent Lane 03 recheck, before Lane 01 reconsiders canonical integration.
