# Decision 003 — Canonical Portability Semantics

Status: accepted architecture constraint for Stage 2 repair

## Context

Lane 02 PR #7 introduced the first production canonicalization and immutable-reference implementation. Lane 03 then challenged the exact reconciled implementation and preserved two concrete cross-runtime counterexamples in integrated PR #8:

- `ADV-021-A`: repository prose said object keys are "sorted" while the Python implementation inherited Python Unicode scalar-value ordering. A normal JavaScript UTF-16 sort can order `U+E000` and `U+10000` differently, producing different canonical bytes and hashes from the same valid object.
- `ADV-022-A`: repository prose said reference components use "canonical percent encoding" while the Python implementation inherited `urllib.parse.quote(..., safe="._-")`. Common URL encoders disagree about characters such as `! * ' ( )`, producing different `axmref:v1` spellings from the same logical component.

The Python implementation is internally deterministic. The failure is that part of the identity contract still lives in host-language convention instead of explicit institutional state.

## Decision

Stage 2 identity is not ready for integration until the following rules are explicit in repository-visible contract text and regression-tested in production code.

### 1. Object-key ordering

For the Stage 2 canonical JSON subset, object member names MUST be ordered lexicographically by Unicode scalar value sequence, ascending.

Because Stage 2 already requires NFC text and rejects surrogate code points, comparison is over the resulting sequence of Unicode scalar values (`U+0000` through `U+10FFFF`, excluding surrogates).

Comparison rules:

1. compare the first differing Unicode scalar value numerically;
2. the lower scalar value sorts first;
3. if one key is an exact prefix of another, the shorter key sorts first.

This preserves the current Python implementation's intended ordering semantics without making Python itself normative. Implementations in runtimes with UTF-16-native string ordering must implement the scalar-value comparison explicitly rather than relying on their host's default sort.

Required witness:

```text
U+E000 < U+10000
```

Therefore the canonical object containing those two keys must place `U+E000` first.

### 2. `axmref:v1` component percent encoding

Logical-id and version components MUST use one byte-level encoding independent of host URL helpers:

1. input text must already satisfy the Stage 2 canonical string rules (including NFC and no surrogate code points);
2. encode the text as UTF-8 bytes;
3. emit bytes for ASCII `A-Z`, `a-z`, `0-9`, `-`, `.`, `_`, and `~` literally;
4. percent-encode every other byte as `%` followed by exactly two uppercase hexadecimal digits `0-9A-F`;
5. spaces are therefore `%20`, never `+`;
6. a literal `%` is `%25`;
7. non-ASCII text is percent-encoded byte-by-byte from its UTF-8 representation;
8. parsing must reject any spelling that does not round-trip to this exact canonical encoding.

Required witness:

```text
a!b*a'b(c)
-> a%21b%2Aa%27b%28c%29
```

This intentionally preserves the spelling currently produced by Lane 02's Python implementation while moving the rule out of Python library behavior and into the institution contract.

## Integration consequence

PR #7 remains deferred, not rejected.

Lane 02 should repair the smallest possible surface:

- make the two rules above normative in `IDENTITY_V0.md`;
- ensure production code implements the rules without depending on undocumented host defaults;
- add regression vectors for `ADV-021-A` and `ADV-022-A`;
- rerun the deterministic identity suite and compilation evidence on the changed head;
- preserve the current Stage 2 scope and do not begin Stage 3 in the same repair.

Lane 03 should then verify the repaired exact head. It does not need to reopen later-stage stale-state, lineage, epoch, integration, or replay obligations during that bounded verification.

## Root grounding

### Truth

Canonical identity must be reconstructable from explicit rules, not from knowing which standard-library helper happened to be used.

### Agency / non-domination

No runtime or specialist is privileged by category. The current Python behavior is retained only because it is a small compatible choice once fully specified; another rule could have been chosen if equally explicit and grounded.

### Continuity

A replacement occupant or future non-Python implementation can reproduce hashes and references from repository state alone.

### Wisdom before speed

Freezing these byte-level semantics before durable state/replay depends on them is cheaper and safer than migrating stored identities later.

## Truth boundary

This decision specifies two Stage 2 portability semantics. It does not claim:

- PR #7 is integrated;
- the complete canonical JSON serializer is proven portable across every runtime;
- Stage 3 state storage exists;
- stale-state, lineage, epoch, integration, or replay checks are implemented;
- autonomous institutional correctness has been established.

Those remain separate evidence gates.
