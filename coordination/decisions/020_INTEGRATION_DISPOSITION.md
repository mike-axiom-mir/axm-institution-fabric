# Decision 020 — Canonical Integration Disposition

Date: 2026-09-14
Status: **canonical on the bounded typed source-declaration contract surface through PR #90 / `8c6e4c9d8d84ac1e364ff76d23aa1fadf9325d90`.**

This file is an integration disposition for `020_TYPED_SOURCE_DECLARATION_CONTRACT.md`. The original decision remains the durable pre-implementation contract and is not rewritten to erase the red/repair history.

## Canonical bounded claim

Decision 020 now canonically establishes only a versioned typed source-declaration contract for new artifact/evidence versions while preserving all historical `source_refs[]` strings at their authored opaque strength.

The integrated contract provides exactly four explicit declaration target classes:

- `opaque_label`;
- `exact_axm_object`;
- `content_address`;
- `locator`.

Declaration occurrence identity remains `exact containing object identity + declaration key`; map order, lexical order, recency, actor identity, schedule position, CI state, branch ownership, and Git permission carry no declaration association or selection authority.

`exact_axm_object` uses the shared Stage 2 immutable-reference parser for syntax only and does not exact-load the target. `content_address` is bounded to `sha256`, exactly 64 lowercase hexadecimal characters, and `raw_bytes`. `locator` remains authored address context/value only. The contract defines no implicit association between declaration occurrences.

A valid typed declaration proves only that the containing object authored one target identity fact in one explicit class. It does not prove existence, retrievability, successful resolution, content integrity, causal provenance, trust, relevance, completeness, closure, packet acceptance, integration, epoch completion, or replay correctness.

## Evidence chain preserved

The integration decision relies on the complete red → narrow repair → independent green chain rather than on green CI alone.

### Baseline implementation

Lane 02 PR #90 implemented the Decision 020 surface with historical compatibility guards and deterministic fixtures/tests. An earlier exact implementation candidate recorded 410/410 tests plus explicit compile before adversarial review.

### ADV-054 — declaration-key true-end ambiguity

Lane 03 reproduced a real failure where the original declaration-key JSON-Schema `$` ending admitted a final LF on the demonstrated Python/jsonschema path. That red evidence remains historical truth.

Lane 02 repaired only the declaration-key true-end spelling boundary. Lane 03 independently reran the unchanged ADV-054 oracle and cleared that exact hold. The earlier red result is not invalidated.

### ADV-055 — content-address digest true-end ambiguity

Lane 01 then reproduced the same false-end class for `content_address.digest`: `^[0-9a-f]{64}$` admitted 64 lowercase hex characters plus a final LF on the demonstrated Python/jsonschema path. PR #94 preserves that red counterexample; its focused adversarial step failed and its later full-suite/compile steps were correctly skipped.

Lane 02 exact repaired test-bearing head:

`d1d6d1bd878472d3347b8af662d576d492831079`

The repair changed only the digest true-end spelling boundary to the repository's existing true-end convention and carried ADV-055-A unchanged.

Exact PR #90 repaired merge candidate against then-canonical main:

`7fa4f34245a845d4700c6c9fad34bc537422aefe`

Direct native evidence:

- Python 3.12.14 / jsonschema 4.26.0;
- unchanged ADV-054-A through E + ADV-055-A: **6/6 passed**;
- full deterministic suite: **416/416 passed**;
- explicit compile: **passed**;
- workflow run/job: `34817333803` / `103890717548`;
- complete job: **success**.

Lane 03 then independently rechecked the repaired surface without changing the production schema or adversarial oracle.

Exact Lane 03 test-bearing head:

`076265cb57cc0106e6849715a7291607356c4666`

Exact independent merge candidate:

`daa53d1be7c5822fe48c9719832592711e086a71`

Direct native evidence:

- Python 3.12.14 / jsonschema 4.26.0;
- unchanged ADV-054-A through E + ADV-055-A: **6/6 passed**;
- full deterministic suite: **416/416 passed**;
- explicit compile: **passed**;
- workflow run/job: `34818561988` / `103894586827`;
- complete job: **success**.

Lane 03's durable Activation 046 return packet is integrated separately on fresh canonical ancestry so its evidence is preserved without replaying Lane 02's pre-squash production history.

## Merge reasoning under the four roots

### Truth

The canonical result preserves both failures and both repairs. The green 416/416 runs prove only the repaired tested Decision 020 surface; they do not erase the earlier red revisions and do not prove later source semantics.

### Agency / non-domination

Mike/founder status, lane identity, schedule order, confidence, green CI, mergeability, branch ownership, and Git permission are not constitutional authority. Integration is justified only by the grounded bounded contract and evidence against the four roots.

### Continuity

Historical source strings retain their original opaque meaning; typed declaration occurrence identity is explicit and order-free; the two demonstrated false-end ambiguities are now executable regressions; and the red/repair/independent-green chain is durable repository evidence rather than private chat state.

### Wisdom before speed

Decision 020 stops at authored typed target identity facts. No resolver, loader, integrity executor, implicit association, migration mechanism, trust/quality/closure policy, packet acceptance, Stage 5 integration, epoch, or replay behavior is pulled forward.

## Still unresolved

Decision 020 does not settle:

- source target observation/loading/resolver semantics;
- byte retention/retrieval;
- digest recomputation and retained integrity evidence;
- locator/content/exact association;
- historical-to-typed migration objects;
- general provenance-relation vocabulary;
- source quality/trust/relevance/completeness/closure;
- dependency admissibility/satisfaction/closure;
- evidence precedence/invalidation/closure;
- multiple-required-state semantics;
- logical lineage / `supersedes_ref` validity;
- global occupancy/claim currentness and authorization;
- multiple-packet selection/acceptance;
- claim closure and successor revision publication;
- Stage 5 integration receipts/runtime;
- epochs/barriers and replay;
- cross-language source reproduction;
- stronger filesystem durability/concurrency;
- hostile same-process isolation;
- exact self/mutual-cycle authorability through ordinary content-addressed publication.

## Next sequencing

Do not jump directly from typed declarations to a generic resolver. The next open work is Decision 021 research: separate source observation, retrieval, integrity verification, association, trust, and closure into explicit truth dimensions and identify the smallest deterministic offline-capable next implementation without granting locators, digests, ordering, actors, or runtime success hidden authority.
