# Decision 025 — Exact Integration Receipt Identity and Acyclic Publication Chronology

Date: 2026-09-15
Status: **accepted Stage 5 entry prerequisite; implementation open only for exact integration-receipt identity and one-way publication chronology. Stage 5 state mutation, packet acceptance execution, claim closure, successor publication runtime, epochs, and replay remain closed.**

## Why this decision exists

Decision 024 is now canonical and provides one bounded read-only fact: whether one exact return packet fits the first created-output Stage 5 acceptance-candidate slice. That fact is intentionally not packet acceptance or integration.

The next Stage 5 entry audit finds one smaller prerequisite before any mutating integration runtime can truthfully publish a successor revision: the integration receipt contract still uses opaque/logical strings where the already-canonical identity layer requires exact immutable instances, and the existing receipt/result shape invites a reciprocal content-addressed reference cycle if strengthened naively.

The current `integration-receipt.schema.json` v0.1 exposes:

- `base_state_revision` as a generic string;
- `packet_ids[]` as logical ids;
- `resulting_state_revision` as a generic string for accepted decisions.

Decision 002 already requires consequential Stage 5 integration/replay relationships to consume explicit immutable identities rather than invent another reference convention. Therefore a v0.1 receipt cannot, by itself, prove which exact base revision, exact packet instance, or exact successor instance participated in one integration transition.

At the same time, state-revision schema v0.2 already gives successor revisions an exact `integration_receipt_refs[]` membership relation. If an accepted receipt were changed to exact-reference that same successor revision, the two content-addressed objects would form a reciprocal dependency:

```text
successor revision S -> exact receipt R
receipt R            -> exact successor revision S
```

Neither immutable hash can be constructed first without hidden placeholders, mutation, indirection, or another ungrounded convention.

The smallest truthful next move is therefore to version the receipt identity contract and freeze an acyclic publication order before implementing Stage 5 mutation.

## Single blocking fact named by this audit

> Before Stage 5 may publish a canonical successor revision, one integration decision record must bind the exact base revision and exact packet instance(s), and accepted-result chronology must remain content-addressable without requiring the receipt and successor revision to exact-reference each other.

This is the only prerequisite opened by this decision.

## Required v0.2 receipt identity contract

Lane 02 should introduce the smallest versioned integration-receipt contract equivalent to the following semantics while preserving historical v0.1 readability:

1. **Exact base identity.**
   - v0.2 uses `base_state_revision_ref` carrying one canonical exact immutable `state-revision` reference.
   - a logical id, generic string, newest/current revision lookup, branch/HEAD, timestamp, or actor assertion cannot substitute for this exact base identity.

2. **Exact packet identity.**
   - v0.2 uses `packet_refs[]` carrying one or more canonical exact immutable `return-packet` references.
   - logical packet ids, same-logical-id/different-instance substitution, recency, array discovery, or storage order cannot identify the packet used by the decision.

3. **Existing decision facts remain facts, not new authority.**
   - `decision`, `reasons`, `root_grounding`, and `unresolved_conflicts` remain explicit receipt facts under the existing bounded vocabulary/shape unless a later decision changes them.
   - this decision does not automate constitutional root approval and does not make the receipt author, CI, Git permission, schedule position, or role an authority.

4. **No exact successor reference inside an accepted v0.2 receipt.**
   - accepted v0.2 receipts must not require or carry an exact immutable reference to the successor state revision they help explain;
   - the old v0.1 `resulting_state_revision` field remains historical v0.1 data and is not silently reinterpreted as exact v0.2 identity.

5. **Acyclic accepted publication chronology.**

```text
exact base revision B
exact eligible packet P
    -> construct/store exact receipt R that binds B + P + decision facts
    -> construct/store successor revision S
       where S.parent_revision_ref == B
       and S.integration_receipt_refs includes exact R
```

This gives the reconstructable one-way graph:

```text
S -> R -> {B, P...}
```

It avoids the reciprocal `S <-> R` content-hash cycle. It does not yet authorize a runtime to perform those writes.

6. **Historical v0.1 remains historical.**
   - existing v0.1 receipt objects remain valid/readable under their historical schema;
   - they must not be silently promoted into proof of exact Stage 5 base/packet/result identity;
   - migration, if later needed, must produce a new explicit object rather than rewriting historical meaning.

## Required semantic validation

Shape-only regex acceptance is not enough for consequential exact references. The v0.2 path should reuse the shared immutable-reference parser / canonical spelling rules so that:

- `base_state_revision_ref` parses and round-trips exactly as kind `state-revision`;
- every `packet_refs[]` value parses and round-trips exactly as kind `return-packet`;
- wrong-kind exact references fail closed;
- non-canonical spellings fail closed rather than being normalized into a different identity;
- duplicate exact packet refs remain rejected;
- no mutable current/HEAD lookup participates.

This decision does not require the receipt preflight to exact-load the referenced objects yet if doing so would widen into Stage 5 operational mutation semantics. The minimum is exact typed identity at the contract/semantic-validation layer.

## Required implementation evidence

Lane 02 should implement only this Decision 025 contract/validation slice and add deterministic regressions demonstrating at least:

1. one v0.2 receipt with an exact canonical base revision ref and exact canonical packet ref validates;
2. a logical/generic base string is rejected for v0.2;
3. a logical packet id is rejected for v0.2;
4. wrong-kind exact refs are rejected for both base and packet fields;
5. non-canonical exact-reference spellings fail rather than silently normalize;
6. same-logical-id/different-exact packet refs remain distinguishable;
7. duplicate exact packet refs are rejected;
8. accepted v0.2 has no exact successor-state field and therefore cannot create the demonstrated reciprocal content-addressed cycle;
9. historical v0.1 receipt fixtures remain readable/valid under v0.1 but are explicitly insufficient for exact Stage 5 identity proof;
10. repeated identical v0.2 receipt input canonicalizes/identifies deterministically under the existing identity layer;
11. Decision 024 and the complete deterministic suite remain green;
12. explicit compile remains green.

## Lane 03 attack surface

After Lane 02 publishes an exact tested Decision 025 head, Lane 03 should attack only this opened identity/chronology surface:

- logical-id or same-logical-id/different-exact packet substitution;
- wrong-kind exact base or packet refs;
- non-canonical exact spellings being accepted through fallback logic;
- duplicate packet membership being laundered by ordering/materialization;
- hidden current/newest/HEAD or actor authority entering identity resolution;
- an exact successor ref reappearing inside accepted v0.2 and recreating the reciprocal content-addressed cycle;
- historical v0.1 being silently treated as exact v0.2 evidence.

Do not open packet-acceptance execution, successor mutation, claim closure, partial-integration semantics, epochs/barriers, or replay in the same adversarial lane.

## Why Stage 5 mutation remains closed

Decision 024 answers whether one exact packet is inside a bounded acceptance-candidate slice. Decision 025 will answer whether the integration record can name the exact inputs and later be linked into a successor without impossible reciprocal hashing.

Those are prerequisites, not a mutating integration engine. After Decision 025 is implemented and independently checked, Lane 01 must perform another bounded Stage 5 entry audit. That later audit may open the smallest actual immutable transition or may identify one further exact prerequisite such as successor membership/claim-state semantics.

## Explicitly still unopened

This decision does not establish or authorize:

- packet acceptance/rejection execution;
- automatic root approval;
- successor state-revision publication runtime;
- claim closure or occupancy closure;
- partial integration semantics;
- mutable/global currentness;
- dependency admissibility/satisfaction/closure beyond existing facts;
- source trust/quality/relevance/completeness/closure;
- epochs/barriers;
- replay runtime or replay success;
- model autonomy;
- general hostile same-process isolation;
- cross-language reproduction.

## Root grounding

### Truth

Logical ids and generic strings do not identify the exact immutable inputs required to explain an integration transition. A reciprocal content-hash cycle also cannot be waved away by naming convention. The contract must state an exact, constructible chronology before mutation exists.

### Agency / non-domination

Exact identity and chronology are derived from stored relationships, not founder status, lane title, model confidence, schedule position, CI, branch ownership, or Git permission. Root-assessment fields remain explicit facts rather than hidden actor authority.

### Continuity

A replacement occupant must be able to reconstruct the transition as `successor -> receipt -> exact base/packets` from immutable stored identities. Historical v0.1 meaning remains preserved instead of being silently upgraded after the fact.

### Wisdom before speed

Fix the smallest impossible/ambiguous identity boundary before writing the mutating integration engine. Do not solve packet acceptance execution, claim closure, successor publication, epochs, and replay in the same change.

## Ownership

**Lane 02:** implement Decision 025 only, with versioned receipt identity/semantic validation and deterministic tests.

**Lane 03:** attack the exact tested Decision 025 surface only and preserve all failed/uncertain evidence.

**Lane 01:** integrate only after implementation and adversarial evidence are sufficiently grounded against the four roots, then perform the next bounded Stage 5 entry audit.
