# Decision 024 — Minimal Packet Integration Eligibility Before Stage 5

Date: 2026-09-15
Status: **accepted Stage 5 entry prerequisite; implementation open only for the bounded read-only eligibility projection below. Stage 5 state mutation, integration receipts, successor publication, claim closure, epochs, and replay remain closed.**

## Why this decision exists

The bounded Stage 4 -> Stage 5 entry audit finds one immediate missing deterministic fact.

The current kernel can reconstruct one exact return packet, its exact claim/base/occupancy/lane context, exact created and modified output identities, exact subject-bound evidence, bounded lane/output compatibility, exact work-base provenance, and several dependency/source facts. Those are component facts.

They do **not** currently produce a packet-level fact saying that one exact packet is inside a sufficiently grounded acceptance candidate slice. `ResolvedMixedPacketCompatibility` deliberately exposes no packet-level `accepted`, `complete`, `closed`, or aggregate `satisfied` field. That boundary is correct: Stage 4 has not yet defined packet acceptance.

Opening a mutating Stage 5 engine now would therefore require the integration runtime to invent packet acceptance policy while it is also publishing canonical state. That would collapse fact collection and authority into one hidden step.

The smallest truthful next move is a read-only, deliberately narrow **integration eligibility** projection. It answers only whether one exact packet is inside the first currently-grounded acceptance candidate slice. It does not accept the packet and does not create state.

## Single blocking fact named by the entry audit

> Before Stage 5 may mutate canonical state, the institution needs one deterministic packet-level eligibility fact that composes already-canonical Stage 4 facts without inventing dependency admissibility, evidence precedence, source trust/closure, global currentness, claim closure, or actor authority.

This is the only prerequisite opened by this decision.

Known later Stage 5 obligations such as ADV-002-G/H exact integration-receipt base/result/packet identity remain preserved but are **not** opened in the same lane. They will be sequenced only after this eligibility fact is implemented and adversarially checked.

## First eligible slice

The first implementation is intentionally narrower than all valid return packets.

A packet may report `eligible_for_stage5_acceptance_candidate = true` only when all of the following are grounded from exact stored state:

1. **Exact packet/lifecycle context is reconstructed.**
   - `packet_ref` is one exact immutable `return-packet` instance.
   - the packet's exact base equals the exact claim base;
   - the exact claim-base lane and exact occupancy historical lane relation reconstruct successfully;
   - the local exact claim snapshot is `open` and the local exact occupancy snapshot is `active` under the already-canonical Stage 4 rules;
   - this does not establish mutable/global currentness.

2. **The first slice is created-output only.**
   - `artifacts_created[]` contains at least one exact artifact ref;
   - `artifacts_modified[]` is empty.
   - A packet with modifications is not false or invalid; it is outside this first eligibility slice and must be reported as unsupported/deferred rather than silently reinterpreted.

3. **Every created output is compatibly evidenced under the exact historical lane contract.**
   - each exact created artifact matches exactly one declared lane output type;
   - that type has exactly one evidence requirement with exactly one `required_states` value under the current bounded compatibility semantics;
   - at least one packet evidence record is exact-subject-bound to that exact artifact and has exactly that required state;
   - any missing/ambiguous output contract, missing/ambiguous evidence requirement, or unresolved multi-state requirement fails closed through existing canonical preflights.

4. **No evidence-precedence policy is invented.**
   - for each created output, all packet evidence records exact-subject-bound to that output must carry the same single required state for this first eligibility slice;
   - if the same exact output also has subject-bound packet evidence in another state, eligibility must not choose a winner by array order, recency, state ranking, actor intent, confidence, or role;
   - such a packet is outside the first eligible slice until an explicit evidence precedence/invalidation decision exists.

5. **Exact created-artifact work-base provenance is grounded.**
   - each created artifact must pass Decision 010's exact work-base and producer-lane provenance invariant against the same exact claim base/lane;
   - historical artifact versions whose provenance relation is not exact enough for that preflight remain outside this first slice rather than being guessed into compatibility.

6. **Dependency policy is not invented.**
   - every created artifact in this first eligible slice must have an empty `dependency_refs[]` set;
   - packets with dependencies remain valid institutional objects, but Stage 4 currently exposes dependency identity/context/graph/reachability facts without a universal admissibility/satisfaction/closure rule;
   - therefore non-empty dependencies yield an explicit unsupported/deferred eligibility reason, not acceptance or rejection.

7. **Packet uncertainty/failure text is preserved as fact, not silently converted into authority.**
   - `uncertainties`, `failures_or_blockers`, `downstream_effects`, and `requested_followup` remain visible packet facts;
   - this eligibility projection does not erase them, rank them, or close the claim;
   - their mere presence does not become a hidden universal rejection rule in this decision.

8. **Source metadata is preserved without becoming trust/closure authority.**
   - existing provenance/source fields remain part of the exact artifact/evidence objects;
   - this first eligibility projection does not claim source trust, relevance, completeness, closure, immutable source context, or literal re-execution;
   - source facts may be surfaced but must not be silently promoted into an acceptance requirement that the current lane contract did not declare.

## Required result shape / meaning

Lane 02 may choose the exact Python representation, but the returned deterministic named fact must make at least these meanings explicit:

- exact `packet_ref`;
- exact `base_state_revision_ref`;
- exact `claim_ref`;
- exact `lane_ref`;
- exact created output refs considered;
- `eligibility_outcome`, with a bounded vocabulary equivalent to:
  - `eligible_for_stage5_acceptance_candidate`;
  - `not_eligible_unsatisfied_output_evidence`;
  - `not_eligible_conflicting_subject_evidence`;
  - `unsupported_modified_output_slice`;
  - `unsupported_dependency_policy`;
- deterministic reason facts sufficient to explain the outcome without exception text, actor identity, timestamps, branch/CI state, or private chat.

An implementation may use more precise reason codes if they remain deterministic and do not broaden semantics.

`eligible_for_stage5_acceptance_candidate` means only that the packet fits this first bounded factual slice. It is **not** packet acceptance, root approval, claim closure, successor publication, integration, replay success, or global currentness.

## Reuse requirement

The implementation should compose existing canonical preflights rather than duplicate or weaken them. At minimum it should reuse the already-grounded exact packet/output/evidence/provenance path and preserve its fail-closed semantics.

Do not add a mutable `current`, newest-object selection, logical-id fallback, actor preference, schedule precedence, founder override, or Git/CI authority to obtain an eligibility result.

## Required implementation evidence

Lane 02 should implement only this read-only Decision 024 projection and add deterministic regressions demonstrating at least:

1. one exact created-output packet with exact provenance and one exact required-state evidence record is eligible;
2. weak/missing evidence is not eligible;
3. exact subject-bound evidence in both the required state and a different state does not get silently ranked into eligibility;
4. unrelated/unmatched evidence cannot satisfy an output;
5. same-logical-id/different-exact artifact evidence cannot satisfy the output;
6. a packet with non-empty `artifacts_modified[]` is explicitly outside the first slice;
7. a created artifact with any non-empty exact dependency set is explicitly outside the first slice;
8. exact provenance-base or producer-lane mismatch fails through the existing provenance preflight;
9. packet uncertainties/failures/follow-up remain observable and are not erased by the eligibility result;
10. repeated identical exact inputs produce identical named eligibility facts;
11. no mutable current/HEAD, recency, array order, actor/founder identity, schedule, CI, branch, or Git permission participates;
12. the complete deterministic suite and explicit compile remain green.

## Lane 03 attack surface

After Lane 02 publishes an exact tested head, Lane 03 should attack only this Decision 024 slice:

- evidence conflict laundering into eligibility;
- weak/unmatched evidence becoming sufficient through type pooling;
- exact subject substitution by logical id or recency;
- modified packets accidentally entering the created-only slice;
- non-empty dependencies being treated as satisfied without a dependency policy;
- provenance mismatch being bypassed by packet/lane names;
- uncertainty/failure text disappearing from the reconstructable packet context;
- mutable currentness, actor identity, schedule, CI, branch, or Git permission entering disposition;
- deterministic fact transport changing meaning under materialization.

Do not jump to integration-receipt/result chronology, successor publication, claim closure, epochs, or replay until this exact prerequisite is independently grounded.

## Why Stage 5 remains closed for one more gate

The current component facts are strong enough to define this bounded eligibility slice, but not yet enough to mutate canonical state without silently inventing packet acceptance semantics.

Once Decision 024 is implemented and independently checked, Lane 01 should perform the next narrow Stage 5 entry review. That review may then open the smallest immutable transition or name the next exact prerequisite. ADV-002-G/H receipt identity and the content-addressed receipt/result chronology remain explicit downstream obligations rather than being solved implicitly inside this packet-level precondition.

## Root grounding

### Truth

A set of component facts is not the same thing as a packet-level acceptance fact. The kernel must make the composition rule explicit before a mutating integration runtime can rely on it. Conflicting exact-subject evidence and unresolved dependency policy are preserved rather than ranked away.

### Agency / non-domination

No founder, occupant, specialist, model, schedule, CI state, branch, or Git permission can turn an unsupported packet into an eligible one. The result follows exact stored relations and bounded rules only.

### Continuity

A replacement occupant can reconstruct exactly why a packet is or is not inside the first Stage 5 candidate slice from repository/store state. The decision does not require hidden chat convention about what `done`, confidence, or a specialist role was meant to imply.

### Wisdom before speed

Open one read-only composition fact before opening canonical state mutation. Restrict the first slice to created outputs with no unresolved dependency policy instead of deciding evidence precedence, dependency closure, source trust, claim closure, receipt chronology, and replay all at once.

## Ownership

**Lane 02:** implement Decision 024 only, with deterministic tests and explicit compile evidence.

**Lane 03:** attack the exact tested Decision 024 head only; preserve all failed/uncertain evidence.

**Lane 01:** integrate only after the implementation and adversarial evidence are sufficiently grounded against the four roots, then perform the next bounded Stage 5 entry review.
