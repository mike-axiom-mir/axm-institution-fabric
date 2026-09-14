# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current canonical source precursor: **Decision 022 — Exact Source Runtime Capability Facts**
Current executable source gate: **Decision 023 — Exact Source Live Observation Facts**
Current disposition: **Decision 023 is blocked by independently reproduced ADV-058-A. Lane 02's green implementation baseline remains valid evidence for its tested surface, but the exact implementation can combine Decision 022 capability classification under one live bundled schema interpretation with target validation under a different live bundled schema interpretation during the same observation invocation. Do not integrate PR #112 until the smallest bounded repair is implemented and the unchanged adversarial oracle is independently rechecked.**

This file is the current sequencing pointer. Earlier overlays, red and green specialist runs, Decisions 020–023, and return packets remain historical evidence and are not invalidated or rewritten. `coordination/CURRENT_WAVE.md` remains historical chronology and must not override newer repository state.

## Canonical state inspected

Canonical `main` at this lead activation began at:

`7859f1b89387dd4765d2056ff0955a7eb57beeaf`

That commit records Lane 02 Activation 049 as verification-only continuity evidence. It changes no production runtime, schema, fixture, test, workflow, source-observation, Stage 5, epoch, or replay semantics.

Decision 022 production integration remains commit:

`ae2a4171dac0c6bb56b86ac11fc4b987924b4a94`

Decision 022 still establishes only bundled-runtime interpretation capability for one exact typed source occurrence. Runtime capability is not target existence, availability, retrieval, integrity, provenance causality, trust, closure, acceptance, integration, epoch completion, or replay correctness.

## Decision 023 contract that remains in force

Decision 023 remains a bounded live mutable local-store observation contract. It still requires:

- one exact typed `exact_axm_object` declaration occurrence;
- Decision 022 capability derived for that same exact occurrence;
- no target I/O for unsupported kinds;
- exact `FilesystemObjectStore.load_bytes(target_object_ref)` only for supported kinds;
- the **same fixed bundled kernel schema interpretation context** for capability classification and exact target observation;
- custom/caller-supplied `schema_dir` rejected before target I/O;
- no logical-id, newest-version, recency, locator, search, network, package, adjacent-source, actor, CI, branch, Git, or schedule fallback;
- exact occurrence identity preserved;
- explicit availability/retrieval/integrity dimensions;
- `context_standing = live_mutable_store`;
- `reexecution_standing = not_established`.

Decision 023 still does **not** authorize immutable snapshots, retained-byte objects, generic resolvers, trust/quality policy, closure, packet acceptance, claim closure, Stage 5 integration, epochs/barriers, or replay-success semantics.

## Lane 02 Decision 023 implementation baseline — green on its demonstrated surface

Open PR #112 remains the implementation PR.

Current Lane 02 PR head:

`023de7bd8bd0a16178ad0351bb2232e631cf5e69`

Lane 02 Activation 049 recorded the fresh current-base GitHub Actions merge candidate:

`4099d85252c90398c7a8b677d9f63a32e13e6aa5`

That candidate was `023de7bd...` merged against then-canonical `43c7e709e97fc3c817da85d07041d134d7ba536d` and recorded:

- Decision 020 ADV-054/055 unchanged oracle: **6/6 passed**;
- Decision 022 ADV-057 unchanged oracle: **6/6 passed**;
- Decision 023 focused implementation suite: **14/14 passed**;
- complete deterministic suite: **451/451 passed**;
- explicit compile: **passed**.

This green evidence remains valid for that exact tested surface. It is not invalidated by ADV-058-A, but it also did not test the newly demonstrated same-invocation bundled-schema substitution failure.

## Lane 03 ADV-058-A — independent red counterexample

Open PR #115 is deliberately stacked on exact Lane 02 PR #112 head `023de7bd8bd0a16178ad0351bb2232e631cf5e69` so the counterexample is attributable to the implementation surface rather than a reconstructed copy.

Current Lane 03 PR head:

`d551da2fffbc66ee43b3369291b3024b3dcb079e`

GitHub Actions tested PR #115 merge candidate:

`4c9759d492aa74037e4fa9167ea4df3347a03dd9`

Directly inspected native run:

- workflow run: `34857492622`;
- job: `104020715891`;
- checkout: `4c9759d492aa74037e4fa9167ea4df3347a03dd9`;
- Ubuntu 24.04.5;
- Python 3.12.14;
- jsonschema 4.26.0.

Observed sequence:

1. Decision 020 ADV-054/055 oracle: **6/6 passed**.
2. Decision 022 ADV-057 oracle: **6/6 passed**.
3. ADV-058-A: **1 test run, 1 failure**.
4. Exact failure: `AssertionError: SourceLiveObservationError not raised`.
5. Lane 02 Decision 023 focused suite: **skipped after the adversarial failure**.
6. Complete deterministic suite: **skipped after the adversarial failure**.
7. Explicit compile: **skipped after the adversarial failure**.

Therefore ADV-058-A creates **no new full-suite or compile claim**. The earlier 451/451 + compile evidence remains attached only to its exact green candidate.

## What ADV-058-A demonstrates

The current observer first derives Decision 022 capability, then later calls `store.load_bytes(target_object_ref)`. For the bundled context, both phases ultimately consult live schema material from the bundled schema directory.

ADV-058-A changes only the relevant bundled target-kind schema after capability classification and immediately before the exact store load, using a different valid permissive JSON Schema. The store then loads under that substituted interpretation, and the current Decision 023 observer does **not** fail closed.

The bounded blocker is therefore:

> One Decision 023 fact can currently combine capability classification and target-integrity evaluation from different live bundled schema interpretations within a single invocation, despite the contract requiring one fixed bundled interpretation context.

This is not evidence that Decision 023 needs an immutable historical snapshot, retained source bytes, a generic resolver, trust policy, or replay implementation. It is evidence only that the current implementation has not yet made **single-invocation interpretation coherence** true.

## Smallest repair boundary

### Lane 01 — integration owner

Decision 023 integration remains **held**. Do not merge PR #112 while ADV-058-A is red. Do not merge stacked PR #115 as production history; it is adversarial evidence on Lane 02 ancestry. Preserve its red evidence explicitly.

### Lane 02 — bounded repair owner

Repair only the demonstrated same-invocation interpretation-coherence failure.

The repair must make it true that the capability and target-validation dimensions in one Decision 023 fact are evaluated under one coherent bundled schema interpretation, or else fail closed before emitting a normal observation fact.

Do not broaden into immutable historical snapshots, custom schema contexts, retained bytes, generic resolvers, trust/closure, packet acceptance, Stage 5 integration, epochs, or replay.

A repair should not rely only on a before/after equality check of mutable schema files as proof of coherence: a swap-and-restore race can in principle occur between checkpoints. Evidence should instead demonstrate that the interpretation actually used for capability and target validation is one bounded invocation context, or that any inability to establish that fact fails closed.

After the repair, rerun:

- unchanged Decision 020 ADV-054/055;
- unchanged Decision 022 ADV-057;
- unchanged ADV-058-A;
- the Decision 023 focused suite;
- the complete deterministic suite;
- explicit compile.

### Lane 03 — independent recheck owner

After Lane 02 publishes an exact repaired head, rerun **ADV-058-A unchanged** against that exact surface. Do not weaken the oracle to fit the repair. Then attack only the same Decision 023 interpretation-coherence surface for nearby substitution/rebinding paths without opening broader source policy.

## Root grounding

**Truth:** both the green 451/451 baseline and the newer red ADV-058-A remain explicit. A green suite is not rewritten as invalid, and a newly demonstrated counterexample is not hidden by prior success.

**Agency / non-domination:** no lane, founder, CI result, branch recency, PR mergeability, schedule position, or Git permission can convert the blocked implementation into canon.

**Continuity:** exact heads, merge candidates, run/job ids, failure state, ownership, and next action are durable repository state so a replacement occupant can continue without this chat.

**Wisdom before speed:** repair only the demonstrated coherence hole before expanding source observation or advancing toward Stage 5.

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
- cross-language graph/reachability/frontier/source-observation reproduction;
- exact self/mutual-cycle authorability through ordinary content-addressed publication;
- stronger filesystem durability/concurrency evidence;
- hostile same-process code isolation beyond the trusted deterministic runtime boundary.

## Stop rule for the next activation

Do not integrate Decision 023 while ADV-058-A remains red. The next executable lane is Lane 02's smallest coherence repair. After repair, require unchanged ADV-058-A plus full deterministic and compile evidence, followed by an independent Lane 03 recheck, before Lane 01 reconsiders canonical integration.
