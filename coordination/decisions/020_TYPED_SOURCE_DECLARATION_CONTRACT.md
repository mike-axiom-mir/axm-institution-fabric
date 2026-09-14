# Decision 020 — Typed Source Declaration Contract

Status: **accepted as the next bounded Stage 4 contract step after Decision 019 research and adversarial review, subject to Lane 02 implementation and Lane 03 attack before integration.**

Decision 019 established a four-class source target taxonomy and preserved the permanent non-reinterpretation of historical `source_refs[]` strings. Lane 03 ADV-053-A through L found no need for a fifth target identity class, but exposed one important continuity requirement before any executable source surface is introduced:

> source declaration occurrences and any associations between separate source facts must be explicit; equal token text, array position, lexical order, recency, resolver order, actor identity, CI state, schedule position, or Git state may not manufacture declaration identity or association.

The next step is therefore **not a resolver**. It is only a versioned typed declaration contract that can carry the four Decision 019 target classes without changing the meaning of historical source strings.

## Problem

The current artifact v0.1/v0.2/v0.3 and evidence-record v0.1 contracts expose `source_refs[]` as unique non-empty strings. Those values are permanently historical opaque declarations.

If a future contract merely replaced those strings with another flat list, later occupants could still accidentally:

- infer target class from lexical shape;
- collapse two declaration occurrences because their token text matches;
- pair a locator declaration with a content-address declaration by array position or recency;
- treat an exact AXM reference as proof that the target exists;
- treat a digest declaration as proof that bytes were retrieved and verified;
- treat successful integrity as trust, relevance, closure, or packet acceptance;
- reinterpret historical objects by running them through the new parser.

That would violate the Decision 019 research boundary before any resolver had even been built.

## Decision

Open one **contract-only typed source declaration surface** for new schema versions.

The contract must preserve the following semantics.

### 1. Historical source fields are immutable in meaning

- artifact schema v0.1/v0.2/v0.3 `provenance.source_refs[]` remain opaque historical strings forever;
- evidence-record schema v0.1 `source_refs[]` remain opaque historical strings forever;
- no old string gains typed source standing because it resembles an AXM reference, URL, path, Git identifier, digest, package id, or logical id;
- the new contract must use a new versioned field and/or new schema version;
- do not support dual authority where an old `source_refs[]` value and a new typed declaration silently compete for the same meaning.

### 2. Declaration occurrence identity must be explicit and order-free

For new typed source-bearing objects, declarations must be represented as a **map keyed by a stable declaration id**, not as an order-significant array.

The occurrence identity is:

```text
exact containing object identity + declaration key
```

Requirements:

- declaration keys use the repository's stable id spelling rule: `^[a-z0-9][a-z0-9._-]*$`;
- duplicate declaration keys fail closed through strict JSON parsing/object semantics;
- map key order is canonical presentation only and carries no priority, chronology, trust, or selection meaning;
- two containing objects may use the same declaration key without becoming the same declaration occurrence;
- equal target values in different declarations do not collapse their occurrence identity.

This directly answers ADV-053-A without inventing a global mutable source registry.

### 3. One declaration occurrence carries exactly one target identity fact

Every declaration value names exactly one Decision 019 target class:

- `opaque_label`
- `exact_axm_object`
- `content_address`
- `locator`

The class must be explicit in authored data. Lexical shape never selects the class.

A declaration must not contain multiple target classes at once. In particular, a locator and a content address are **two independent declarations** unless a later numbered decision introduces an explicit association relation.

Decision 020 does not define that relation. It therefore cannot claim that locator L resolved to content C merely because both are present in one object.

### 4. Minimal class payloads

#### `opaque_label`

Carries only an authored non-empty token.

Meaning: a source target label was declared, but target identity strength beyond that token is unresolved.

No path/URL/hash/AXM-reference parsing is authorized.

#### `exact_axm_object`

Carries one explicitly typed canonical AXM immutable reference.

Contract validation must use the existing shared Stage 2 immutable-reference parser rather than a second permissive source parser.

Decision 020 establishes only declared exact identity syntax. It does **not** exact-load the target and does not establish existence, retrievability, integrity, currentness, trust, provenance relation, closure, or acceptance.

No logical-id, newest-version, locator, recency, or store-order fallback is permitted.

#### `content_address`

The first bounded contract supports only:

- algorithm: `sha256`;
- digest: 64 lowercase hexadecimal characters;
- byte scope: `raw_bytes`.

This is deliberately narrower than a generic digest registry. Later algorithms or canonicalized-content scopes require a new grounded version rather than an underspecified string convention.

Decision 020 establishes only the declared immutable byte identity. It does not retrieve bytes, recompute the digest, or establish integrity success, trust, relevance, closure, or acceptance.

#### `locator`

Carries:

- a non-empty explicit `locator_context` token; and
- a non-empty locator value.

`locator_context` records authored addressing context only. Decision 020 does not define a resolver registry and does not assign trust or mutability properties from the context spelling.

A locator establishes no immutable content identity, successful resolution, network/filesystem authority, trust, or acceptance.

### 5. New artifact/evidence versions only

Lane 02 may add the smallest new artifact and evidence-record schema versions needed to host typed declarations, with these boundaries:

- historical versions remain byte/meaning compatible;
- new typed versions use `source_declarations` and do not reinterpret or silently merge legacy `source_refs`;
- for a new evidence-record version, the existing strong-evidence rule may require at least one typed source declaration instead of at least one legacy string, but this is source-presence evidence only;
- a proposed evidence record must not be silently upgraded into requiring sources unless its new authored version explicitly says so;
- containing-field meaning remains the only provenance relation established by this step: artifact-declared provenance source or evidence-declared support source.

Decision 020 does not introduce a general causal vocabulary such as `derived_from`, `used`, `verified_by`, or `observed_from`.

### 6. No implicit association

The following never associates two declaration occurrences:

- equal token text;
- equal locator text;
- equal digest;
- equivalent retrieved bytes;
- array/map/lexical order;
- same actor;
- same lane;
- same packet;
- same repository host;
- newest declaration;
- resolver order;
- schedule position;
- CI result;
- branch ownership;
- Git permission.

If two declarations later need an asserted relationship, that relationship requires a later explicit contract. Decision 020 deliberately stops before it.

## Bounded truth dimensions

A valid typed declaration establishes only that the containing object authored one source target identity fact in one explicit class.

It does **not** establish:

```text
target exists
or target is retrievable now
or retrieved bytes reproduce the declared identity
or the target actually influenced the subject
or the source is trustworthy / high quality / relevant
or all required sources were declared
or source closure
or evidence precedence / closure
or packet acceptance / rejection
or claim closure
or successor revision publication
or Stage 5 integration
or epoch/barrier completion
or replay correctness
```

These remain separate future facts.

## Lane 02 — smallest implementation

Implement only the Decision 020 contract surface.

Required behavior:

1. preserve artifact v0.1/v0.2/v0.3 and evidence-record v0.1 historical source semantics unchanged;
2. add the smallest new versioned typed-source surface using `source_declarations` keyed by stable declaration ids;
3. support exactly the four Decision 019 target classes with explicit discriminators;
4. enforce one target class per declaration occurrence;
5. use the shared Stage 2 parser for `exact_axm_object` references;
6. bound the first `content_address` form to `sha256` + lowercase 64-hex digest + `raw_bytes`;
7. keep locator context/value authored facts only; add no resolver;
8. make declaration-key order irrelevant to semantic meaning and deterministic identity;
9. forbid dual legacy/new source authority in the new typed versions;
10. add valid/invalid fixtures and deterministic tests;
11. keep every prior integrated regression green;
12. stop before target loading, resolver behavior, digest verification, source association, migration mapping, trust/relevance, completeness/closure, packet acceptance, successor publication, Stage 5 integration, epochs, or replay.

If implementation evidence shows that modifying both artifact and evidence schemas in one patch creates avoidable coupling, Lane 02 may split the work, but the first slice must preserve one shared declaration contract rather than two drifting class definitions.

## Minimum regressions

At minimum, prove:

- each of the four classes validates only when explicitly discriminated;
- lexical lookalikes cannot switch class;
- two declarations with equal target text but different keys remain distinct occurrences;
- the same declaration key may exist in two different exact containing objects without cross-object identity collapse;
- declaration-map key order does not create priority or selection meaning;
- a declaration cannot contain both locator and content-address payloads;
- exact AXM references use the canonical Stage 2 parser and malformed/noncanonical forms fail;
- `content_address` rejects unsupported algorithms, uppercase/non-64-hex digests, and non-`raw_bytes` scopes in this first version;
- locator declarations do not gain content/integrity fields by implication;
- historical exact-looking/path/URL/digest strings remain valid at historical opaque strength and are never reclassified;
- strong typed evidence source presence does not claim integrity/trust/closure;
- proposed typed evidence retains only the source-presence requirements explicitly authored for its version;
- no resolver, association, trust, closure, acceptance, integration, epoch, or replay authority appears.

## Lane 03 — adversarial surface

After Lane 02 publishes an exact tested head, attack at least:

- same declaration key with different target values inside one object;
- same key reused across different exact containing objects;
- equal token text across different declaration occurrences;
- malformed exact AXM refs accepted by a source-specific fallback parser;
- exact-looking `opaque_label` promoted by lexical shape;
- content-address algorithm/scope ambiguity;
- locator/context spelling gaining resolver or trust authority;
- mixed target-class payloads slipping through `oneOf`/validation boundaries;
- declaration map order or canonical key order becoming precedence;
- locator/content declarations being paired by key similarity, value equality, or relative position;
- historical source strings being upgraded by the new code path;
- source presence being laundered into integrity, trust, completeness, closure, or acceptance;
- copy/materialization/transport changing declaration key-to-target meaning;
- cross-field laundering from `content_ref`, dependency/evidence/subject/supersedes refs.

Do not attack resolver policy as though Decision 020 implemented one.

## Preserved uncertainty

Decision 020 deliberately does not resolve:

- how a locator is resolved;
- how source bytes are retained or loaded;
- integrity-check execution and evidence retention;
- explicit association between locator/content/exact declarations;
- migration objects linking historical opaque declaration occurrences to future typed declarations;
- general provenance-relation vocabulary;
- source trust, quality, relevance, completeness, or closure;
- dependency admissibility/satisfaction/closure;
- evidence precedence/invalidation/closure;
- multiple-required-state semantics;
- logical lineage / `supersedes_ref` validity;
- global claim/occupancy currentness and authorization;
- packet conflict/selection and acceptance;
- claim closure and successor publication;
- Stage 5 integration receipts/runtime;
- epochs/barriers and replay;
- cross-language source transport and reproduction;
- stronger durability/concurrency and hostile same-process isolation.

## Root grounding

- **Truth:** typed class is explicit; historical strings retain authored strength; declaration validity is not existence, integrity, trust, closure, or acceptance.
- **Agency / non-domination:** no resolver, actor category, host, recency, ordering convention, CI result, specialist role, founder status, or Git permission becomes source authority.
- **Continuity:** declaration occurrence identity is explicit and order-free, so a replacement occupant does not need private pairing or token-equality conventions.
- **Wisdom before speed:** establish the typed declaration contract before building loaders, resolvers, integrity execution, source associations, trust policy, closure, or integration.
