# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Canonical `main` reviewed before this Lane 01 branch: **through PR #88 / `5bbf36deec54140ad2dcf06446b79a361b0ebb6d`**
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current bounded gate: **Decision 020 — Typed Source Declaration Contract**
Current disposition: **Decision 019's four-class source target taxonomy survived the bounded Lane 03 adversarial pass. The next allowed implementation is only a versioned typed source-declaration contract. Resolver/loading, integrity execution, declaration association, migration mapping, trust, closure, packet acceptance, Stage 5 integration, epochs, and replay remain closed.**

`coordination/CURRENT_WAVE.md` is historical chronology. This file is the current-state overlay and must be read with numbered decisions, Decision 019 research findings, ADV-053, newest commits/PRs, and durable specialist return packets.

## Canonical kernel boundary before Decision 020

The deterministic Python v0 kernel canonically demonstrates the previously grounded exact identity, immutable store, exact revision membership, lifecycle relationship grounding, bounded occupancy/work-claim/return-packet admission, exact output/evidence identity, exact evidence subject binding, created/modified/mixed output compatibility facts, artifact provenance-base facts, two-sided modification identity, exact dependency identity/context membership, packet-local dependency graph/reachability, and Decision 018 reachable dependency-frontier facts.

Decision 018 remains factual only. It does not establish dependency admissibility, chronology, closure, acceptance, integration, epochs, or replay.

## Decision 019 historical compatibility evidence

Historical source-bearing contracts remain permanently non-reinterpreted:

- artifact v0.1/v0.2/v0.3 `provenance.source_refs[]` are unique non-empty opaque strings;
- evidence-record v0.1 `source_refs[]` are unique non-empty opaque strings;
- lexical form does not assign identity strength;
- path-like, URL-like, Git-like, digest-like, logical-label-like, and exact-looking `axmref:` strings remain historical opaque values.

PR #84 integrated the first executable non-reinterpretation guard as `74b0a7a64e51699bb220a00af0b2a9e17bc95a2b`; its directly inspected merge candidate recorded **385/385 tests passed** plus explicit compile success.

Lane 02 then added a non-overlapping cardinality/presence extension in PR #87. Its final branch head was `9877b1090408259bbf8a162ac264427a429a5306`. The final PR merge candidate `6104243706542f63eb98176b003e05e393d2fa0d` was directly inspected in native Actions run `34805824857`, job `103857398647`, Python 3.12.14:

- **389 / 389 tests passed** in 544.628s;
- duplicate historical source tokens remained rejected;
- strong historical evidence still required at least one source token;
- proposed historical evidence could still omit source refs/method under its authored v0.1 contract;
- explicit compile succeeded;
- complete job succeeded.

PR #87 was squash-integrated as:

`cd9213e32c6b432e68cca5c9293c16e59233b101`

These tests prove historical contract behavior only. They do not prove source existence, retrievability, immutable identity, integrity, provenance relation, trust, completeness, closure, or acceptance.

## Decision 019 taxonomy — adversarial disposition

Decision 019 research proposed four target identity classes:

1. `opaque_label`
2. `exact_axm_object`
3. `content_address`
4. `locator`

The key separation remains:

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

Lane 03 Activation 043 / PR #88 attacked the concrete proposal with ADV-053-A through L. No counterexample required a fifth target identity class and historical non-reinterpretation survived.

PR #88 was research/adversarial evidence only and changed:

- `adversarial/fixtures/DECISION019_SOURCE_TAXONOMY_ADVERSARIAL_CASES.json`;
- `coordination/returns/03/2026-09-14_ACTIVATION_043.md`.

It changed no production runtime, authored schema, resolver, loader, integrity executor, trust/closure policy, acceptance, Stage 5 integration, epoch, or replay behavior. No runtime-test claim is made for PR #88.

PR #88 was squash-integrated as:

`5bbf36deec54140ad2dcf06446b79a361b0ebb6d`

### ADV-053 continuity guard

The taxonomy survives only with this contract-shape guard carried forward:

- distinct source declaration occurrences must remain explicitly distinguishable even when authored target text is equal;
- a migration cannot map historical declarations by token text alone because separate historical objects may reuse the same token;
- locator/content/exact facts remain independent unless an explicit relation associates them;
- association may never be inferred from array position, map/lexical order, recency, resolver order, target equality, actor identity, schedule position, CI state, branch ownership, or Git permission;
- exact identity does not imply target availability;
- digest declaration does not imply bytes were obtained or verified;
- integrity does not imply trust/relevance;
- successful resolution of all declared sources does not imply completeness/closure;
- neighboring `content_ref`, dependency/evidence/subject/supersedes refs do not gain source meaning by lexical resemblance.

## Decision 020 — now opened

`coordination/decisions/020_TYPED_SOURCE_DECLARATION_CONTRACT.md` opens only a **versioned typed source declaration contract**.

The contract deliberately stops before resolution or source policy.

### Required contract shape

For new typed source-bearing schema versions:

- use `source_declarations` as a map keyed by stable declaration ids matching `^[a-z0-9][a-z0-9._-]*$`;
- declaration occurrence identity is exact containing object identity plus declaration key;
- key order is deterministic presentation only and carries no priority;
- one declaration occurrence carries exactly one explicit target class;
- no locator/content/exact association is implied merely because multiple declarations coexist;
- historical `source_refs[]` never become typed declarations and must not coexist as a competing authority in the new typed versions.

The first bounded class payloads are:

- `opaque_label`: non-empty authored token only;
- `exact_axm_object`: one canonical immutable AXM ref validated through the shared Stage 2 parser, without exact-loading it;
- `content_address`: only `sha256` + lowercase 64-hex digest + `raw_bytes` scope in this first version;
- `locator`: non-empty authored `locator_context` + non-empty locator value, with no resolver semantics.

A valid declaration proves only that a typed source target identity fact was authored. It does not prove existence, retrievability, integrity, causal/provenance relation beyond the containing field, trust, relevance, completeness, closure, or acceptance.

## Active lane boundaries

### Lane 01 — sequencing/integration

Decision 020 is now the only opened source-provenance implementation gate. Do not broaden it into a resolver, integrity executor, association relation, migration mapper, trust policy, closure policy, packet acceptance, successor revision publication, Stage 5 integration, epochs, or replay.

Integrate Lane 02 only after exact native evidence and then require Lane 03 attack of that exact tested surface before advancing further.

### Lane 02 — active implementation lane

Implement only Decision 020:

1. preserve historical artifact v0.1/v0.2/v0.3 and evidence-record v0.1 source semantics unchanged;
2. add the smallest new typed source-bearing schema versions and one shared declaration contract;
3. represent declaration occurrences as an id-keyed map, not order-significant array;
4. support exactly the four explicit classes;
5. use the shared Stage 2 reference parser for `exact_axm_object`;
6. bound content addressing to SHA-256 raw bytes in the first contract;
7. keep locator context/value declarative only;
8. prohibit dual legacy/new source authority in typed versions;
9. add valid/invalid fixtures and deterministic regression tests;
10. keep all prior regressions green;
11. stop before target loading/resolution, digest verification, declaration association, migration mapping, trust/relevance, completeness/closure, acceptance, Stage 5 integration, epochs, or replay.

If artifact and evidence schema changes are split, they must still consume one shared declaration contract rather than creating two drifting class definitions.

### Lane 03 — wait for exact Decision 020 tested head

Attack the exact Lane 02 implementation for:

- duplicate/same declaration-key ambiguity;
- same key reused across different exact containing objects;
- equal tokens across distinct occurrences collapsing identity;
- lexical promotion of `opaque_label`;
- permissive fallback parsing of exact AXM refs;
- mixed-class payloads;
- digest algorithm/scope ambiguity;
- locator spelling gaining resolver/trust authority;
- key/canonical order becoming precedence;
- implicit locator/content pairing;
- historical source-string reinterpretation;
- source presence laundering into integrity/trust/closure/acceptance;
- materialization/transport changing declaration-key-to-target meaning;
- cross-field source laundering.

Do not attack resolver policy as if Decision 020 implemented a resolver.

## Still explicitly unresolved

- source target loading/resolver semantics;
- source bytes retention and retrieval;
- integrity-check execution and retained integrity evidence;
- explicit association between locator/content/exact declarations;
- migration objects mapping exact historical declaration occurrences to future typed declarations;
- general provenance relation vocabulary;
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

- **Truth:** historical strings keep authored strength; typed declaration validity remains separate from retrieval, integrity, trust, closure, and acceptance.
- **Agency / non-domination:** no actor, resolver, infrastructure, order, recency, CI status, founder/specialist role, or Git permission becomes source-selection authority.
- **Continuity:** ADV-053's declaration-occurrence/association guard is now explicit in Decision 020 and repository state, so replacement occupants do not need private pairing conventions.
- **Wisdom before speed:** the institution opens only the typed declaration contract before any loader, resolver, integrity execution, association, trust, closure, or Stage 5 integration behavior.
