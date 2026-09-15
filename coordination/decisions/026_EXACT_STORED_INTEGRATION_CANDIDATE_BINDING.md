# Decision 026 — Exact Stored Integration Candidate Binding Before Stage 5 Mutation

Date: 2026-09-15
Status: **accepted Stage 5 entry prerequisite; implementation open only for the bounded read-only candidate-binding preflight below. Canonical state mutation, receipt publication, successor publication, claim closure, epochs/barriers, replay, and model-heavy autonomy remain closed.**

## Why this decision exists

Decision 024 now provides a deterministic read-only eligibility fact for one exact return packet in the bounded created-output/no-dependency slice.

Decision 025 now provides exact immutable identity for an integration receipt's base revision and return-packet inputs, while preserving one-way publication chronology:

```text
exact base B + exact packet P
    -> exact receipt R
    -> future successor S
       with S.parent_revision_ref == B
       and S.integration_receipt_refs containing R
```

Those two facts are necessary but are not yet composed.

The current Decision 025 helper validates the spelling, kind, canonical identity, and deterministic receipt identity of `base_state_revision_ref` and `packet_refs[]`, but explicitly does **not** exact-load those referenced objects from durable storage. Separately, Decision 024 exact-loads and reconstructs one packet's Stage 4 context, but nothing yet proves that a proposed accepted receipt names the same exact packet/base pair that produced that eligibility fact.

Opening a mutating Stage 5 transition now would therefore require the mutation runtime itself to invent this binding step. That would mix input truth reconstruction with canonical publication.

## Single blocking fact named by the entry audit

> Before any accepted receipt may participate in successor-state construction, the institution needs one deterministic read-only fact proving that the receipt's exact base and packet input are present as exact verified stored objects and are the same exact single packet/base pair whose Decision 024 eligibility fact is being relied upon.

This decision opens only that fact.

## First candidate-binding slice

The first implementation is intentionally one-packet only. Multi-packet receipts remain valid Decision 025 objects, but packet aggregation/partial acceptance semantics are not yet grounded for mutation.

A proposed v0.2 receipt may report a **coherent Stage 5 acceptance candidate binding** only when all of the following are established:

1. **Decision 025 receipt identity is valid.**
   - validate the proposed v0.2 receipt through the canonical Decision 025 exact-identity path;
   - historical v0.1 remains readable historical data but is insufficient for this preflight;
   - exact base and packet references remain consequential immutable identities, not logical ids.

2. **The first mutation candidate slice contains exactly one packet.**
   - `packet_refs[]` contains exactly one exact return-packet ref;
   - zero packets is already invalid under the receipt schema;
   - two or more exact packets are reported as explicitly unsupported for this first candidate-binding slice, not silently aggregated or ordered.

3. **The exact base revision is materially present.**
   - load `base_state_revision_ref` through the existing immutable object-store exact-load path;
   - absence, wrong stored bytes, non-canonical bytes, wrong reproduced identity, wrong kind, or corruption must fail closed through existing typed store/identity behavior;
   - no mutable `current`, newest-object lookup, branch, schedule, or actor hint may substitute for the exact ref.

4. **The exact packet is materially present.**
   - load the single `packet_ref` through the same exact immutable store path;
   - same-logical-id/different-exact packet substitution must remain distinguishable;
   - a merely well-formed receipt reference is not proof that the packet bytes exist.

5. **Decision 024 is recomputed from that exact packet.**
   - call the canonical Decision 024 eligibility preflight using the exact stored packet ref;
   - do not copy, restate, or weaken Decision 024 evidence/provenance rules inside Decision 026;
   - preserve the complete Decision 024 result and reasons as evidence-bearing facts.

6. **Receipt/base/packet identity is coherent with the Decision 024 fact.**
   - the exact packet ref returned by Decision 024 equals the receipt's sole exact packet ref;
   - the exact base state revision ref returned by Decision 024 equals the receipt's exact base state revision ref;
   - mismatch is explicit non-readiness, not a fallback to logical id, recency, or receipt order.

7. **A non-eligible packet cannot become mutation-ready through receipt wording.**
   - only `eligible_for_stage5_acceptance_candidate` can satisfy the eligibility side of this binding;
   - unsupported/conflict/unsatisfied Decision 024 outcomes remain explicit and cannot be converted by `decision: accepted`, root-grounding prose, actor identity, or Git/CI state.

8. **A non-accepting receipt does not become a successor candidate.**
   - `rejected`, `deferred`, `repair_requested`, and the still-unopened state-creating use of `partially_integrated` must not produce an acceptance-candidate binding;
   - this is compatibility with Decision 001's already-canonical decision/result semantics, not a new acceptance policy.

9. **Root-grounding fields remain evidence-bearing claims, not hidden automatic constitutional authority.**
   - the v0.2 schema already requires every root assessment to be `grounded` for `decision: accepted` and requires no unresolved conflicts;
   - Decision 026 may expose those exact receipt facts but must not claim that parsing the word `grounded` independently proves the underlying constitutional reasoning;
   - constitutional merge standing still comes from grounded evidence against the four roots, never actor/founder/model/CI/Git authority.

## Required result meaning

Lane 02 may choose the exact Python representation, but the read-only result must preserve at least:

- exact proposed receipt immutable identity;
- exact base state revision ref;
- exact sole packet ref when inside the one-packet slice;
- whether the exact base materialized successfully;
- whether the exact packet materialized successfully;
- the complete nested Decision 024 eligibility fact for that exact packet;
- a deterministic candidate-binding outcome with bounded meanings equivalent to:
  - `coherent_stage5_acceptance_candidate_binding`;
  - `unsupported_multi_packet_receipt_slice`;
  - `receipt_packet_not_eligible`;
  - `receipt_base_mismatch`;
  - `non_accepting_receipt_decision`;
- deterministic reasons sufficient to reconstruct the disposition without exception text, actor identity, timestamps, branch state, CI state, or private chat.

Existing typed identity/store failures may propagate for malformed, absent, or corrupted exact objects rather than being collapsed into a new local vocabulary.

A positive candidate-binding result still does **not** mean the packet has been canonically accepted, the receipt has been published, a successor has been constructed, claims have been closed, an epoch has completed, replay succeeds, or root reasoning has been automatically approved.

## Reuse requirement

The implementation must compose existing canonical mechanisms instead of replacing them:

- Decision 025 exact receipt identity validation;
- `FilesystemObjectStore` exact loading/identity verification;
- Decision 024 packet integration eligibility.

Do not add a second immutable-ref parser, duplicate output/evidence/provenance policy, mutable current pointer, newest-object selection, logical-id fallback, actor preference, founder override, schedule precedence, CI authority, branch authority, or Git authority.

## Required implementation evidence

Lane 02 should implement only this read-only preflight and add deterministic regressions demonstrating at least:

1. one exact stored base + one exact stored eligible packet + coherent accepted v0.2 receipt produces the bounded positive binding;
2. a well-formed exact base ref whose object is absent fails closed through the store;
3. a well-formed exact packet ref whose object is absent fails closed through the store;
4. stored corruption / reproduced-identity mismatch cannot be laundered into readiness;
5. same-logical-id/different-exact base or packet substitution does not bind;
6. receipt base different from Decision 024's exact packet base is explicit non-readiness;
7. a Decision 024 non-eligible/unsupported packet cannot become ready through `decision: accepted`;
8. rejected/deferred/repair-requested receipts do not become successor candidates;
9. two or more exact packet refs are explicitly outside the first slice rather than being silently aggregated or first-item selected;
10. repeated identical exact stored inputs produce identical named facts;
11. no mutable current/HEAD, recency, array order, actor/founder identity, schedule, CI, branch, or Git permission participates;
12. Decision 024 and Decision 025 regressions remain green;
13. the complete deterministic suite and explicit compile remain green.

## Lane 03 attack surface

After Lane 02 publishes an exact tested head, Lane 03 should attack only this Decision 026 surface:

- well-formed-but-absent exact input refs being treated as material truth;
- same-logical-id/different-exact base or packet substitution;
- receipt/base mismatch being hidden by packet or receipt logical ids;
- multi-packet aggregation/order smuggling into the one-packet first slice;
- a non-eligible Decision 024 packet becoming ready because the receipt says `accepted`;
- non-accepting receipt decisions becoming successor candidates;
- mutable current/newest/HEAD, actor/founder identity, schedule, CI, branch, or Git permission entering the binding;
- exact-load failures being converted into stronger facts than the store established.

Do not jump to successor membership delta, receipt publication, state mutation, claim closure, epochs/barriers, replay, or general hostile-process isolation unless a new repository-visible decision opens that surface.

## Why Stage 5 mutation remains closed

Decision 025 fixed exact receipt input identity and acyclic publication chronology. Decision 026 now sequences the missing composition between that receipt identity and the exact stored packet/base facts already checked by Decision 024.

The next audit, after implementation and independent adversarial verification, can determine whether the first actual immutable successor construction is sufficiently specified or whether one exact successor-membership prerequisite remains.

## Root grounding

### Truth

A syntactically exact reference is not proof that its bytes are materially present, and two separately valid facts are not proof that they refer to the same transition. The candidate binding must make stored presence and exact cross-decision identity coherence explicit before mutation.

### Agency / non-domination

Receipt wording, founder status, specialist role, model identity, CI success, branch ownership, schedule position, or Git permission cannot turn an absent, mismatched, multi-packet-unsupported, or non-eligible input into a mutation candidate.

### Continuity

A replacement occupant can reconstruct the exact receipt/base/packet relation and the exact Decision 024 eligibility fact from immutable store/repository state without private chat convention or logical-id substitution.

### Wisdom before speed

Compose and verify the already-canonical read-only facts before opening writes. Keep the first candidate slice to one exact packet rather than simultaneously inventing packet aggregation, partial integration, successor membership, claim closure, epochs, and replay.

## Ownership

**Lane 02:** implement Decision 026 only, with deterministic tests and explicit compile evidence.

**Lane 03:** independently attack the exact tested Decision 026 head only and preserve red/uncertain evidence.

**Lane 01:** integrate only after implementation and adversarial evidence are sufficiently grounded against Truth, Agency/non-domination, Continuity, and Wisdom before speed; then perform the next bounded Stage 5 entry review.
