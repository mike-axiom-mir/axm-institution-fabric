# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts integrated; Stage 2 deterministic identity integrated; exact revision membership integrated; Stage 3 immutable object store integrated; Decision 006 exact lifecycle bases integrated; shared semantic state-revision member validation integrated; exact-base exactly-one member resolver integrated and adversarially challenged; Decision 007 lifecycle relationship chronology accepted. The next bounded gate is the created-after-base relationship repair for work-claim -> occupancy and return-packet -> claim. Lifecycle mutation remains closed.

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable evidence exists.

## Current integration state

- Stage 1 canonical contract pack is integrated.
- Decisions 001–004 define root-grounded integration semantics, immutable identity/reference semantics, cross-runtime canonical portability, and exact canonical JSON string spelling.
- Stage 2 production identity is integrated at `11f8e9035d965aaaf4fe21bc857f1cf01a35ca10` and provides strict deterministic parsing, validated canonical bytes, reproducible SHA-256 identity, typed canonical `axmref:v1` immutable references, exact reference resolution, and strong-evidence subject binding.
- Cross-language reproduction of the full Stage 2 identity algorithm remains not tested.
- Decision 005 exact revision membership is integrated; `state-revision.schema.json` v0.2 binds typed immutable refs for parent revision, objective, lanes, occupancies, claims, artifacts, evidence, return packets, and integration receipts.
- Stage 3 immutable store PR #13 is integrated at `cab7ec2daf4d6e5f7ad5fb67c800c99cf14f7859`. Reviewed evidence recorded 45 deterministic tests passing plus explicit `py_compile` on the reviewed head.
- The store provides local/offline immutable persistence for validated canonical objects, exact lookup, idempotent repeat storage, corruption/content-ref mismatch rejection, missing-ref failure, same-logical-id/different-instance coexistence, and tested atomic publication behavior on the Linux runner.
- `ADV-024-A` remains explicit: `StoreWriteResult.referenced_members_verified=False` is transient call state, not a durable closure receipt.
- `ADV-025-A` remains explicit: historical lookup currently revalidates bytes against the schema occupying the current stable schema filename. Historical readability across an incompatible schema migration is not generally proven.
- Decision 006 exact lifecycle-base semantics is integrated through PR #15 merge commit `4f51dea31bd494099266e0e5a13ab34f1b53958b`.
- PR #19 is integrated as `090b8bde1638eacc277f4df27bf3f254b8225e86`; all state-revision exact-member families pass through the shared Stage 2 semantic parser plus required-kind validation before normal store publication. Native tested-head evidence recorded 67 deterministic tests / OK plus explicit `py_compile`; prior failed evidence remains preserved.
- Lane 02 PR #22 is integrated as merge commit `c28ca8e67afac1e5bdf0286e0e8b80acb6a851e1`.
- PR #22 adds the read-only `resolve_exact_revision_member(...)` primitive. It accepts one exact `state-revision` ref, one explicit membership family / required kind, and one logical id; loads the exact base and every exact member in that selected family through the immutable store; returns only one exact immutable member when exactly one logical-id match exists; and fails explicitly on zero/multiple matches, wrong configuration, invalid base refs, missing members, or corrupt members.
- Lane 02 native GitHub Actions run `34730104976` on tested implementation head `d991d624e0b826be286051ca7097c4c0d8fd0af0` completed successfully with `Ran 79 tests in 84.900s` / `OK` plus explicit compilation including the resolver and its regression module. Final Lane 02 head added only its return packet after that tested implementation.
- Lane 03 PR #23 adversarially challenged the exact resolver surface and is integrated as merge commit `0dc9745bc3528543d2fb18f0253808399aa6e5af`.
- Lane 03 covered lane/occupancy/work-claim same-logical-id ambiguity, member-array reordering, an unreferenced later same-id object in the store, exact returned identity, and selected-family success without global revision closure. Its first exact stacked run `34730613240` recorded `Ran 85 tests in 128.043s` / `OK`; after PR #22 integration the branch was reconciled without content change and run `34731861339` also completed successfully before integration.
- No new resolver counterexample was found on that bounded surface. This clears only the generic read-only primitive, not relation chronology or lifecycle mutation.
- Decision 007 (`007_LIFECYCLE_RELATIONSHIP_CHRONOLOGY.md`) is accepted at commit `05022e2d9f0d9ebcfcc61afdfcf0e8161e09f731`.
- Decision 007 separates relationships whose target must already exist in the exact base from relationships whose target is created after that base. Pre-existing relationships may use exact-base exactly-one logical resolution; created-after-base authoritative relationships must bind exact immutable target instances directly.
- For the first lifecycle chronology: `occupancy.lane_id` may resolve against the occupancy's exact entry base only when exactly one lane instance matches; `work-claim.occupancy_id` is insufficient as authoritative runtime identity because the occupancy can be created after the work base; `return-packet.claim_id` is likewise insufficient because the claim can be created after the work base.
- Work-ledger persistence/coordination, claim/occupancy/return transitions, semantic duplicate-claim handling, stale-base runtime, supersession graph validation, successor-revision lifecycle publication, integration runtime, epoch runtime, and replay are still not implemented.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, roots, evidence precision, and universal-vs-domain separation;
- treat the exact-base member resolver as integrated only on its tested read-only surface;
- preserve Decision 007's temporal distinction instead of applying the resolver to every relationship by convenience;
- keep lifecycle mutation closed until created-after-base authoritative relationships can name exact immutable instances;
- keep `ADV-024-A`, `ADV-025-A`, provenance, stale-target, integration-receipt, epoch, portability, and cross-language obligations explicit;
- prevent logical ids, recency, mutable current/HEAD, array order, occupant identity, schedule position, founder status, or private chat from becoming hidden historical authority;
- maintain repository state so another occupant can reconstruct the build without private chat memory.

Current boundary: immutable storage, exact lifecycle bases, semantic exact-member validation, and exact-base exactly-one member resolution are integrated. Decision 007 now defines the chronology boundary. The next work is a narrow contract repair for the two post-base authoritative relationships; no claim/occupancy/return mutation should begin before that repair survives deterministic and adversarial evidence.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **repair only the created-after-base authoritative relationship contracts from Decision 007; do not begin lifecycle mutation runtime.**

Immediate next action:

1. start from current canonical `main` after PR #22/#23 integration and Decision 007;
2. repair `work-claim.occupancy_id` into an exact canonical immutable occupancy relationship, preferably `occupancy_ref`;
3. repair `return-packet.claim_id` into an exact canonical immutable work-claim relationship, preferably `claim_ref`;
4. version the affected schemas honestly and update the canonical fixture without broad unrelated rewrites;
5. route semantic checking through the existing Stage 2 `parse_immutable_ref()` path (or the existing shared validation surface) so JSON Schema is not treated as a second Unicode/percent/canonicality parser;
6. require the exact parsed kind to be `occupancy` for the work-claim relationship and `work-claim` for the return-packet relationship;
7. add deterministic witnesses showing bare logical ids, wrong-kind refs, noncanonical percent/UTF-8/NFC/trailing-data forms fail at the semantic validation boundary;
8. prove two exact occupancy instances with one logical id give different work-claim immutable identities when substituted;
9. prove two exact work-claim instances with one logical id give different return-packet immutable identities when substituted;
10. include a chronology witness in which the exact occupancy/claim object is created after the lifecycle object's `base_state_revision_ref`; do not require those post-base objects to be members of the earlier base;
11. preserve `lane_id`, `occupancy.claim_ids`, `overlap_with_claim_ids`, evidence, uncertainty, and handoff fields unless a concrete test demonstrates a separate blocker;
12. exercise the normal immutable-store validation path for the repaired object types so malformed authoritative refs cannot enter normal publication merely because isolated schema validation passed;
13. rerun the complete deterministic suite and explicit compile step, publish a bounded return packet, and stop before opening/closing occupancies, claims, or packets.

This repair is about historical identity, not about making every logical id immutable. Do not mass-convert unrelated fields.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current claim: **wait for Lane 02's concrete Decision 007 contract repair, then attack that exact head without implementing lifecycle transitions.**

Immediate next action once the repair exists:

- create two immutable occupancies with the same logical id but different exact content and prove a work claim binds only the supplied exact occupancy instance;
- create two immutable work claims with the same logical id but different exact content and prove a return packet binds only the supplied exact claim instance;
- prove newest/current/array order cannot substitute a different post-base instance;
- prove the exact occupancy and claim may post-date the common work base without being falsely required to appear in that base revision;
- challenge wrong-kind, malformed, invalid UTF-8, non-NFC, percent-encoding, trailing-data, and content/ref mismatch cases through the real store-facing validation path;
- check that the narrow repair does not silently alter `lane_id`, overlap-reporting, uncertainty, evidence, or handoff semantics;
- preserve `occupancy.claim_ids` and `overlap_with_claim_ids` as unresolved snapshot/navigation semantics rather than silently promoting them to exact relationship authority;
- preserve `ADV-024-A`, `ADV-025-A`, provenance, stale-target, integration receipt, epoch, replay, portability, and cross-language obligations as downstream state;
- distinguish observed/runtime-tested evidence from inferred risk and do not relabel Lane 02 CI as independent Lane 03 execution.

## Integrated resolver acceptance boundary

The integrated read-only resolver may currently claim only:

```text
exact state-revision ref
    + explicit membership family / required kind
    + logical id
    -> load exact base
    -> load/verify every exact member in the selected family
    -> exactly one logical-id match => return that exact immutable ref/object
    -> zero or multiple matches => explicit failure
```

Observed tested properties include:

- lane, occupancy, and work-claim families use the same bounded primitive;
- ambiguity survives member-array reordering rather than allowing position to choose a winner;
- a newer/same-id object elsewhere in the store cannot override exact base membership;
- missing/corrupt members in the selected family fail loudly rather than being skipped;
- successful lookup of one family does not imply global revision closure;
- no mutable `current`/`HEAD` pointer is used.

Important distinction:

```text
base-local resolver works
    != every lifecycle relationship is base-local
    != referenced target existed in that base
    != revision is globally referentially complete
    != lifecycle mutation works
    != stored object is current/canonical state
```

## Active gate — Decision 007 post-base authoritative refs

Required chronology:

```text
occupancy entry base N
    lane existed in N
    -> lane_id may resolve exactly-one inside N

occupancy O created from N
    work claim C created after O, while preserving work base N
    -> C must bind exact O directly

claim C created after N
    return packet P produced later, while preserving work base N
    -> P must bind exact C directly
```

Forbidden hidden resolution rules remain:

```text
newest version
recency
array order
mutable current/HEAD
occupant identity
schedule order
founder status
private chat memory
```

Only after this contract repair survives deterministic evidence and Lane 03 exact-head challenge may Lane 01 open the first actual lifecycle transition slice. The first relationship already grounded for that future slice is occupancy -> lane: the lane must resolve exactly once inside the occupancy's exact entry base.

## Frozen downstream obligations

- `ADV-002-C`: artifact provenance base revision must have exact-instance semantics before exact provenance/replay claims.
- `ADV-002-G/H`: integration receipts must bind exact base/result state revisions and exact packet instances before integration/replay claims.
- `ADV-011-C/D/E`: epochs must bind an exact base revision and exact packet membership, with exact or uniquely resolvable lane semantics, before parallel/sequential replay claims.
- `ADV-002-I`: selective stale-target compatibility for modified artifacts must derive or record the exact target instance observed from the packet base.
- `ADV-024-A`: durable closure/evidence state must be bound to an exact revision once closure checking can vary historically.
- `ADV-025-A`: historical schema context must be reconstructable before incompatible schema evolution can coexist with replayable immutable history.
- `occupancy.claim_ids`: snapshot/chronology semantics remain unresolved; do not use as exact dereference authority yet.
- `work-claim.overlap_with_claim_ids`: report/navigation semantics remain unresolved; do not use as exact dereference authority yet.
- lifecycle successor-revision publication remains unimplemented and must not be implied by immutable object persistence.
- full cross-language reproduction of the identity/resolution stack remains not tested.

These are obligations, not evidence that the corresponding runtimes exist.

## Shared return-packet minimum

Each lane leaves: base inspected; bounded claim; files changed; evidence/tests; uncertainty/blockers; dependency/downstream effects; next action; and explicit evidence status (`proposed`, `implemented`, `compiled`, `automated_tested`, `runtime_tested`, `measured`, `inferred`, `blocked`, `not_tested`, etc.).

## Merge boundary

Inside AXM, the constitutional merge gate remains:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

No lane, founder, model, specialist, schedule position, CI result, or Git permission becomes authority by identity. When grounding is insufficient, preserve uncertainty or dissent instead of converting confidence into canon.
