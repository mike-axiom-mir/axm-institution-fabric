# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Canonical `main` reviewed during this activation: **through PR #85 / `eebc79343018ce26fefc1664662a5528ecd5f865`**
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current bounded gate: **Decision 019 — concrete source-provenance taxonomy proposal under adversarial review**
Current disposition: **Decision 018 remains canonical. Decision 019 research has now produced a concrete four-class source identity taxonomy. Source runtime/schema implementation remains closed until Lane 03 attacks the proposal and Lane 01 records the disposition.**

`coordination/CURRENT_WAVE.md` remains historical chronology. This file is the current-state overlay and must be read with numbered decisions, Decision 019 research findings, newest canonical commits/PRs, and durable specialist return packets.

## What is now canonical before the new research proposal

The bounded deterministic Python v0 kernel canonically demonstrates the previously grounded exact identity, immutable-store, lifecycle, packet, evidence-subject, compatibility, provenance-base, modification, mixed-output, dependency-identity, dependency-context-membership, same-packet graph, packet-local reachability, and Decision 018 exact reachable dependency-frontier facts.

Decision 018 remains bounded to factual dependency-frontier reconstruction. It does not establish dependency policy, chronology, closure, acceptance, integration, epochs, or replay.

## Decision 019 historical non-reinterpretation guard — PR #84

Lane 02 stayed inside the research hold and added only executable compatibility evidence for the already-authored historical boundary.

PR #84 final head:

`35b6d5f3f05b457b5d3a0aea07628e54ea073d17`

Final pull-request merge candidate directly observed in native Actions:

`b8daa47109ea53476d922f978366b1e404143916`

Native run `34802748404`, job `103848542521`, directly recorded:

- Python 3.12.14;
- **385 / 385 tests passed** in 399.470s;
- all six `HistoricalSourceRefCompatibilityTests` passed;
- explicit compile including `tests/test_source_ref_historical_compatibility.py` succeeded;
- complete job succeeded.

PR #84 was squash-integrated as:

`74b0a7a64e51699bb220a00af0b2a9e17bc95a2b`

The tests establish only this historical syntax boundary:

- artifact v0.1/v0.2/v0.3 `provenance.source_refs[]` remain unique non-empty opaque strings;
- evidence-record v0.1 `source_refs[]` remain unique non-empty opaque strings;
- path-like, URL-like, Git-like, hash-like, logical-label-like, and exact-looking `axmref:` strings are still accepted by those historical fields;
- empty strings remain rejected;
- no `pattern`, `format`, `enum`, or `const` silently upgrades historical source identity strength.

This does **not** prove source existence, retrievability, integrity, trust, completeness, closure, or authority.

## Lane 03 research-hold continuity — PR #85

Lane 03 Activation 042 added one coordination/evidence return packet only. It did not add source runtime/schema/test semantics. It independently reconstructed the Decision 019 hold, checked replacement-occupant recovery and the stale-`CURRENT_WAVE` trap, reviewed PR #84 for boundary drift, and recorded the same bounded native evidence.

PR #85 was squash-integrated as:

`eebc79343018ce26fefc1664662a5528ecd5f865`

Its historical observation that no concrete taxonomy existed at its activation time remains truthful. The new Lane 01 research finding below is the next state transition, not a rewrite of Lane 03's packet.

## Decision 019 concrete research proposal

Lane 01 has now published:

`coordination/decisions/019_SOURCE_PROVENANCE_TAXONOMY_RESEARCH_FINDINGS.md`

The proposed minimal universal taxonomy has four source identity classes:

1. **`opaque_label`** — an authored source token with unresolved identity strength. All historical source strings remain here permanently, regardless of lexical shape.
2. **`exact_axm_object`** — one explicitly typed canonical immutable AXM object reference. Syntax does not imply target existence; exact-load and digest reproduction remain separate evidence.
3. **`content_address`** — immutable non-AXM bytes/content identified by explicit digest algorithm plus digest over a defined byte scope. Retrieval remains separate from identity; matching bytes establish integrity only, not trust.
4. **`locator`** — a path/URI/repository/service address. Resolution is time/context-specific and does not establish immutable content identity or trust.

The research intentionally reduces other candidates:

- repository/file snapshot = immutable content/object identity plus optional locator/context, not a fifth universal class;
- external/network source = locator unless immutable identity is separately recorded;
- human/machine/tool assertion = provenance/responsibility around a declaration, not a source target identity class.

## Orthogonal truth dimensions

The proposal preserves this boundary:

```text
source identity declared
    != target exists
    != target retrievable now
    != retrieved bytes reproduce immutable identity
    != provenance relation to subject is proven
    != source is trustworthy / high quality / relevant
    != declared source set is complete / closed
    != evidence or packet is accepted
```

No future resolver should collapse these into one success boolean.

## Historical migration boundary

Until a later numbered decision changes only future schema versions:

- artifact v0.1/v0.2/v0.3 historical `source_refs[]` remain `opaque_label` semantics forever;
- evidence-record v0.1 historical `source_refs[]` remain `opaque_label` semantics forever;
- exact-looking `axmref`, URL, path, Git id, digest, package id, or logical id syntax never upgrades an old value;
- a future typed source surface must use a new schema version and/or new explicitly typed field;
- migration may create a new immutable declaration linking an old opaque token to a newly grounded typed identity, but cannot rewrite the old object's meaning;
- missing/corrupt targets remain explicit and never fall back to logical id, newest version, resolver availability, array order, actor identity, or Git permission.

## External comparison evidence — informative, not authority

The research compared the proposal with:

- W3C PROV's separation of entities, activities, agents, and provenance relations;
- SLSA v1.2's separation of human-facing URI/location from revision/content digest, including its warning that a source URI is not intended for policy decisions;
- OCI descriptors' separation of content digest from metadata/location concerns.

AXM does not require these standards or internet access at runtime. They support the architectural separation only.

## Active lane boundaries

### Lane 01 — research integration lane

Do **not** implement source semantics yet. Preserve the four-class proposal and review Lane 03's next adversarial return. If the proposal survives, decide whether to open Decision 020 for a typed source-declaration contract only.

### Lane 02 — still held from source implementation

PR #84 is canonical only as historical compatibility evidence. Do not add resolver behavior, schema migration, typed source parsing, source loading, integrity checking, trust, closure, or acceptance until a later numbered decision explicitly opens a bounded step.

### Lane 03 — now active adversarial lane

Attack exactly the concrete Decision 019 proposal, not imagined implementation code. Priority cases:

1. historical exact-looking opaque values gaining identity strength;
2. same locator / different bytes over time;
3. same bytes / different locators;
4. missing or corrupt exact AXM sources;
5. digest syntax without bytes and digest mismatch;
6. mutable branch/HEAD/path/URL resolution;
7. conflicting source declarations;
8. hidden resolver/network/filesystem/repository-host/recency/order authority;
9. integrity being laundered into trust/quality/relevance;
10. identity/retrievability being laundered into completeness/closure/acceptance;
11. cross-field laundering from `content_ref`, dependency/evidence/subject/supersedes refs;
12. offline replacement-occupant reconstruction without private conventions.

No production source runtime is needed for this adversarial pass; it may return research counterexamples/fixtures if they expose a concrete contradiction in the taxonomy.

## Still explicitly unresolved

- whether the four-class taxonomy survives independent adversarial review;
- exact future typed source-declaration shape;
- source target loading/resolver semantics;
- source integrity-check execution and retained evidence;
- provenance relation vocabulary beyond the historical field-scoped declaration;
- source quality/trust/relevance policy;
- source completeness/closure;
- dependency admissibility / allowed-context policy;
- dependency satisfaction;
- actual production chronology / scheduler ordering;
- declaration completeness and dependency closure policy;
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
- supported cross-language graph/reachability/frontier/source transport;
- cross-language reproduction generally;
- exact self/mutual-cycle authorability through ordinary content-addressed publication;
- stronger filesystem durability/concurrency evidence;
- hostile same-process code isolation beyond the trusted deterministic runtime boundary.

## Four-root gate

- **Truth:** historical strings stay at authored strength; the taxonomy explicitly separates identity, retrieval, integrity, relation, trust, and closure.
- **Agency / non-domination:** no actor category, filesystem, network, repository host, resolver, newest version, array order, or Git permission becomes hidden source authority.
- **Continuity:** PR #84 turns non-reinterpretation into executable evidence; PR #85 preserves replacement-occupant recovery; the concrete taxonomy and next attack surface now live in repository state rather than private chat.
- **Wisdom before speed:** implementation remains held for one independent adversarial pass instead of promoting the first plausible taxonomy directly into code.
