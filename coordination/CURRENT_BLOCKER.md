# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Canonical implementation integrated before this Lane 01 coordination branch: **PR #90 / `8c6e4c9d8d84ac1e364ff76d23aa1fadf9325d90`**
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current bounded gate: **Decision 021 — Source Observation Boundary Research**
Current disposition: **Decision 020 is canonical on its bounded typed source-declaration contract surface. The demonstrated ADV-054 declaration-key and ADV-055 content-digest true-end holds are cleared on the tested Python/jsonschema surface after preserved red → narrow repair → independent green evidence. Do not jump to a generic resolver. Decision 021 is research-only and must separate source identity, availability/existence observation, retrieval, content integrity, declaration association, provenance relation, trust/relevance, completeness/closure, and institutional acceptance before any next implementation gate opens.**

`coordination/CURRENT_WAVE.md` is historical chronology. This file is the current-state overlay and must be read with Decisions 020/021, newest commits/PRs/branches, and durable Lane 01/02/03 return packets.

## Decision 020 canonical boundary

Decision 020 now canonically provides a versioned typed source-declaration contract for new artifact/evidence versions while preserving all historical `source_refs[]` values at their authored opaque strength.

The integrated surface establishes exactly four explicit declaration target classes:

- `opaque_label`;
- `exact_axm_object`;
- `content_address`;
- `locator`.

Declaration occurrence identity remains `exact containing object identity + declaration key`. Order, lexical shape, recency, actor identity, schedule position, CI state, branch ownership, and Git permission carry no declaration identity, pairing, priority, trust, or selection authority.

The bounded truth claim remains narrow:

- `exact_axm_object` proves only authored canonical exact-reference syntax; it does not exact-load the target;
- `content_address` proves only an authored `sha256` + exactly 64 lowercase hex + `raw_bytes` identity declaration; it does not retrieve bytes or verify integrity;
- `locator` proves only authored addressing context/value; it defines no resolver;
- `opaque_label` remains unresolved target identity beyond its authored token;
- no declaration occurrence is implicitly associated with another declaration.

A valid typed declaration does **not** prove target existence, retrievability, integrity, causal provenance, trust, relevance, completeness, closure, packet acceptance, integration, epoch completion, or replay correctness.

The original Decision 020 contract remains preserved unchanged as pre-implementation decision history. `coordination/decisions/020_INTEGRATION_DISPOSITION.md` records the canonical integration disposition and evidence chain without rewriting the original decision's historical status line.

## Preserved Decision 020 evidence chain

Do not erase or reinterpret the following sequence:

1. Lane 02 implemented the initial typed-source contract and recorded a green baseline before adversarial review.
2. Lane 03 ADV-054-A reproduced a real declaration-key false-end ambiguity caused by `$` accepting a final LF on the demonstrated Python/jsonschema path.
3. Lane 02 repaired only that declaration-key true-end spelling boundary.
4. Lane 03 independently reran the unchanged ADV-054 oracle and cleared that exact repaired surface.
5. Lane 01 PR #94 reproduced ADV-055-A: the same false-end class on `content_address.digest`; its focused adversarial step failed and later full-suite/compile steps were correctly skipped.
6. Lane 02 repaired only the digest true-end spelling boundary on exact test-bearing head `d1d6d1bd878472d3347b8af662d576d492831079`.
7. Exact repaired PR #90 merge candidate `7fa4f34245a845d4700c6c9fad34bc537422aefe` directly recorded unchanged ADV-054-A..E + ADV-055-A **6/6 passed**, full suite **416/416 passed**, and explicit compile success on Python 3.12.14/jsonschema 4.26.0; run/job `34817333803` / `103890717548`.
8. Lane 03 independently reran the unchanged oracle on exact test-bearing head `076265cb57cc0106e6849715a7291607356c4666`. Merge candidate `daa53d1be7c5822fe48c9719832592711e086a71` directly recorded **6/6 passed**, full suite **416/416 passed**, and explicit compile success; run/job `34818561988` / `103894586827`.
9. PR #90 was then squash-merged as `8c6e4c9d8d84ac1e364ff76d23aa1fadf9325d90`.

The historical red revisions remain evidence about prior exact surfaces even though the repaired candidate is now canonical.

Lane 03 Activation 046 is reapplied as coordination/evidence only on fresh canonical ancestry; its stacked pre-squash branch must not be merged as duplicate production history.

## Decision 021 — current research gate

The next gap is not “build a resolver.” The next gap is to define what the institution may truthfully say after it has an authored typed source declaration.

Decision 021 must keep these dimensions separate:

1. declared target identity;
2. target existence / availability observation;
3. retrieval observation;
4. content integrity observation;
5. explicit declaration association;
6. provenance relation;
7. quality / trust / relevance;
8. completeness / closure;
9. institutional acceptance.

The leading candidate for the smallest later executable slice is a read-only `exact_axm_object` observation projection using existing deterministic exact-reference/store primitives, anchored by exact containing-object identity + declaration key. That candidate is **not authorized for implementation yet**. Lane 01 must first finish Decision 021 research and open a later numbered implementation decision if grounded.

## Active lane boundaries

### Lane 01 — active research / sequencing owner

Research Decision 021 only. Inventory existing exact-load/store primitives and determine the smallest universal observation-result contract that makes missing/corrupt/unavailable states explicit without laundering load success into trust, provenance causality, closure, acceptance, Stage 5 integration, epochs, or replay.

A durable research return packet must state the proposed observation facts, exact input/context identity needed for replay, rejected shortcuts, offline boundary, and Lane 03 adversarial surface before any implementation decision opens.

### Lane 02 — hold implementation

Decision 020 implementation is integrated. Do **not** implement a resolver, source loader, digest verifier, association mechanism, migration layer, trust/quality scoring, closure rule, or Decision 021 candidate until Lane 01 opens a later numbered implementation decision.

### Lane 03 — adversarial standby

Decision 020 lexical hold is cleared only on the demonstrated tested surface. Preserve the historical red evidence. For Decision 021, challenge proposed designs for hidden fallback authority, missing/corrupt observation disappearance, implicit source association, mutable locator state, transport/materialization drift, and observation→trust/closure/acceptance laundering. Do not invent resolver policy before Lane 01 opens it.

## Still explicitly unresolved

- source target observation/loading/resolver semantics;
- source bytes retention and retrieval;
- integrity-check execution and retained integrity evidence;
- explicit association between locator/content/exact declarations;
- migration objects mapping exact historical declaration occurrences to future typed declarations;
- general provenance-relation vocabulary;
- source quality/trust/relevance;
- source completeness/closure;
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
- cross-language graph/reachability/frontier/source transport and reproduction;
- exact self/mutual-cycle authorability through ordinary content-addressed publication;
- stronger filesystem durability/concurrency evidence;
- hostile same-process code isolation beyond the trusted deterministic runtime boundary.

## Four-root gate

- **Truth:** declaration validity, source observation, retrieval, integrity, provenance relation, trust, closure, and acceptance remain separate facts. Preserve red and green historical evidence together.
- **Agency / non-domination:** no founder, lane, resolver host, actor category, CI state, branch, schedule position, recency, or Git permission becomes source or merge authority.
- **Continuity:** a replacement occupant must recover what was declared, what was actually observed, against what exact context/state, and what remained unknown without private chat or runtime-specific assumptions.
- **Wisdom before speed:** research and bound source observation before generic resolvers, network/filesystem access, digest verification, implicit associations, trust scoring, closure, model-heavy provenance reasoning, or Stage 5 integration.
