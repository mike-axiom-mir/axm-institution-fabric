# Decision 004 — Canonical JSON String Escape Semantics

Status: accepted for Stage 2 repair

## Context

Lane 03 exact-head verification of Stage 2 PR #7 confirmed the Decision 003 repairs for Unicode scalar-value key ordering and `axmref:v1` UTF-8 byte encoding, then exposed `ADV-023-A`: canonical JSON string spelling was still partly inherited from Python `json.dumps` rather than fully reconstructable from repository state.

The ambiguity is sufficient to affect immutable identity. For example, JSON spellings `"a/b"` and `"a\/b"` decode to the same supported string value but are different bytes. A future implementation could therefore preserve logical content yet derive a different SHA-256 identity if the string-rendering contract remains implicit.

This decision freezes the smallest explicit Stage 2 string-escape contract while preserving the current intended Python output. It does not begin Stage 3 state-store, ledger, stale-base, lineage, epoch, integration, or replay semantics.

## Decision

For every JSON string value and every JSON object member name in Stage 2 canonical bytes, after the already-required NFC and no-surrogate checks:

1. Begin and end the string with ASCII quotation mark `"`.
2. Emit quotation mark `U+0022` as `\"`.
3. Emit reverse solidus `U+005C` as `\\`.
4. Emit solidus `/` (`U+002F`) literally. Optional solidus escaping as `\/` is forbidden in canonical output.
5. Emit these control characters using the short JSON escapes:
   - `U+0008` -> `\b`
   - `U+0009` -> `\t`
   - `U+000A` -> `\n`
   - `U+000C` -> `\f`
   - `U+000D` -> `\r`
6. Emit every other scalar value in `U+0000..U+001F` as exactly six ASCII characters `\u00xx`, using lowercase hexadecimal letters `a-f` where letters are required.
7. Emit every other permitted Unicode scalar value literally and encode the resulting canonical JSON text as UTF-8. Do not replace printable/non-control characters with optional `\uXXXX` or surrogate-pair escapes.
8. No other optional JSON escape spelling is canonical. A serializer may parse alternate valid JSON spellings, but canonical identity is computed only from the spelling defined above.

The rule applies identically to object keys and string values.

## Required witness vectors

These exact decoded value -> canonical JSON-string byte spellings are Stage 2 regression requirements:

```text
a/b        -> "a/b"
"          -> "\""
\          -> "\\"
U+0008     -> "\b"
U+0009     -> "\t"
U+000A     -> "\n"
U+000C     -> "\f"
U+000D     -> "\r"
U+0000     -> "\u0000"
U+000B     -> "\u000b"
U+001F     -> "\u001f"
é          -> "é"        (UTF-8 bytes C3 A9 inside the quotes)
U+2028     -> literal U+2028 inside the quotes
U+2029     -> literal U+2029 inside the quotes
```

At minimum, the production regression suite must freeze:

- `ADV-023-A`: `a/b` renders with literal `/`, never `\/`;
- one short control escape witness;
- one non-short control escape containing `a-f` to freeze lowercase hex spelling;
- one non-ASCII literal witness to prove optional ASCII-only `\u` escaping is forbidden.

## Why preserve this spelling

The current PR #7 Python renderer already produces these spellings with `json.dumps(..., ensure_ascii=False, separators=(",", ":"))`. The institutional rule is therefore being externalized rather than changed merely for stylistic preference.

Python behavior itself is not authoritative. After this decision, the repository contract above is authoritative for Stage 2 canonical bytes, and production code must be tested against it explicitly.

## Evidence boundary

This decision establishes the required semantics. It does not itself prove that PR #7 implements them independently of host serializer behavior.

Fresh evidence is required after Lane 02 repairs or documents the production renderer and adds regression vectors. Previous `23 passed` evidence predates this decision and cannot be reused as proof for changed source/tests.

Lane 03 should then verify the exact repaired head against `ADV-023-A` and the required witnesses. Stage 2 remains unintegrated until that bounded repair/verification cycle is complete.

## Root grounding

### Truth

Immutable identity must be reproducible from explicit repository semantics, not unstated serializer ancestry.

### Agency / non-domination

No language runtime or specialist receives authority by incumbency. Any implementation may occupy the lane if it reproduces the explicit byte contract.

### Continuity

A replacement occupant or implementation can reconstruct canonical bytes without private knowledge that the first implementation used Python.

### Wisdom before speed

Freezing the byte rule before immutable identities are stored is cheaper and safer than repairing divergent identity histories after Stage 3 begins.

## Deferred questions

This decision does not settle:

- schema-contract revision identity;
- repository-level reference existence;
- stale-base validation;
- supersession graph validity;
- epoch/base coherence;
- integration-runtime semantics;
- replay.

Those remain later-stage work unless new evidence shows an earlier dependency.