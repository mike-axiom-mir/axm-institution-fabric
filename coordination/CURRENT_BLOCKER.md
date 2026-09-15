# CURRENT BLOCKER — Institution Fabric

Status: **Decision 025 is canonical and independently verified on its bounded exact-receipt-identity surface. There is no active ADV-060 blocker. The single active Stage 5 entry gate is Decision 026: exact stored integration candidate binding between the canonical Decision 025 receipt identity and the canonical Decision 024 packet eligibility fact. Stage 5 mutation remains closed.**

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` is historical chronology and may describe an older active gate. Recency, filename, role, founder identity, CI state, mergeability, schedule position, or Git permission remain evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical main entering this gate

Decision 025 integration commit:

`0577282627d2b949bb3a695dfdd3affc288adf17` — `Integrate Decision 025 exact receipt identity`

Decision 025 is canonical only for:

- historical receipt v0.1 remaining readable but insufficient for exact Stage 5 proof;
- receipt v0.2 exact `base_state_revision_ref`;
- receipt v0.2 exact `packet_refs[]`;
- deterministic canonical receipt identity;
- one-way future chronology `successor -> receipt -> exact base/packets` with no reciprocal exact successor backlink inside receipt v0.2.

It does not exact-load those base/packet objects, perform packet acceptance, publish a receipt, build/publish a successor, close claims, complete an epoch, or prove replay.

## Decision 025 evidence accepted

### Lane 02 implementation

PR #165 exact semantic/test/workflow head:

`31c0ca484951f8a5e2d589f3788511bd1e1245cc`

Native evidence recorded by Lane 02:

- Decision 025 workflow run `34973946826`, job `104396805493`: **10/10 targeted tests passed**, Decision 024 regressions passed, complete deterministic discovery passed, explicit `py_compile` passed, broad `compileall` passed;
- protected identity workflow run `34973946700`, job `104396805213`: Decision 020/022/023 protected gates passed, complete deterministic discovery passed, compile passed.

Lane 02 explicitly preserved these limits: the Decision 025 helper validates exact refs but does not exact-load the referenced base/packet objects; the one-way successor test proves contract compatibility only, not successor construction/publication.

### Lane 03 independent verification

PR #166 re-anchored exactly on Lane 02 semantic head `31c0ca...`.

Verification test/workflow head:

`efdbb02e6ab2d7dc401963835985c909ad89d261`

Native independent run/job:

- run `34975820287`;
- job `104403144701`;
- Decision 025 adversarial cases: **7/7 passed**;
- Lane 02 Decision 025 baseline: **10/10 passed**;
- Decision 024 continuity regression: **17/17 passed**;
- complete deterministic discovery: **502/502 passed**;
- explicit `py_compile`: **passed**;
- broad deterministic `compileall`: **passed**.

Lane 03 reproduced no concrete adjacent contradiction on the opened Decision 025 identity/chronology surface. Its return packet independently preserves the same next uncertainty: exact referenced base/packet material has not yet been bound through durable exact loading to the packet eligibility fact, and successor construction/publication remains untested.

PR #166 is verification evidence for an already-integrated prerequisite and should not replay its one-off workflow into `main`. It may be closed without merge as superseded, not invalidated, after this canonical handoff is merged.

## Fresh Stage 5 entry audit

The audit compared canonical Decisions 024 and 025 against the current object-store and state-revision boundaries.

Observed canonical facts:

1. `FilesystemObjectStore.load(...)` already provides exact material loading that verifies stored canonical bytes reproduce the requested immutable identity.
2. Decision 024 already reconstructs one exact packet from the store and returns its exact `packet_ref` and exact `base_state_revision_ref` with bounded eligibility reasons.
3. Decision 025 validates receipt v0.2 exact reference syntax/kind/canonical spelling and deterministic receipt identity, but explicitly does **not** exact-load the referenced base/packet objects.
4. Nothing canonical yet composes those mechanisms into one fact proving that a proposed accepted receipt names the exact materially present single packet/base pair whose Decision 024 eligibility is being relied upon.
5. Receipt v0.2 permits multiple exact packet refs, while Decision 024 eligibility is packet-local. No aggregation/partial-acceptance rule is canonical yet.

Therefore opening successor mutation directly would make the mutating runtime invent input-materialization, cross-decision binding, and possibly multi-packet aggregation policy in the same step that publishes canonical state.

## Active gate — Decision 026

Decision file:

`coordination/decisions/026_EXACT_STORED_INTEGRATION_CANDIDATE_BINDING.md`

The opened read-only contract is deliberately narrow:

1. validate a proposed v0.2 receipt through Decision 025;
2. first mutation-candidate slice supports exactly one exact packet ref;
3. exact-load the receipt's base revision and packet through the existing immutable store;
4. recompute canonical Decision 024 eligibility from that exact stored packet;
5. require exact packet identity equality between receipt and eligibility fact;
6. require exact base identity equality between receipt and eligibility fact;
7. a non-eligible/unsupported Decision 024 packet cannot become ready because receipt wording says `accepted`;
8. rejected/deferred/repair-requested receipts cannot become successor candidates;
9. root-grounding strings remain evidence-bearing receipt facts, not automatic constitutional proof;
10. return a deterministic named candidate-binding fact only; perform no writes.

A positive `coherent_stage5_acceptance_candidate_binding` still means only that the exact stored input relation is coherent for the first bounded Stage 5 slice. It is not canonical acceptance, receipt publication, successor construction/publication, claim closure, epoch completion, replay success, or automatic root approval.

## Specialist coordination

### Lane 02 — next executable lane

Implement **Decision 026 only**.

Required evidence includes:

- one exact stored base + one exact stored eligible packet + coherent accepted v0.2 receipt produces the bounded positive binding;
- absent exact base or packet fails through the canonical store;
- corrupt/reproduced-identity-mismatched stored material fails closed;
- same-logical-id/different-exact substitutions do not bind;
- receipt base vs Decision 024 exact packet base mismatch is explicit non-readiness;
- Decision 024 non-eligible/unsupported outcome cannot be laundered into readiness by receipt wording;
- non-accepting receipt decisions do not become successor candidates;
- multiple packet refs are explicitly outside the first slice and are not silently aggregated or first-item selected;
- deterministic repeated inputs produce identical named facts;
- Decision 024 and Decision 025 regressions stay green;
- complete deterministic suite and explicit compile stay green.

Do not implement receipt publication, successor mutation/publication, claim/occupancy closure, partial-integration aggregation, epochs/barriers, replay, mutable currentness, or model autonomy.

### Lane 03

After Lane 02 publishes an exact tested Decision 026 head, independently attack only:

- well-formed-but-absent refs being treated as material truth;
- same-logical/different-exact base or packet substitution;
- receipt/base mismatch hidden by logical ids;
- multi-packet aggregation/order smuggling;
- non-eligible packets becoming ready because receipt says `accepted`;
- non-accepting receipt decisions becoming successor candidates;
- hidden current/newest/HEAD, actor/founder, schedule, CI, branch, or Git authority;
- exact-load failures being converted into stronger facts than the store established.

Do not widen into successor membership/state mutation/replay without a new repository-visible decision.

### Lane 01

Do not open a mutating integration engine yet.

After Lane 02 implements Decision 026 and Lane 03 independently checks that exact tested ancestry, perform a fresh review under:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

If grounded, integrate Decision 026 and perform the next narrow Stage 5 entry audit. That next audit may open the first actual immutable successor construction or identify exactly one remaining successor-membership prerequisite.

## Stage 5 boundaries still closed

Decision 026 does not solve or authorize:

- automatic constitutional/root approval;
- receipt publication;
- successor state-revision construction/publication;
- canonical packet acceptance/rejection execution;
- claim closure or occupancy closure;
- multi-packet aggregation or partial-integration runtime semantics;
- epochs/barriers;
- replay runtime or replay success;
- dependency admissibility/satisfaction/closure outside Decision 024's empty-dependency first slice;
- source trust, quality, relevance, completeness, or closure;
- mutable/global currentness;
- model autonomy;
- general hostile same-process isolation;
- full cross-language reproduction.

## Root grounding of this gate

### Truth

Exact reference syntax is not material presence, and separately valid Decision 024/025 facts are not yet a proven same-transition binding. Decision 026 makes that missing relation explicit before writes.

### Agency / non-domination

Receipt wording, founder status, lane identity, model capability, CI success, branch ownership, schedule position, or Git permission cannot substitute for exact stored inputs or turn a non-eligible packet into a mutation candidate.

### Continuity

A replacement occupant should be able to reconstruct the proposed transition from exact receipt/base/packet identity plus the exact Decision 024 fact, without private chat or logical-id substitution.

### Wisdom before speed

Compose the canonical read-only facts before opening mutation. Keep the first candidate slice to one packet rather than inventing packet aggregation, successor membership, claim closure, epochs, and replay simultaneously.

## Current v0 position

Institution Fabric remains **Stage 4 at the Stage 5 boundary**, but receipt identity/chronology is now canonical and the next pre-mutation binding requirement is explicit.

## Best next action

**Lane 02 implements Decision 026 exact stored integration candidate binding only, with deterministic tests and explicit compile evidence.**
