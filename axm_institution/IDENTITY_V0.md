# Stage 2 Identity v0

This module is the smallest production identity layer for AXM Institution Fabric Stage 2. It implements deterministic load/validation, canonical bytes, reproducible SHA-256 instance identity, explicit immutable references, and exact strong-evidence subject binding.

It does **not** implement the state store, work ledger, repository-level reference existence, stale-base checks, supersession-lineage validation, epoch/base validation, integration, or replay. Those remain later-stage obligations.

## Canonical JSON subset

Stage 2 uses an intentionally narrow JSON subset so identity does not depend on parser quirks or silent normalization.

Supported values:

- `null`;
- booleans;
- integers in the cross-runtime safe range `-9007199254740991` through `9007199254740991`;
- NFC-normalized Unicode strings without surrogate code points;
- arrays of supported values;
- objects with string keys and supported values.

Strict parsing rejects:

- duplicate object keys;
- floating-point number spellings;
- non-canonical integer spelling such as `-0`;
- integers outside the safe range;
- `NaN` / `Infinity` style non-standard constants;
- non-NFC text instead of silently normalizing it;
- surrogate code points;
- malformed JSON.

The canonical byte representation is UTF-8 JSON with no insignificant whitespace, no ASCII-only escaping, and no NaN-style values. Schema defaults are **not** inserted. An omitted optional field and an explicitly supplied default-valued field therefore remain different content unless a future explicit semantic rule says otherwise.

### Object-key ordering

Object member names are ordered lexicographically by their Unicode scalar-value sequence, ascending, after the NFC/no-surrogate checks above.

Comparison is explicit and host-independent:

1. compare the first differing Unicode scalar value numerically;
2. the lower scalar value sorts first;
3. if one key is an exact prefix of the other, the shorter key sorts first.

A runtime whose native string comparison is UTF-16 based must implement this scalar-value comparison rather than relying on its host default sort.

Required Stage 2 witness (`ADV-021-A`):

```text
U+E000 < U+10000
```

So a canonical object containing those two keys emits `U+E000` first.

## Validated instance identity

`canonical_validated_sha256(value, schema_name)` first validates the object against the integrated Stage 1 Draft 2020-12 contract and then hashes its canonical bytes with SHA-256.

Logical identity and immutable identity are different:

- logical id example: `artifact.rules`;
- immutable instance: exact validated canonical content, including its `version` field when the object has one.

Two objects may share the same logical id while receiving different immutable identities because their version or content differs.

## Immutable reference format

The v0 reference format is:

```text
axmref:v1:<kind>:<logical-id>:<version-token>:sha256:<64-lowercase-hex>
```

`kind` is derived from the schema filename (`artifact.schema.json` -> `artifact`). Objects without an instance `version` field use the token `-`. Objects with a version use `v=<encoded-version>`, so a real version string such as `-` becomes `v=-` and cannot collide with the no-version sentinel. `schema_version` is not substituted for instance version.

### Component encoding

Logical-id and version components use one byte-level encoding independent of host URL helpers:

1. the input text must already satisfy the Stage 2 canonical string rules (NFC, no surrogate code points);
2. encode the text as UTF-8 bytes;
3. emit ASCII bytes `A-Z`, `a-z`, `0-9`, `-`, `.`, `_`, and `~` literally;
4. percent-encode every other byte as `%` followed by exactly two uppercase hexadecimal digits `0-9A-F`;
5. spaces are `%20`, never `+`;
6. a literal `%` is `%25`;
7. non-ASCII text is percent-encoded byte-by-byte from its UTF-8 representation;
8. parsing rejects any spelling that does not round-trip to this exact canonical encoding.

Required Stage 2 witness (`ADV-022-A`):

```text
a!b*a'b(c)
-> a%21b%2Aa%27b%28c%29
```

Parsing also rejects malformed hashes, unknown structure, invalid UTF-8, non-canonical percent escapes, and non-canonical Unicode components. Resolving a reference requires exactly one candidate whose reconstructed immutable reference matches byte-for-byte.

The SHA-256 digest identifies canonical content; the typed kind/id/version fields keep the reference understandable to a fresh occupant and prevent the digest from becoming an undocumented opaque convention.

## Strong evidence binding

For these evidence states:

```text
compiled
automated_tested
runtime_tested
visually_inspected
playtested
measured
```

the identity helper requires `subject_ref` to equal the exact immutable reference reconstructed from the supplied subject instance.

The `ADV-015-B` regression fixture proves that evidence generated for `artifact.rules` version 1 does not silently transfer to version 2 merely because both share the logical id `artifact.rules`.

## Lane 03 Stage 2 ambiguity and portability oracles

The production test spine explicitly covers the Stage 2 requirements frozen by Lane 03 evidence and Decisions 002/003:

- `ADV-017-A`: duplicate JSON member names fail during strict parsing, before validation or hashing;
- `ADV-018-A`: Unicode policy is explicit — v0 accepts NFC and rejects NFD/non-NFC input instead of silently normalizing it;
- `ADV-019-A`: JSON Schema defaults are not materialized by validation; omitted optional content and explicitly present default-valued content remain distinct immutable input;
- `ADV-020-A`: a bare SHA-256 digest is not a valid immutable reference; typed `axmref:v1` context is required;
- `ADV-021-A`: object-key ordering is Unicode-scalar-value lexicographic, including the `U+E000 < U+10000` witness;
- `ADV-022-A`: immutable-reference components use the explicit UTF-8 byte / uppercase `%HH` encoding above, including the punctuation witness.

These oracles constrain the identity layer without pulling stale-state, lineage, or epoch validation forward from later stages.

## Deliberately deferred relationships

Stage 2 creates identities that later validators can trust; it does not pretend isolated identity code knows repository history.

The following integrated Lane 03 oracles remain for later state/runtime layers:

- `ADV-002-B`: stale packet/target versus current state;
- `ADV-011-B`: epoch packet/base coherence and replayable progression;
- `ADV-006-B`: supersession existence, ordering, and acyclicity.

`supersedes_ref` can therefore be hashed as explicit artifact content in Stage 2, but whether it resolves to a valid prior immutable artifact instance is a Stage 3/4 cross-object question.

## Root boundary

This module makes deterministic execution decisions only. It grants no actor, lane, model, founder, or Git permission canonical authority. Integration of identity conventions remains accountable to Truth, Agency / non-domination, Continuity, and Wisdom before speed.
