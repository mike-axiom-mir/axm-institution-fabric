# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current canonical source precursor: **Decision 022 — Exact Source Runtime Capability Facts**
Current executable source gate: **Decision 023 — Exact Source Live Observation Facts**
Current disposition: **Decision 023 remains blocked. Lane 02 repaired ADV-058-A on its exact tested surface, but Lane 03 independently reproduced a nearby ADV-058-B failure showing that a caller-owned `FilesystemObjectStore` subclass can temporarily rebind its validation schema context during `load_bytes()`, restore the observer-owned value before return, and evade the current after-call drift check. Do not integrate PR #112 until the smallest bounded repair is implemented and ADV-058-A/B are independently rechecked unchanged.**

This file is the current sequencing pointer. Earlier overlays, red and green specialist runs, Decisions 020–023, and return packets remain historical evidence and are not invalidated or rewritten. `coordination/CURRENT_WAVE.md` remains historical chronology and must not override newer repository state.

## Canonical state inspected

Canonical `main` at this lead activation:

`7000fa873f6e1d9f460f4630925329edfed6bb7c`

That commit already preserves the earlier ADV-058-A hold. It changes no Decision 023 production runtime itself.

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

## Lane 02 repair evidence — ADV-058-A cleared on exact tested surface

Open PR #112 remains the Decision 023 implementation PR.

Current PR head is a documentation-only descendant:

`2e648567fe3d1f637596256fe497a44213513ac5`

Exact final semantic/test-bearing repair head from Lane 02 Activation 050:

`995bd8f44afdffe678a7531505a75a0fc468a1b7`

Exact merge candidate recorded by Lane 02 against canonical `7000fa873f6e1d9f460f4630925329edfed6bb7c`:

`bda6388ff0f1214c575b4e6dc8ec8a8fe8476690`

Native run / job:

- run: `34861302338`;
- job: `104033920424`.

Recorded final repair evidence:

- Decision 020 ADV-054/055 unchanged oracle: **green**;
- Decision 022 ADV-057 unchanged oracle: **green**;
- ADV-058-A unchanged oracle: **green**;
- Decision 023 focused suite: **green**;
- complete deterministic discovery: **green**;
- explicit compile: **green**.

The numerical complete-suite count `452` in the Lane 02 packet is explicitly source-accounting inference, not directly observed connector stdout.

A later workflow on documentation-only head `2e648567...` also completed every adversarial, focused, full-discovery, and compile step successfully in run `34862414958`, job `104037749096`. That workflow still contained only ADV-058-A on the Decision 023 adversarial surface; it does not answer ADV-058-B.

Lane 02's repair uses a function-owned temporary schema copy for both capability classification and target validation, plus ambient bundled-schema mutation checks. This is valid evidence that the original ambient swap/restore path from ADV-058-A was repaired.

## Lane 03 ADV-058-B — independent remaining counterexample

Open PR #117 is deliberately stacked on exact Lane 02 repaired ancestry so the repair is attacked without reconstructing production code.

Current PR head is a return-packet descendant:

`b620fb15f0cd334d6063155c1fefc07d1253afb0`

Exact adversarial test-bearing head recorded by Lane 03:

`b57075ed963284d8832f0f67f0001b45c555f91f`

Exact tested merge candidate recorded by Lane 03:

`845bd6a06a0dfb13876f86a9dd3e240e3074c6f5`

Native run / job:

- run: `34862323802`;
- job: `104037436583`.

Observed sequence:

1. Decision 020 ADV-054/055: **6/6 passed**.
2. Decision 022 ADV-057: **6/6 passed**.
3. Decision 023 adversarial suite: **2 tests run**.
4. ADV-058-A: **passed**.
5. ADV-058-B: **failed** with `AssertionError: SourceLiveObservationError not raised`.
6. Lane 02 Decision 023 focused suite: **skipped after adversarial failure**.
7. Complete deterministic suite: **skipped after adversarial failure**.
8. Explicit compile: **skipped after adversarial failure**.

The current PR #117 documentation descendant also produced a red workflow run `34862446978`; its Decision 020 and Decision 022 adversarial gates passed and the Decision 023 adversarial gate failed before focused/full/compile steps. No new full-suite or compile claim is made from either red run.

### What ADV-058-B demonstrates

Decision 023 currently accepts any object satisfying `isinstance(store, FilesystemObjectStore)` and temporarily assigns the function-owned snapshot directory to `store.schema_dir` before calling the caller-owned object's `load_bytes()` method.

A subclass can:

1. enter Decision 023 with `schema_dir is None`, passing the public custom-context rejection;
2. receive the observer-owned temporary schema directory;
3. inside its overridden `load_bytes()`, save that value;
4. rebind `self.schema_dir` to a caller-owned permissive schema directory;
5. execute ordinary exact `FilesystemObjectStore.load_bytes()` validation under that alternate interpretation;
6. restore the observer-owned value before returning.

The observer's current after-call equality check then sees the expected value and emits no `SourceLiveObservationError`, even though capability classification and target-integrity validation used different interpretation contexts.

The bounded blocker is therefore:

> Decision 023 has repaired ambient bundled-schema mutation, but it still does not force the actual target-validation operation to consume the same function-owned interpretation context when validation is dispatched through an overridable caller-owned store method.

This is the same Decision 023 same-invocation interpretation-coherence surface. It is not evidence that broader historical snapshots, retained source bytes, generic resolvers, trust policy, Stage 5, epochs, or replay must be opened now.

## Smallest repair boundary

### Lane 01 — integration owner

Decision 023 integration remains **held**. Do not merge PR #112 while ADV-058-B remains red. Do not merge stacked PR #117 as production history; it is adversarial evidence on Lane 02 ancestry.

The older PR #115 ADV-058-A evidence remains historically valid for its exact pre-repair surface, but it is superseded as the active open attack lane because ADV-058-A is now green on the repaired surface and PR #117 carries the preserved oracle plus the newer counterexample.

### Lane 02 — bounded repair owner

Repair only the demonstrated target-validation context-rebinding hole.

The repair must make it true that the **actual target-validation operation** uses the same function-owned interpretation context as capability classification, or else fails closed.

Do not rely only on before/after equality of mutable caller-owned store attributes. Do not broaden into general hostile-process isolation. Candidate bounded mechanisms may include preventing subclass dispatch on the validation path, forcing a function-owned validation helper over exact stored bytes, requiring the exact base store type for this first slice, or another deterministic mechanism that is directly tested. The implementation choice belongs to Lane 02 evidence, not Lane 01 preference.

After the repair, rerun:

- unchanged Decision 020 ADV-054/055;
- unchanged Decision 022 ADV-057;
- unchanged ADV-058-A;
- unchanged ADV-058-B;
- Decision 023 focused suite;
- complete deterministic suite;
- explicit compile.

### Lane 03 — independent recheck owner

After Lane 02 publishes an exact repaired head, rerun **ADV-058-A and ADV-058-B unchanged** against that exact surface. Do not weaken the oracle to fit the repair. Attack only nearby same-invocation interpretation-rebinding paths unless a new repository-grounded contradiction requires a wider decision.

## Root grounding

**Truth:** Lane 02's repaired-green ADV-058-A evidence and Lane 03's newer red ADV-058-B counterexample are both preserved with exact heads/run identity. Neither erases the other.

**Agency / non-domination:** no lane, founder, CI result, branch recency, PR mergeability, schedule position, or Git permission can convert the blocked implementation into canon.

**Continuity:** exact canonical base, semantic heads, documentation descendants, run/job ids, failure state, ownership, and next action are durable repository state so a replacement occupant can continue without this chat.

**Wisdom before speed:** repair only the demonstrated validation-context rebinding hole before expanding source observation or advancing toward Stage 5.

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

Do not integrate Decision 023 while ADV-058-B remains red. The next executable lane is Lane 02's smallest target-validation context-rebinding repair. After repair, require unchanged ADV-058-A/B plus full deterministic and compile evidence, followed by an independent Lane 03 recheck, before Lane 01 reconsiders canonical integration.
