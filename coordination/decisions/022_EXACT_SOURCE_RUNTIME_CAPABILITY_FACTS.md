# Decision 022 — Exact Source Runtime Capability Facts

Date: 2026-09-14
Status: **canonical on the bounded no-target-I/O bundled-runtime capability surface. Actual source observation remains outside this decision.**

Decision 021 research established that the current exact store can surface target-path outcomes before it has established whether the runtime supports the target kind. A direct target-availability observer would therefore risk collapsing runtime capability with source absence/corruption.

Decision 022 establishes the smallest deterministic precursor that removes that ambiguity without reading a source target path.

## Bounded objective

For one Decision 020 `exact_axm_object` declaration occurrence in an exact typed containing object, project a deterministic **kernel-bundled runtime capability fact**:

- preserve the exact containing-object identity;
- preserve the exact declaration key;
- preserve the exact authored target `object_ref`;
- preserve the parsed target kind;
- state only whether the **bundled AXM kernel contract set in this runtime** supports interpreting that kind.

This projection performs **no exact target object lookup** and is not a source resolver.

## First-slice input boundary

The canonical implementation consumes only:

1. an exact containing-object ref for a typed artifact v0.4 or evidence-record v0.2;
2. the corresponding validated containing-object value;
3. one declaration key that exists in that exact value and whose `source_class` is `exact_axm_object`.

The implementation verifies that the supplied containing value reproduces the supplied exact immutable reference. It extracts the declaration by exact key from that exact containing value. Logical-id lookup, newest-version lookup, `supersedes_ref`, array/map order, recency, actor, lane, branch, CI, or Git state may not substitute another containing object or declaration occurrence.

The target `object_ref` is consumed unchanged through the existing Stage 2 exact-reference parser.

## Runtime capability context — deliberately narrow

V0 Decision 022 covers the repository/package **bundled kernel schema context only**.

A target kind is `supported` only when its inferred bundled `<kind>.schema.json` contract exists and is a valid bundled kernel schema under the existing schema loader.

A canonical target kind with no bundled schema is `unsupported_kind`.

A bundled schema file that exists but cannot itself be read/decoded/validated is a **kernel/runtime configuration failure**, not an `unsupported_kind` result and not a source corruption result. The projection fails closed through `SourceRuntimeCapabilityContextError` rather than laundering that condition into source standing.

Custom/mutable `schema_dir` contexts are outside this first slice. They require an explicit context-identity decision later and must not silently enter through a hidden parameter or ambient filesystem fallback.

## Minimum result semantics

The implementation preserves named semantics equivalent to:

- `containing_object_ref`
- `declaration_key`
- `target_object_ref`
- `target_kind`
- `runtime_capability` = `supported` | `unsupported_kind`

The canonical implementation uses a canonical-byte-backed named fact. Transport/materialization must not turn these named facts into position-dependent meaning.

A result is attributable to the exact declaration occurrence, not only the target ref. Two declaration occurrences that name the same target may share internal computation but must yield occurrence-attributable results.

## Required behavior

### Supported bundled kind

If the target ref names a kind with a valid bundled kernel schema, return `supported`.

This means only:

> this runtime's bundled deterministic kernel has a contract with which it can attempt to interpret that exact AXM object kind.

It does **not** mean the target exists, is present in any store, is retrievable, is canonical, is uncorrupted, is trustworthy, is relevant, is complete, or is accepted.

### Unsupported canonical kind

If the target ref is canonical but names no bundled kernel schema, return `unsupported_kind`.

This means only:

> this runtime's bundled kernel does not currently provide an interpretation contract for that exact target kind.

It does **not** mean the target is malformed, absent globally, invalid, corrupt, untrusted, irrelevant, or forbidden.

### Invalid containing occurrence

Fail closed if:

- the containing ref is noncanonical;
- the containing value does not reproduce that exact ref;
- the containing kind/version is outside the typed Decision 020 surface;
- the declaration key is absent;
- the selected declaration is not `exact_axm_object`;
- the target ref is noncanonical.

No fallback to another declaration or source class is allowed.

## Canonical integration evidence

Lane 02 first produced a green baseline, after which Lane 03 demonstrated ADV-057-A: an existing regular bundled schema containing invalid UTF-8 leaked raw `UnicodeDecodeError` instead of the dedicated capability-context failure. That red result remains valid for its exact pre-repair candidate.

Lane 02 then repaired only that demonstrated failure-normalization boundary. Exact repaired test-bearing head:

`b4aeafc236d4abb426bbd0bd78ca4780675fabab`

Exact fresh-main PR merge candidate:

`a78ff60a4dd2721e24ab0eedd6b3f9e8f7ff896b`

Native run/job:

`34832341654` / `103938318383`

Observed results:

- preserved Decision 020 ADV-054/055: **6/6 passed**;
- unchanged Decision 022 ADV-057-A through F: **6/6 passed**;
- full deterministic discovery: **437/437 passed, 0 failures, 0 errors** in 383.638s;
- explicit enumerated `py_compile`: **passed**;
- complete job: **success**.

Lane 03 independently reran the byte-identical ADV-057 oracle (blob `d5a855e9883d1ed42df39379f3ab8b34126477be`) against the repaired head. Exact Lane 03 test head:

`9a881a433b1973a893b6d8501cd39b93c79de4b9`

Exact native merge candidate:

`4c709c088eaa1babcbcaad17ed4daf32120f22b4`

Native run/job:

`34833589216` / `103942279133`

Observed results:

- Decision 020 ADV-054/055: **6/6 passed**;
- unchanged ADV-057-A through F: **6/6 passed**;
- full deterministic discovery: **437/437 passed, 0 failures, 0 errors** in 298.555s;
- explicit enumerated `py_compile`: **passed**;
- complete job: **success**.

Lane 01 then squash-merged Lane 02 PR #101 as canonical commit:

`ae2a4171dac0c6bb56b86ac11fc4b987924b4a94`

The historical red run is preserved as evidence rather than rewritten by the later repair and green recheck.

## Regression obligations retained

The canonical Decision 022 regression surface includes the previously required cases:

1. artifact v0.4 occurrence targeting a supported bundled kind;
2. evidence-record v0.2 occurrence targeting a supported bundled kind;
3. canonical unsupported future kind returning `unsupported_kind` while declaration syntax remains valid;
4. equal target refs under different declaration occurrences remain separately attributable;
5. equal declaration keys under different exact containing objects remain separate occurrences;
6. later same-logical-id containers cannot rebind an earlier exact occurrence;
7. declaration-map order cannot alter result meaning;
8. non-exact source classes cannot be promoted by lexical appearance;
9. target object path presence/absence is not an input to runtime-capability standing;
10. named transport/materialization preserves meaning or fails closed;
11. capability facts expose no existence/retrieval/integrity/trust/closure/acceptance authority;
12. unsupported kind remains distinct from malformed declaration and source absence;
13. invalid bundled schema context fails closed rather than becoming `unsupported_kind`;
14. existing invalid-UTF-8 bundled schema fails through the dedicated context-error boundary;
15. explicit compile succeeds.

## Explicit non-goals

Decision 022 does **not** authorize:

- reading the declared target object's content-addressed path;
- `FilesystemObjectStore.load()` / `load_bytes()` against the source target;
- target availability/existence observation;
- source byte retrieval or retention;
- content-address digest recomputation;
- locator or network/filesystem/package resolution;
- source declaration association;
- historical source migration;
- provenance-relation vocabulary;
- source trust/quality/relevance/completeness/closure;
- dependency/evidence closure;
- packet acceptance, claim closure, successor publication;
- Stage 5 integration;
- epochs/barriers or replay claims.

## Why this boundary remains useful

Decision 021 cannot safely classify exact target availability until runtime capability is separate from store state. Decision 022 isolates that precondition with no source-target I/O and no mutable store-root replay claim. The remaining observation-context/re-execution question therefore returns to Decision 021 rather than being silently answered by this implementation.

## Root grounding

- **Truth:** unsupported runtime interpretation remains distinct from malformed declaration, missing target, corrupt target, and trust judgment; the pre-repair red evidence remains preserved.
- **Agency / non-domination:** bundled contract presence is a runtime capability fact, not source authority; no actor/host/branch/CI/Git status gains power.
- **Continuity:** each capability fact remains attached to the exact authored declaration occurrence, and the exact repair/recheck evidence is durable outside private chat.
- **Wisdom before speed:** canonicalize only the capability precursor and keep target availability, generic resolution, integrity execution, trust, closure, Stage 5, epochs, and replay outside this decision.

## Lane ownership after integration

Decision 022 implementation is canonical and Lane 02 should preserve its regression surface.

Lane 01 returns to Decision 021 research and must ground the observation-context / re-execution boundary before opening a later numbered target-observation implementation decision.

Lane 03 should retain ADV-057 as regression evidence and attack only the next bounded decision once it is opened durably.
