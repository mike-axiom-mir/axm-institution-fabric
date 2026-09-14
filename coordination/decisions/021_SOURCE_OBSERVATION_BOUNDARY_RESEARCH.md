# Decision 021 — Source Observation Boundary Research Gate

Date: 2026-09-14
Status: **research open; no source resolver, loader, integrity executor, association rule, trust policy, closure rule, or acceptance behavior is authorized by this decision.**

Decision 020 now gives the institution an explicit typed declaration language for source target identity. It deliberately stops before observing whether a declared target exists, can be retrieved, reproduces declared bytes, or actually bears any stronger provenance meaning.

The next continuity risk is semantic collapse: a later occupant could treat one successful lookup, one valid digest spelling, one nearby locator, or one green runtime event as if it simultaneously proved existence, retrieval, integrity, association, trust, completeness, and acceptance.

Decision 021 is therefore a **research gate**, not an implementation contract.

## Research question

What is the smallest universal, deterministic, offline-capable source observation surface that can follow Decision 020 without conflating distinct truth dimensions or importing domain-specific resolver assumptions into the institutional kernel?

The research must keep at least these dimensions separate:

1. **declared target identity** — already established by Decision 020;
2. **target existence / availability observation** — whether the exact target was observed in a specified bounded context;
3. **retrieval observation** — whether bytes/object data were actually obtained, from what explicit mechanism/context, and at what exact observation input;
4. **content integrity observation** — whether obtained raw bytes reproduce an explicitly declared content address;
5. **declaration association** — whether two source declaration occurrences are explicitly asserted to refer to one observed source relation;
6. **provenance relation** — what relation, if any, is claimed between source and subject;
7. **quality / trust / relevance** — evaluative standing, deliberately separate from identity/integrity;
8. **completeness / closure** — whether all required source facts are present;
9. **institutional acceptance** — downstream policy/lifecycle meaning, deliberately separate from every observation above.

No research conclusion may collapse these dimensions merely because one implementation could compute several of them together.

## Four Decision 020 classes must remain distinct

### `opaque_label`

Research must assume no automatic resolver. A non-empty token is not a path, URL, object ref, package id, digest, or search query unless a later explicit contract says so.

### `exact_axm_object`

The repository already has a deterministic exact immutable-reference parser and object store. Research should determine whether the smallest next executable proof can safely observe exact AXM target loadability/exact-load result **without** turning successful loading into trust, causal provenance, closure, or acceptance.

A key question is whether missing, corrupt, wrong-kind, or otherwise unloadable exact targets should be represented as explicit observation facts or fail the projection itself. Do not choose this by convenience; ground it in continuity/replay needs and existing store semantics.

### `content_address`

A syntactically valid SHA-256 declaration is not integrity evidence. Verification requires actual bytes and a declared byte scope. Decision 020 has no byte provider or association from a digest declaration to any locator/exact-object declaration.

Research must therefore reject any design that recomputes a digest from an implicitly adjacent source occurrence.

### `locator`

A locator is authored addressing context/value only. Research must not create a universal network/filesystem/package resolver by guessing from `locator_context` spelling.

If resolver behavior is ever introduced, resolver identity/version/configuration, offline behavior, mutable-target behavior, and returned observation evidence must be explicit enough for replay or an explicit replay limitation.

## Required research outputs

Before opening an implementation decision, Lane 01 must produce a durable return packet that:

1. inventories the existing exact-load/store primitives relevant to `exact_axm_object` sources;
2. inventories what Decision 020 artifacts/evidence can and cannot currently expose at runtime without reinterpretation;
3. separates observation facts from policy decisions in a proposed minimal result shape;
4. decides whether the first executable slice should cover only `exact_axm_object` declarations or another narrower universal subset;
5. records how missing/corrupt/unavailable targets remain explicit rather than silently disappearing;
6. records what exact containing-object/declaration occurrence identity anchors an observation;
7. records what input state or store context must be named so later replay does not depend on hidden process state;
8. explicitly rejects order/recency/actor/host/CI/Git authority and implicit association;
9. states offline behavior and whether any external resolver is prohibited in the first slice;
10. identifies adversarial cases Lane 03 should attack if an implementation decision is later opened.

## Candidate smallest executable slice — not yet authorized

The leading candidate is a read-only **exact AXM source observation** projection for Decision 020 `exact_axm_object` declarations only:

- anchor each observation to exact containing object identity + declaration key;
- consume the exact authored `object_ref` unchanged;
- use only existing deterministic exact-reference/store primitives;
- expose explicit exact-load standing without logical-id/newest/recency/locator fallback;
- leave `opaque_label`, `content_address`, and `locator` explicitly unobserved by that projection;
- add no trust, provenance-relation, completeness, closure, packet acceptance, Stage 5 integration, epoch, or replay-success implication.

This candidate is recorded so research has a concrete falsifiable target. It is **not** permission for Lane 02 to implement it until Lane 01 finishes the research and opens a numbered implementation decision.

## Explicitly rejected shortcuts

Decision 021 research must reject:

- treating valid `exact_axm_object` syntax as target existence;
- treating successful exact load as trust or provenance causality;
- treating a valid content digest string as verified integrity;
- pairing locator/content/exact declarations by map order, key similarity, equal text, recency, actor, lane, packet, host, CI order, or Git history;
- treating locator context spelling as a resolver registry;
- network access by default in the universal kernel;
- newest-version/logical-id fallback for exact source identity;
- source observation success as completeness, closure, packet acceptance, claim closure, integration, epoch completion, or replay correctness;
- rewriting historical `source_refs[]` strings into typed declarations;
- introducing a model/agent judgment layer before the deterministic observation boundary is grounded.

## Root grounding

- **Truth:** make every transition from authored identity → observation → integrity → evaluation → closure explicit rather than laundering one into the next.
- **Agency / non-domination:** no resolver host, actor category, founder/specialist identity, schedule, CI, Git permission, or recency becomes source authority.
- **Continuity:** a replacement occupant must be able to reconstruct what was declared, what was actually observed, against what exact state/context, and what remained unknown without hidden process memory.
- **Wisdom before speed:** research and bound the observation layer before adding generic resolvers, network/filesystem access, source associations, trust scoring, closure, or model-heavy provenance reasoning.

## Lane ownership

**Lane 01 owns this research gate.**

Lane 02 should not implement a source observation/resolver layer until a later numbered implementation decision is opened.

Lane 03 should remain available to challenge the proposed observation boundary, especially hidden fallback authority, disappearance of missing/corrupt observations, implicit association, mutable locator state, transport/materialization drift, and observation→trust/closure laundering.
