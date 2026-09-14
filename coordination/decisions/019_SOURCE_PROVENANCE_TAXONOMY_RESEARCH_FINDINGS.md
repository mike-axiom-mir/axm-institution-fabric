# Decision 019 Research Findings — Minimal Source Provenance Taxonomy

Date: 2026-09-14
Status: **concrete research proposal; adversarial review required before any implementation decision**
Stage: **Stage 4 — claim / occupancy / return lifecycle**

This file is a research finding under Decision 019. It does **not** modify Decision 019, authorize a schema migration, add a resolver, or make source presence sufficient for trust, closure, acceptance, integration, or replay.

## Research question

What is the smallest domain-neutral source taxonomy that lets a future occupant distinguish source identity strength without silently rewriting historical `source_refs[]` strings or introducing filesystem, network, repository-host, actor, recency, or resolver authority into the universal kernel?

## Repository inventory

The current universal contract pack has two authored source-bearing fields:

1. `artifact.provenance.source_refs[]`
   - artifact schema versions `0.1`, `0.2`, and `0.3`;
   - unique non-empty strings;
   - no `pattern`, `format`, `enum`, or `const` gives those strings identity strength;
   - artifact version branches do not redefine the field.
2. `evidence-record.source_refs[]`
   - evidence-record schema `0.1`;
   - unique non-empty strings;
   - no authored identity-strength syntax;
   - strong evidence states require at least one source string, but that requirement proves only that a source was declared, not that it is exact, retrievable, trusted, complete, or replayable.

Representative historical values already include:

- repository-relative paths such as `NEXT_BUILD.md`, `BUILD_PLAN.md`, coordination decision paths, and `fixtures/contracts/valid.json`;
- path-like subject/content/dependency values on neighboring fields;
- Git-like strings such as the historical artifact `base_state_revision` value;
- and, through the Decision 019 compatibility regression, URL-like, hash-like, logical-label-like, and syntactically exact-looking `axmref:` strings that are intentionally still accepted as opaque historical source strings.

Source-adjacent fields are **not** source aliases. `content_ref`, `dependency_refs`, `evidence_refs`, `subject_ref`, `supersedes_ref`, lifecycle base refs, and state-revision membership refs each have their own authored relation and must not be cross-laundered into source provenance.

## External research used only as comparison evidence

The proposal was checked against established provenance/content-addressing designs without importing them as authority:

- W3C PROV separates entities, activities, agents, and provenance relationships. This supports keeping *what is named*, *who/what asserted or used it*, and *the relation between them* distinct rather than making actor identity a source identity class.
- SLSA v1.2 source guidance separates a human-facing URI from a revision digest and explicitly says the URI is not intended for policy decisions. Its build provenance also records resolved dependencies with a URI and digest as separate facts.
- OCI content descriptors separate a content identifier (digest) from metadata such as media type and size, and treat the digest as the content-addressing/integrity anchor.

AXM does not require those standards, internet access, their exact syntax, or their policy models. They are comparison evidence that the separation below is not an arbitrary private convention.

## Minimal universal taxonomy proposal

The smallest grounded taxonomy is **four source identity classes**. Repository snapshots, network sources, and human/machine assertions are compositions or provenance facts around these classes rather than additional universal identity classes.

### Class A — `opaque_label`

Purpose: preserve a declared source token whose identity strength is unresolved.

Identity:
- exactly the authored string token and its containing historical object;
- no semantic parsing of path/URL/Git/hash/`axmref` shape.

Existence / retrievability:
- unknown;
- local resolution success does not upgrade the class.

Integrity:
- none implied.

Provenance relation:
- only the relation authored by the containing field: artifact-declared provenance source or evidence-declared source;
- no automatic `derived-from`, `verified-by`, `used`, `caused`, or equivalent causal meaning.

Quality / trust:
- none implied.

Closure:
- none implied. The list is not a claim that all sources have been enumerated.

Offline / replay:
- the exact token can be replayed as a historical assertion;
- the underlying source cannot be reconstructed from this class alone.

Migration:
- **all historical `source_refs[]` values are permanently interpreted at this strength**, including values that happen to look like another class.

Examples:
- `NEXT_BUILD.md` in artifact v0.1 provenance;
- `fixtures/contracts/valid.json` in evidence v0.1;
- `https://example.invalid/source` in a historical source field;
- `sha256:<hex>` in a historical source field;
- an exact-looking `axmref:v1:...` in a historical source field.

### Class B — `exact_axm_object`

Purpose: name one exact immutable AXM institution object when a future versioned contract explicitly says that is the source identity class.

Identity:
- canonical AXM immutable reference, including kind, logical id/version component where applicable, digest, and canonical spelling under the existing identity contract.

Existence / retrievability:
- **not implied by syntax**;
- exact store loading is a separate observed fact and may fail explicitly.

Integrity:
- if the target is exact-loaded through the existing canonical store path, reproduced canonical bytes must match the reference digest;
- an unloaded exact-looking ref is not integrity evidence.

Provenance relation:
- still separate from identity. The exact object being named does not itself prove why or how it influenced the subject.

Quality / trust:
- none implied by being an AXM object.

Closure:
- none implied.

Offline / replay:
- identity survives offline;
- full reconstruction requires the exact object bytes to remain available in an object store or replay bundle;
- missing bytes are explicit missing evidence, never a reason to substitute a newer same-logical object.

Migration:
- a later typed declaration may explicitly link to an old opaque token, but the old token itself does not become this class.

### Class C — `content_address`

Purpose: name immutable bytes/content that are not required to be AXM institution objects.

Identity:
- explicit digest algorithm plus digest value over a specified byte scope;
- a bare hash-looking historical string is not this class;
- byte scope/canonicalization must be explicit if the source is not raw bytes.

Existence / retrievability:
- not implied. A digest can name content that is currently unavailable.

Integrity:
- verifiable only when candidate bytes are obtained and independently reproduce the declared digest.

Provenance relation:
- separate from identity; matching bytes do not prove that those bytes were actually used by the producer or evidence method.

Quality / trust:
- none implied. A cryptographically identified source can still be wrong, malicious, irrelevant, or low quality.

Closure:
- none implied.

Offline / replay:
- identity and later integrity verification are offline-safe;
- replay still needs the bytes from any compatible local bundle/store/cache.

Migration:
- no digest is inferred from a legacy string. A new typed declaration needs explicit digest evidence.

### Class D — `locator`

Purpose: preserve where/how a source was named or found without pretending the location is immutable content identity.

Identity:
- the locator string plus its explicitly declared locator scheme/context in a future typed contract;
- examples can include a path, URI, repository location, branch/ref, service key, or other address.

Existence / retrievability:
- resolution is a time/context-specific observation, not permanent truth;
- unavailable, moved, redirected, deleted, or permission-gated targets remain explicit failure states.

Integrity:
- none from the locator alone;
- a locator can be paired with a separate `content_address` or `exact_axm_object` declaration when immutable identity is known.

Provenance relation:
- separate from identity; resolving a URL/path does not prove the resolved content influenced the subject.

Quality / trust:
- none implied by scheme, host, repository, filesystem location, or successful resolution.

Closure:
- none implied.

Offline / replay:
- locator spelling is replayable;
- successful resolution is not guaranteed offline and must never be required to reconstruct historical institutional meaning when immutable content evidence was separately captured.

Migration:
- historical path/URL/Git-like source strings remain `opaque_label`; they are not silently promoted into locators. A later typed declaration can copy the spelling only as a newly asserted locator fact.

## Why the evaluated candidate categories reduce to four

### Repository/file snapshot is a composition, not a fifth identity class

A truthful immutable snapshot needs an immutable identity (`content_address` or, when it is already an institution object, `exact_axm_object`) plus optional `locator`/repository context describing where it came from. A path, Git branch, or `HEAD` alone is only a locator. A Git commit or tree identifier can serve as a content/revision identity only when a future contract explicitly states the digest/revision semantics and verification scope.

Making `repository_snapshot` a universal primitive would bake one storage/version-control model into the kernel when the actual universal facts are content identity plus optional location/context.

### External/network source is a locator until immutable identity is separately recorded

`https://...` identifies a network location, not immutable bytes. If fetched bytes are digested, the source may have both a `locator` fact and a `content_address` fact. Network availability, TLS success, host identity, redirect order, or resolver preference cannot choose institutional truth.

### Human/machine assertion is provenance of the assertion, not a source identity class

Whether a human, model, script, sensor, or other intelligence asserted a source concerns responsibility/method/provenance around the declaration. It does not change what the source target *is*. Treating actor category as a source identity class would mix identity with responsibility and risk category-based authority. Future assertion provenance should remain a separate relation grounded by evidence, not hidden source-selection power.

## Relation boundary

This research does **not** open a universal causal provenance vocabulary.

For current historical fields, the only grounded statement is:

- `artifact.provenance.source_refs[]`: the artifact declares these tokens as provenance sources;
- `evidence-record.source_refs[]`: the evidence record declares these tokens as source support.

A future typed source declaration may need an explicit relation/role, but Decision 019 does not have evidence to choose a complete domain-neutral vocabulary such as `derived_from`, `used`, `observed_from`, `verified_by`, or `reported_by`. No such meaning should be inferred from identity class.

## Identity, retrieval, integrity, trust, and closure are orthogonal

A future source view should preserve these as separate facts:

```text
what source identity is declared
    != target exists now
    != target can be retrieved now
    != retrieved bytes match immutable identity
    != source relation to subject is proven
    != source is trustworthy / high quality / relevant
    != all required sources are present
    != evidence or packet is accepted
```

No resolver may collapse those states into one success boolean.

## Historical migration / non-reinterpretation rules

1. Existing artifact v0.1/v0.2/v0.3 `provenance.source_refs[]` remain `opaque_label` semantics forever.
2. Existing evidence-record v0.1 `source_refs[]` remain `opaque_label` semantics forever.
3. Lexical shape never upgrades a historical value, including valid-looking `axmref`, URL, path, Git id, digest, package id, or logical id.
4. A future typed source surface must use a new schema version and/or a new explicitly typed field. It must not reinterpret the old array in place.
5. A migration may create a **new immutable declaration** that records both the historical opaque token and a newly grounded typed source identity. That new declaration does not rewrite the original object's meaning.
6. If a claimed mapping cannot reproduce the exact AXM object or candidate content bytes, the mapping remains unresolved/failed rather than falling back to logical id, location, newest version, or network success.
7. Multiple candidate mappings remain multiple facts until an explicit later policy resolves them. Array order, recency, actor identity, branch ownership, resolver preference, and Git permission are not tie-breakers.

## Offline and replay implications

| Class | Identity survives offline | Underlying bytes guaranteed offline | Integrity can be rechecked offline | Network/filesystem resolver required for historical meaning |
| --- | --- | --- | --- | --- |
| `opaque_label` | yes, token only | no | no | no |
| `exact_axm_object` | yes | only if exact object bytes are retained | yes, when bytes retained | no |
| `content_address` | yes | only if bytes are retained | yes, when bytes retained | no |
| `locator` | yes, locator only | no | no, unless paired with immutable identity | **must not be required** |

Replay bundles may therefore retain immutable object/content bytes plus auxiliary locators, but a missing external location must not silently alter the historical source declaration.

## Adversarial cases the proposal must survive

1. **Same locator, different bytes over time:** a mutable path/URL/branch resolves to content A, later content B. Locator equality must not imply content equality.
2. **Same bytes, different locators:** two mirrors resolve to identical bytes. Different locators do not imply different content identity.
3. **Exact-looking historical string:** old `source_refs[]` contains a canonical-looking `axmref`; it remains `opaque_label` and cannot exact-load by authority of spelling.
4. **Missing exact AXM source:** a typed exact source ref is canonical but its object is absent. Identity survives; retrievability fails explicitly; no logical/recency fallback.
5. **Wrong/corrupt exact AXM source:** target exists at a path but does not reproduce the declared reference. Integrity fails; local presence does not override it.
6. **Digest without bytes:** content address is syntactically valid but content unavailable. Existence/integrity stay unresolved.
7. **Digest mismatch:** retrieved bytes do not match. Do not retain a successful integrity state because the locator was trusted or available.
8. **Mutable repository name/ref:** repository URL + `main`/`HEAD` changes. It remains locator context unless immutable revision/content identity is separately declared and verified.
9. **Conflicting source declarations:** exact/content/locator declarations disagree. Preserve conflict; newest, first, actor, host, and resolver order do not win automatically.
10. **Cross-field laundering:** `content_ref`, `dependency_refs`, `evidence_refs`, `subject_ref`, or `supersedes_ref` resembles a source. It gains no source authority without an explicit source relation.
11. **Trust laundering:** exact identity or digest verification is green but the source is irrelevant, malicious, low quality, or contradicted. Integrity is not trust or relevance.
12. **Closure laundering:** all declared source targets resolve. This does not prove the list was complete or evidence/packet closure.
13. **Offline replacement occupant:** network and original filesystem are absent. The occupant must still reconstruct the historical identity-strength class and unresolved state without private resolver conventions.

## Rejected alternatives

### Rejected: one string union parsed by lexical shape

Example shortcut:

```text
if starts with axmref -> exact AXM object
else if starts with http -> network source
else if looks like sha256 -> content source
else -> path/logical source
```

Rejected because it:
- silently upgrades historical strings;
- makes parser convention hidden authority;
- conflates identity with retrieval/integrity;
- gives filesystem/network/repository syntax universal-kernel power;
- cannot truthfully distinguish same-label/different-bytes cases;
- creates migration drift across runtimes.

### Rejected: every source is an AXM artifact

Rejected because external immutable bytes, mutable locations, and unresolved assertions do not necessarily participate in artifact lifecycle/version/provenance semantics. Forcing them into `artifact` would erase a useful boundary and create fake institutional ownership/meaning.

### Rejected: every source is a mandatory locator+digest pair

Rejected because it cannot truthfully represent unresolved historical assertions or exact institution objects without redundant/fictional locators, and it would incorrectly require retrievable byte-oriented semantics for every source declaration.

### Rejected: actor category as source identity class

Rejected because human/machine/tool responsibility is provenance of the assertion or activity, not target identity. Category must not create source-selection authority.

## Comparison-evidence references

- W3C PROV publications: `https://www.w3.org/groups/wg/prov/publications/`
- SLSA v1.2 source requirements: `https://slsa.dev/spec/v1.2/source-requirements`
- SLSA v1.2 build provenance: `https://slsa.dev/spec/v1.2/build-provenance`
- OCI descriptor specification: `https://specs.opencontainers.org/image-spec/descriptor/`

These references inform the separation of concepts only. AXM remains offline-capable and does not depend on these sites or standards at runtime.

## Recommendation

**Do not open source runtime/schema implementation yet.** The research is concrete enough to give Lane 03 an exact adversarial target now, which Decision 019 previously lacked.

Next sequence:

```text
Decision 019 concrete four-class taxonomy proposal
    -> Lane 03 adversarial review of identity-strength and migration boundaries
    -> Lane 01 integration/research disposition
    -> only if the proposal survives: consider Decision 020
```

If later opened, Decision 020 should be smaller than a resolver: define only an explicitly typed immutable source-declaration contract that can distinguish the four identity classes without reinterpreting historical arrays. Target loading, network/filesystem resolution, integrity checking, relation vocabulary, quality/trust, source closure, packet acceptance, Stage 5 integration, epochs, and replay should remain separate later gates.

## Stop condition for this research packet

This proposal is complete enough for an independent occupant to challenge without private chat state. Decision 019 itself remains active until that adversarial review is recorded and Lane 01 decides whether the four-class taxonomy is sufficiently grounded to open the next numbered bounded step.
