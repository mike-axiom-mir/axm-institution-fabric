# CURRENT BLOCKER — Institution Fabric

Status: **Decision 025 is canonical. The single active Stage 5 entry gate is Decision 026: exact accepted-receipt operational re-grounding before successor publication. Stage 5 mutation remains closed while Lane 02 implements only that read-only preflight, Lane 03 independently attacks it, and Lane 01 performs a fresh four-root review.**

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` is historical chronology and may describe an older active gate. Recency, filename, role, founder identity, CI state, mergeability, schedule position, or Git permission remain evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical main entering this gate

Decision 025 integration commit:

`0577282627d2b949bb3a695dfdd3affc288adf17` — `Integrate Decision 025 exact receipt identity`

Decision 025 is now canonical as a **versioned exact integration-receipt input identity and acyclic publication chronology contract**. Historical v0.1 remains readable but insufficient for exact Stage 5 proof. V0.2 exact-binds `base_state_revision_ref` and exact `packet_refs[]`, and intentionally carries no exact successor-state reference.

No Stage 5 successor mutation/publication runtime, claim closure, epoch/barrier, or replay runtime is canonical yet.

## Decision 025 evidence now integrated

Lane 02 PR #165 implemented Decision 025 on exact semantic/test/workflow head:

`31c0ca484951f8a5e2d589f3788511bd1e1245cc`.

Its later head `388d6ea8f6a5ef446257b05fff3a08bccd047583` adds only the durable Lane 02 return packet; comparison against the tested semantic head shows no production/schema/test/workflow change after testing.

Implementation-side native evidence:

- `decision025-receipt-identity` run `34973946826`: **completed / success**;
- `identity-stage2` run `34973946700`: **completed / success**;
- Decision 025 targeted tests, Decision 024 continuity, complete deterministic discovery, explicit Decision 025 compile, and broad compile all succeeded on the exact tested head.

Lane 03 PR #166 independently anchored on that exact Lane 02 tested head and verified it on exact adversarial test/workflow head:

`efdbb02e6ab2d7dc401963835985c909ad89d261`.

Native independent run:

- `decision025-lane03-adversarial` run `34975820287`: **completed / success**;
- Lane 03 bounded adversarial checks: **7/7 passed**;
- unchanged Lane 02 Decision 025 baseline: **10/10 passed**;
- Decision 024 continuity regressions: **17/17 passed**;
- complete deterministic discovery: **502/502 passed**;
- explicit attacked-surface compile and broad compile passed.

No concrete adjacent contradiction reproduced on the opened Decision 025 surface. No new ADV case was invented merely to keep the chain moving.

## Fresh four-root review of Decision 025

### Truth — grounded for the bounded contract

V0.2 exact receipt inputs use the shared immutable-reference parser, reject logical/wrong-kind/non-canonical/duplicate exact refs, preserve same-logical/different-exact identity, keep v0.1 historical rather than silently upgrading it, and make no mutation/replay claim.

### Agency / non-domination — grounded

Founder identity, lane identity, CI, branch ownership, schedule position, or Git permission does not participate in receipt identity or supply constitutional authority. Root-assessment fields remain explicit decision facts rather than hidden actor authority.

### Continuity — grounded

A replacement occupant can reconstruct the exact base/packet identities named by v0.2 from repository-visible immutable facts. Accepted v0.2 avoids the reciprocal content-addressed `receipt <-> successor` cycle; the later successor may exact-reference the receipt instead.

### Wisdom before speed — grounded

Decision 025 stops at exact receipt identity/chronology. It does not open successor mutation, claim closure, multi-packet conflict policy, epochs, replay, currentness, or model autonomy.

PR #165 was therefore squash-merged as canonical Decision 025.

## Fresh Stage 5 entry audit

Decision 025 solves exact receipt input identity, but its helper intentionally does **not** exact-load the referenced base revision or packet objects and does **not** rerun Decision 024 packet eligibility.

That leaves one smaller prerequisite before a mutating successor transition can be opened:

> A future Stage 5 operation must prove that the exact accepted receipt instance, exact base revision, and exact packet instance it is about to use are the durable objects actually present in the immutable store, and that the packet still satisfies canonical Decision 024 eligibility against the same exact base.

A syntactically exact receipt reference alone is not proof that the referenced material is present, uncorrupted, or operationally compatible.

## Active gate — Decision 026

Decision file:

`coordination/decisions/026_EXACT_ACCEPTED_RECEIPT_PREFLIGHT.md`

The opened contract is deliberately read-only and narrow:

1. accept one exact immutable `integration-receipt` ref;
2. exact-load that receipt and require v0.2;
3. consume `decision == accepted` only as a recorded input fact, not constitutional authority;
4. exact-load the receipt's exact base revision;
5. support **exactly one** packet ref in the first operational Stage 5 slice;
6. exact-load that packet and rerun canonical Decision 024 eligibility;
7. require `eligible_for_stage5_acceptance_candidate`;
8. require the packet's exact Decision 024 base to equal the receipt's exact base;
9. return only a deterministic named publication-candidate fact;
10. perform **no mutation**.

Multi-packet v0.2 receipts remain valid structural objects but are explicitly unsupported by this first operational preflight so the kernel does not invent packet ordering, conflict resolution, partial integration, or epoch semantics.

## Specialist coordination

### Lane 02 — next executable lane

Implement **Decision 026 only**.

Required bounded evidence includes:

- exact stored v0.2 accepted receipt + exact base + one exact Decision 024 eligible packet passes;
- missing/corrupt exact receipt fails closed;
- v0.1 cannot pass;
- non-accepted receipt cannot drive successor-publication candidacy;
- missing/corrupt exact base fails closed;
- same-logical/different-exact base substitution fails;
- missing/corrupt exact packet fails closed;
- same-logical/different-exact packet substitution fails;
- non-eligible Decision 024 packet fails;
- receipt-base / packet-base mismatch fails;
- multi-packet receipt is explicitly unsupported rather than partially selected;
- no current/newest/HEAD/actor/branch/schedule/CI/Git authority enters selection;
- repeated identical inputs produce the same named result;
- Decision 024 and Decision 025 remain green;
- complete deterministic suite and explicit compile green.

Do not implement successor state-revision mutation/publication, claim/occupancy closure, modified-output integration, dependency-bearing output integration, multi-packet conflict semantics, partial integration, epochs/barriers, replay, mutable currentness, or model autonomy.

### Lane 03

PR #166 is independent Decision 025 verification evidence for an already-integrated prerequisite. Preserve its branch, exact tested head, native run, and return packet, then close it without merge as **superseded, not invalidated** once its durable packet is copied to canonical coordination state.

Wait for Lane 02's exact tested Decision 026 head, then attack only the opened re-grounding surface:

- exact receipt substitution;
- same-logical/different-exact base or packet substitution;
- missing/corrupt exact receipt/base/packet material;
- stale/caller-authored eligibility trying to bypass a fresh Decision 024 run;
- receipt base vs packet base mismatch;
- multi-packet ordering/partial-selection laundering;
- hidden current/newest/HEAD or actor/branch/schedule/CI/Git authority;
- v0.1 promotion;
- named result materialization losing exact identity.

Do not widen into successor mutation/replay unless a new repository-visible decision opens it.

### Lane 01

Do not open a mutating integration engine yet.

After Lane 02 implements Decision 026 and Lane 03 independently checks the exact tested ancestry, perform a fresh review under:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

If grounded, integrate Decision 026 and perform the next narrow Stage 5 entry audit. Otherwise preserve the exact blocker/dissent.

## PR disposition

- PR #165: merged as Decision 025 canonical implementation.
- PR #166: independent Decision 025 verification evidence; close without merge as superseded, not invalidated after canonical preservation of its return packet/evidence pointers.

## Stage 5 boundaries still closed

Decision 026 does not solve or authorize:

- automatic root approval;
- successor state-revision construction/storage/publication;
- state-revision member-set mutation semantics;
- claim or occupancy closure/status replacement;
- modified-output integration;
- dependency-bearing output integration;
- multi-packet integration/conflict resolution;
- partial integration runtime semantics;
- mutable/global currentness;
- epochs/barriers;
- replay runtime or replay success;
- source/dependency closure beyond already-canonical bounded facts;
- general hostile same-process isolation;
- model autonomy;
- full cross-language reproduction.

## Root grounding of this gate

### Truth

Decision 025 proves exact receipt reference identity, not presence/correctness of the referenced durable objects at operational use. Before mutation, exact-load and freshly re-run the already-canonical eligibility proof on the exact packet.

### Agency / non-domination

No actor category or execution permission substitutes for exact stored relationships or root review. `accepted` is consumed as a recorded decision fact, not as automatic constitutional authority.

### Continuity

A replacement occupant can reconstruct one future publication candidate from `exact receipt -> exact base + exact packet -> fresh Decision 024 eligibility` without private chat or a stale caller cache.

### Wisdom before speed

Compose proven exact-load and eligibility primitives before adding writes. Keep successor mutation, claim closure, epochs, and replay closed until this operational read boundary is independently green.

## Current v0 position

Institution Fabric remains **Stage 4 at the Stage 5 boundary**.

Decision 025 is canonical. Decision 026 is the sole active prerequisite before the next Stage 5 entry review. The first canonical mutating integration transition is still unimplemented and unclaimed.

## Best next action

**Lane 02 implements Decision 026 exact accepted-receipt operational preflight only, with deterministic tests and explicit compile evidence.**
