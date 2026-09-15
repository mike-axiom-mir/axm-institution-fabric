# Decision 026 — Exact Accepted-Receipt Operational Re-grounding Before Successor Publication

Date: 2026-09-15
Status: **accepted Stage 5 entry prerequisite; implementation open only for one read-only exact accepted-receipt operational preflight. Successor mutation/publication, claim closure, epochs/barriers, replay, and model autonomy remain closed.**

## Why this decision exists

Decision 025 is now canonical. Integration-receipt v0.2 can name an exact immutable base state revision and exact immutable return-packet instance(s), while avoiding the reciprocal content-addressed cycle between receipt and successor revision.

That solves identity and publication direction, but it does not yet prove that a future Stage 5 operation is using the exact stored objects named by the receipt.

The current Decision 025 helper validates a receipt mapping and its exact-reference syntax. It deliberately does **not** exact-load the referenced base revision or packets, does not rerun Decision 024 packet eligibility, and does not publish a successor.

The current object store already has exact immutable load semantics, and Decision 024 already has a read-only eligibility preflight that reconstructs an exact packet's base/claim/lane/output/evidence/provenance facts.

Before the first mutating integration transition is opened, those existing facts must be composed once at the receipt boundary so a successor cannot be published from a structurally valid receipt whose exact referenced base/packet material is absent, corrupt, mismatched, or outside the currently supported Decision 024 acceptance-candidate slice.

## Single blocking fact named by this audit

> Before Stage 5 successor publication may be implemented, the exact accepted v0.2 receipt instance used for that transition must be re-grounded against the exact stored base revision and exact stored packet instance, and the packet must still satisfy the canonical Decision 024 first-slice eligibility preflight against that same exact base.

This is the only prerequisite opened by this decision.

## Required bounded preflight

Lane 02 should implement one read-only preflight equivalent to:

```text
exact integration-receipt ref R
    -> exact-load R as integration-receipt v0.2
    -> validate Decision 025 exact input identity
    -> require R.decision == accepted as an input fact
    -> exact-load R.base_state_revision_ref == B
    -> require exactly one packet ref in this first Stage 5 slice
    -> exact-load packet P
    -> rerun Decision 024 eligibility for P
    -> require eligibility outcome == eligible_for_stage5_acceptance_candidate
    -> require eligibility.base_state_revision_ref == B
    -> return a named, deterministic, read-only publication-candidate fact
```

The output may establish only something like `eligible_for_successor_publication_candidate` for this exact receipt/base/packet triple.

It is **not** successor publication, packet acceptance authority, root approval, claim closure, epoch completion, replay success, or global currentness.

## Why exactly one packet in the first slice

Integration-receipt v0.2 correctly allows one-or-more exact `packet_refs[]` for future integration shapes.

The first actual Stage 5 slice should fail closed on `len(packet_refs) != 1` rather than inventing multi-packet conflict resolution, packet ordering, partial-integration policy, epoch/barrier semantics, or cross-packet dependency policy before those are grounded.

This does not invalidate multi-packet receipts as historical/structural objects. It only marks them **unsupported by the first operational publication preflight**.

## Required semantics

1. **Exact receipt identity is operationally used.**
   - the preflight accepts an exact immutable `integration-receipt` reference, not a loose mapping or logical receipt id;
   - the receipt is exact-loaded through the immutable store;
   - a missing, corrupt, wrong-kind, or non-canonical receipt fails closed.

2. **Historical v0.1 is not promoted.**
   - v0.1 remains readable historical data;
   - it cannot pass the Decision 026 exact accepted-receipt preflight.

3. **Accepted is a recorded decision fact, not constitutional authority.**
   - the preflight may require `decision == "accepted"` because rejected/deferred/repair records cannot drive successor publication;
   - this check does not convert receipt text, root-assessment strings, CI, Git permission, actor identity, or schedule position into the constitutional merge gate;
   - the four roots remain the gate for canonical AXM integration decisions.

4. **Exact base is present and usable.**
   - `base_state_revision_ref` must exact-load successfully as the immutable state revision named by the receipt;
   - no newest/current/HEAD lookup or logical-id fallback is permitted.

5. **One exact packet is present and still eligible.**
   - the first operational slice supports exactly one exact `return-packet` ref;
   - that packet must exact-load successfully;
   - Decision 024 eligibility is rerun from the exact stored packet rather than trusting a stale or caller-authored cached eligibility label;
   - the resulting exact packet base must equal the receipt's exact base.

6. **No mutation.**
   - the preflight does not store a successor revision;
   - it does not rewrite claim or occupancy status;
   - it does not add artifacts/evidence/packet/receipt membership to a new revision;
   - it does not update a mutable current pointer;
   - it does not implement replay.

7. **Named deterministic output.**
   - return a self-describing immutable/frozen result containing at least exact receipt ref, exact base ref, exact packet ref, exact created-output refs, exact relevant evidence facts already exposed by Decision 024, and a bounded publication-candidate outcome;
   - ordinary supported materialization must not silently degrade named institutional facts into positional meaning.

## Required implementation evidence

Lane 02 should add deterministic regressions demonstrating at least:

1. exact stored v0.2 accepted receipt + exact stored base + one exact Decision 024 eligible packet passes;
2. exact receipt ref missing from the store fails closed;
3. corrupt exact receipt bytes fail closed;
4. historical v0.1 cannot pass the operational preflight;
5. rejected/deferred/repair-requested receipt cannot drive successor-publication candidacy;
6. exact base ref missing/corrupt fails closed;
7. logical/same-logical-different-exact base substitution cannot replace the receipt's exact base;
8. exact packet ref missing/corrupt fails closed;
9. same-logical-id/different-exact packet substitution cannot replace the receipt's exact packet;
10. packet whose Decision 024 outcome is non-eligible cannot pass;
11. packet whose exact Decision 024 base differs from the receipt exact base cannot pass;
12. multi-packet receipt is explicitly unsupported by this first operational slice rather than partially or order-dependently interpreted;
13. no current/HEAD/actor/branch/schedule authority participates;
14. repeated identical stored inputs yield the same named preflight result;
15. Decision 024 and Decision 025 regressions remain green;
16. complete deterministic suite and explicit compile remain green.

## Lane 03 attack surface

After Lane 02 publishes one exact tested Decision 026 head, Lane 03 should attack only this operational re-grounding surface:

- exact receipt substitution;
- same-logical/different-exact base or packet substitution;
- missing/corrupt exact receipt/base/packet material;
- cached/caller-authored eligibility trying to bypass a fresh Decision 024 preflight;
- receipt base vs packet exact base mismatch;
- multi-packet ordering/partial-selection laundering;
- hidden current/newest/HEAD, actor, branch, schedule, CI, or Git authority entering selection;
- v0.1 promotion;
- named-result materialization losing exact identity.

Do not widen into successor mutation, claim closure, epochs/barriers, replay, or general hostile-process isolation unless a new repository-visible decision opens them.

## Why this remains smaller than mutation

Decision 025 made the receipt capable of naming exact inputs. Decision 026 makes a future mutation operation prove that those exact named inputs are the durable objects actually being used and that the packet still lies inside the already-canonical Decision 024 acceptance-candidate slice.

Only after that read-only boundary is independently verified should Lane 01 decide whether the smallest actual successor-state transition can be opened.

## Explicitly still unopened

Decision 026 does not establish or authorize:

- automatic constitutional root approval;
- packet acceptance policy beyond consuming an existing `accepted` receipt fact;
- successor state-revision construction or storage;
- state-revision member-set mutation rules;
- claim/occupancy closure or status replacement;
- modified-output integration;
- dependency-bearing output integration;
- multi-packet integration/conflict resolution;
- partial integration semantics;
- mutable/global currentness;
- epochs/barriers;
- replay runtime or replay success;
- source/dependency closure beyond already-canonical facts;
- model autonomy;
- full cross-language reproduction.

## Root grounding

### Truth

A syntactically exact reference is not proof that the referenced immutable object is present, uncorrupted, or the same exact object whose packet eligibility was grounded. Re-ground the exact receipt/base/packet at operational use before mutation exists.

### Agency / non-domination

The preflight consumes stored exact relationships only. No founder, lane, actor, model, CI result, schedule position, branch, or Git permission may substitute for exact object identity or constitutional review.

### Continuity

A replacement occupant can reconstruct the future publication candidate from `exact receipt -> exact base + exact packet -> fresh Decision 024 eligibility` without hidden chat state or a stale caller-provided eligibility cache.

### Wisdom before speed

Compose the already-proven exact-load and eligibility primitives once before adding writes. Do not combine receipt re-grounding, successor mutation, claim closure, epochs, and replay in one change.

## Ownership

**Lane 02:** implement Decision 026 read-only exact accepted-receipt operational preflight only, with deterministic tests and explicit compile evidence.

**Lane 03:** attack the exact tested Decision 026 surface only and preserve failed/uncertain evidence.

**Lane 01:** integrate only after implementation and independent evidence are sufficiently grounded against the four roots, then perform the next bounded Stage 5 entry audit.
