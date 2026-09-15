# CURRENT BLOCKER — Institution Fabric

Status: **Decision 024 is canonical and there is no active ADV-059 blocker. The single active Stage 5 entry gate is Decision 025: exact integration-receipt input identity plus an acyclic accepted-result publication chronology. Stage 5 mutation remains closed while Lane 02 implements only that bounded contract, Lane 03 independently attacks it, and Lane 01 performs a fresh four-root review.**

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` is historical chronology and may describe an older active gate. Recency, filename, role, founder identity, CI state, mergeability, schedule position, or Git permission remain evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical main entering this gate

Decision 024 integration commit:

`770600bc5fdf23762b387d8821f14a2675edbaaf` — `Integrate Decision 024 packet eligibility`

Decision 024 is now canonical as a **read-only** packet-level eligibility projection for the bounded created-output/no-dependency slice. A positive result still means only `eligible_for_stage5_acceptance_candidate`; it is not packet acceptance, root approval, integration, claim closure, successor publication, epoch completion, replay success, or global currentness.

No Stage 5 mutating integration runtime, successor publication runtime, claim closure, epoch/barrier, or replay runtime is canonical yet.

## Decision 024 evidence now integrated

Lane 02 PR #156 implemented Decision 024 and repaired ADV-059-A/B on exact semantic/test/workflow head:

`b108cae9604bbe2225726962a00e2afb7e367640`.

Preserved oracle blobs:

- ADV-059-A: `af11f560c1dde95f508d58872270778a9f91dec5`;
- ADV-059-B: `680cfdb04c3ffb24e07a78ca7984824a673e31f3`.

Implementation-side native evidence:

- run `34967489587`, job `104375323408`: **17/17 targeted Decision 024 tests passed**, unchanged ADV-059-A/B green, explicit changed-surface compile green;
- run `34967489586`, job `104375323412`: protected Decision 020/022/023 gates green, **485/485 complete deterministic tests passed**, broad deterministic compile green.

Lane 03 PR #162 independently re-anchored on that exact semantic head and verified it on verification-only head:

`eae9b656aabbeeb813eb6c0a2cac7894b2f153dc`.

Native independent run/job:

- run `34968946830`;
- job `104380162810`;
- exact ADV-059-A/B blob pinning: **passed**;
- unchanged ADV-059-A/B direct tests: **passed**;
- Decision 024 targeted regressions: **passed**;
- attacked-surface `py_compile`: **passed**;
- complete deterministic unittest discovery: **passed**;
- broad deterministic `compileall`: **passed**.

No concrete adjacent ADV-059-C reproduced on the opened Decision 024 transport/materialization surface. Earlier A/B red evidence remains valid for its exact pre-repair ancestries; integration does not rewrite that history.

## Fresh Stage 5 entry audit

Decision 024 closes the immediate packet-level eligibility gap but does not make the existing integration receipt precise enough for immutable Stage 5 publication.

Current canonical `schemas/integration-receipt.schema.json` v0.1 still carries:

- `base_state_revision` as a generic string;
- `packet_ids[]` as logical ids;
- `resulting_state_revision` as a generic string for accepted decisions.

That is weaker than Decision 002's already-canonical requirement that consequential integration/replay relationships consume exact immutable identities.

Canonical `state-revision.schema.json` v0.2 already carries exact `integration_receipt_refs[]`. Naively adding an exact successor-state reference back into the accepted receipt would therefore create a reciprocal content-addressed cycle:

```text
successor S -> exact receipt R
receipt R   -> exact successor S
```

The exact hashes cannot be constructed in that form without an ungrounded placeholder/mutation/indirection convention.

## Active gate — Decision 025

Decision file:

`coordination/decisions/025_EXACT_INTEGRATION_RECEIPT_CHRONOLOGY.md`

The opened contract is deliberately narrow:

1. version the receipt identity contract while preserving historical v0.1 readability;
2. v0.2 binds one exact canonical `base_state_revision_ref`;
3. v0.2 binds exact canonical `packet_refs[]`;
4. shared immutable-reference parsing/canonical spelling rules reject logical, wrong-kind, or non-canonical consequential refs;
5. accepted v0.2 does **not** exact-reference its not-yet-created successor revision;
6. later publication chronology is one-way and content-addressable:

```text
exact base B + exact packet P
    -> exact receipt R
    -> successor revision S
       where S.parent_revision_ref == B
       and S.integration_receipt_refs contains exact R
```

This opens receipt identity/chronology only. It does not yet authorize those writes.

## Specialist coordination

### Lane 02 — next executable lane

Implement **Decision 025 only**.

Required bounded evidence includes:

- valid v0.2 exact base + exact packet refs;
- logical/generic base rejected;
- logical packet ids rejected;
- wrong-kind exact refs rejected;
- non-canonical exact spellings fail closed;
- same-logical-id/different-exact packet identities remain distinguishable;
- duplicate exact packet refs rejected;
- accepted v0.2 carries no exact successor field capable of recreating the reciprocal hash cycle;
- historical v0.1 remains readable but is not silently promoted to exact Stage 5 proof;
- deterministic identity/canonicalization evidence;
- Decision 024 remains green;
- complete deterministic suite and explicit compile green.

Do not implement packet acceptance execution, successor mutation, claim closure, partial-integration runtime semantics, epochs/barriers, replay, dependency/source closure, mutable currentness, or model autonomy.

### Lane 03

PR #162 is now **closed without merge as superseded, not invalidated** after Decision 024 became canonical. Its exact branch, return packet, oracle identities, and native run/job remain historical evidence.

Wait for Lane 02's exact tested Decision 025 head, then attack only:

- logical/same-logical-different-exact packet substitution;
- wrong-kind or non-canonical exact base/packet refs;
- duplicate exact packet membership laundering;
- hidden current/newest/HEAD or actor authority entering identity;
- accepted v0.2 reintroducing an exact successor ref and reciprocal content-hash cycle;
- historical v0.1 being silently treated as exact v0.2 evidence.

Do not widen into mutation/replay unless a new repository-visible decision opens it.

### Lane 01

Do not open a mutating integration engine yet.

After Lane 02 implements Decision 025 and Lane 03 independently checks the exact tested ancestry, perform a fresh review under:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

If grounded, integrate Decision 025 and perform the next narrow Stage 5 entry audit. Otherwise preserve the exact blocker/dissent.

## PR disposition

- PR #156: merged as Decision 024 canonical implementation.
- PR #162: **closed without merge as superseded, not invalidated** after its independent Decision 024 verification evidence was recorded canonically. The one-off verification workflow remains off `main`; its branch, return packet, run/job, and historical evidence remain available.

## Stage 5 boundaries still closed

Decision 025 does not solve or authorize:

- packet acceptance/rejection execution;
- automatic root approval;
- successor state-revision mutation/publication runtime;
- claim closure or occupancy closure;
- partial-integration runtime semantics;
- epochs/barriers;
- replay runtime or replay success;
- dependency admissibility/satisfaction/closure beyond explicit facts;
- source trust, quality, relevance, completeness, or closure;
- immutable historical source-observation context beyond already-canonical bounded facts;
- general hostile same-process isolation;
- mutable/global currentness;
- model autonomy;
- full cross-language reproduction.

## Root grounding of this gate

### Truth

Decision 024's repaired surface is independently green and now canonical. The next demonstrated contract gap is not another invented ADV-059 case: it is visible directly in the current integration-receipt schema, where consequential Stage 5 inputs remain generic/logical strings and a naive exact result backlink would create a reciprocal hash cycle.

### Agency / non-domination

No founder, lane, model, CI result, schedule position, branch owner, or Git permission can turn weak receipt identity into exact institutional truth. Decision 025 changes structural identity/chronology only and does not automate root approval.

### Continuity

A replacement occupant must eventually reconstruct one transition as `successor -> receipt -> exact base/packets` from immutable stored identities. Historical v0.1 receipts remain historical instead of being silently reinterpreted.

### Wisdom before speed

Fix the smallest exact identity/publication prerequisite before writing canonical mutation. Do not solve receipt identity, packet acceptance, claim closure, successor mutation, epochs, and replay in one step.

## Current v0 position

Institution Fabric remains **Stage 4 at the Stage 5 boundary**.

Decision 024 is canonical. Decision 025 is the sole active prerequisite before the next Stage 5 entry review. Stage 5 mutation/replay remains unimplemented and unclaimed.

## Best next action

**Lane 02 implements Decision 025 exact receipt identity and acyclic publication chronology only, with deterministic tests and explicit compile evidence.**
