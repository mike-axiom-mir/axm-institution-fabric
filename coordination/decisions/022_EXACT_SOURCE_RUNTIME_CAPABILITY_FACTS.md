# Decision 022 — Exact Source Runtime Capability Facts

Date: 2026-09-14
Status: **implementation open; bounded precursor to exact source observation only.**

Decision 021 research established that the current exact store can surface target-path outcomes before it has established whether the runtime supports the target kind. A direct target-availability observer would therefore risk collapsing runtime capability with source absence/corruption.

Decision 022 opens the smallest deterministic precursor that removes that ambiguity without reading a source target path.

## Bounded objective

For one Decision 020 `exact_axm_object` declaration occurrence in an exact typed containing object, project a deterministic **kernel-bundled runtime capability fact**:

- preserve the exact containing-object identity;
- preserve the exact declaration key;
- preserve the exact authored target `object_ref`;
- preserve the parsed target kind;
- state only whether the **bundled AXM kernel contract set in this runtime** supports interpreting that kind.

This projection must perform **no exact target object lookup** and must not become a source resolver.

## First-slice input boundary

The first implementation may consume only:

1. an exact containing-object ref for a typed artifact v0.4 or evidence-record v0.2;
2. the corresponding validated containing-object value;
3. one declaration key that exists in that exact value and whose `source_class` is `exact_axm_object`.

The implementation must verify that the supplied containing value reproduces the supplied exact immutable reference. It must extract the declaration by exact key from that exact containing value. Logical-id lookup, newest-version lookup, `supersedes_ref`, array/map order, recency, actor, lane, branch, CI, or Git state may not substitute another containing object or declaration occurrence.

The target `object_ref` must be consumed unchanged through the existing Stage 2 exact-reference parser.

## Runtime capability context — deliberately narrow

V0 Decision 022 covers the repository/package **bundled kernel schema context only**.

A target kind is `supported` only when its inferred bundled `<kind>.schema.json` contract exists and is a valid bundled kernel schema under the existing schema loader.

A canonical target kind with no bundled schema is `unsupported_kind`.

A bundled schema file that exists but cannot itself be read/validated is a **kernel/runtime configuration failure**, not an `unsupported_kind` result and not a source corruption result. The projection should fail closed with a dedicated/explicit capability-context error rather than laundering that condition into source standing.

Custom/mutable `schema_dir` contexts are outside this first slice. They require an explicit context-identity decision later and must not silently enter through a hidden parameter or ambient filesystem fallback.

## Minimum result semantics

The implementation result must preserve named semantics equivalent to:

- `containing_object_ref`
- `declaration_key`
- `target_object_ref`
- `target_kind`
- `runtime_capability` = `supported` | `unsupported_kind`

Exact physical class/record naming is Lane 02's implementation choice, but transport/materialization must not turn these named facts into position-dependent meaning.

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

## Required tests/evidence

Lane 02 should add deterministic tests for at least:

1. artifact v0.4 occurrence targeting a supported bundled kind;
2. evidence-record v0.2 occurrence targeting a supported bundled kind;
3. the PR #98 canonical `future-source-kind.unregistered` case returning `unsupported_kind` while the declaration itself remains valid;
4. same target ref under two different declaration occurrences remains two attributable results;
5. same declaration key under two different exact containing objects remains two occurrences;
6. later same-logical-id container cannot rebind an earlier exact occurrence;
7. declaration-map order cannot alter the result;
8. non-exact source classes cannot be promoted by lexical appearance;
9. no target object path is required to produce either capability result;
10. result transport/materialization either preserves named semantics or fails closed;
11. the result exposes no existence/retrieval/integrity/trust/closure/acceptance authority;
12. all prior source/dependency/lifecycle tests remain green;
13. explicit compile succeeds.

## Lane 03 attack surface

After Lane 02 publishes an exact tested head, Lane 03 should attack unchanged semantics for:

- target-path presence/absence accidentally changing capability standing;
- unsupported kind collapsing into malformed declaration or source absence;
- same-target occurrence collapse through caching;
- stale containing-object rebinding by logical id, version, recency, or `supersedes_ref`;
- declaration order/key-similarity authority;
- non-exact source-class promotion;
- custom schema-directory or ambient filesystem injection;
- invalid bundled schema becoming `unsupported_kind` or source corruption;
- named-result transport drift;
- capability success becoming existence, retrieval, integrity, provenance, trust, closure, packet acceptance, Stage 5 integration, epoch, or replay authority.

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

## Why this is the next smallest step

Decision 021 cannot safely classify exact target availability until runtime capability is separated from store state. Decision 022 isolates that precondition with no source-target I/O and no mutable store-root replay claim. It is therefore smaller than an observer, directly addresses ADV-056-B/F/G/L, and gives Lane 03 an executable semantic boundary before the institution opens live source observation.

## Root grounding

- **Truth:** unsupported runtime interpretation remains distinct from malformed declaration, missing target, corrupt target, and trust judgment.
- **Agency / non-domination:** bundled contract presence is a runtime capability fact, not source authority; no actor/host/branch/CI/Git status gains power.
- **Continuity:** each capability fact remains attached to the exact authored declaration occurrence, so equal targets and later container versions cannot erase provenance of what was checked.
- **Wisdom before speed:** establish capability standing without target I/O before attempting exact source availability, generic resolution, integrity execution, trust, closure, or replay.

## Lane ownership

**Lane 02 owns the first implementation of Decision 022.**

Lane 03 attacks the exact tested implementation head afterward.

Lane 01 should not open target availability/retrieval observation until Decision 022 survives adversarial review and the remaining Decision 021 observation-context/re-execution boundary is revisited explicitly.
