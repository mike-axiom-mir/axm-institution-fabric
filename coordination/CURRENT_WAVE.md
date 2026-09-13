# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts integrated; Stage 2 deterministic identity integrated; exact revision membership integrated; Stage 3 immutable object store integrated; Decision 006 exact lifecycle-base contracts integrated; exact state-revision member semantic validation integrated through PR #19. The next bounded gate is a read-only, exact-base, exactly-one member-resolution primitive for `ADV-027-A/B/C`; lifecycle mutation runtime remains closed.

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
- The store does **not** imply work-ledger lifecycle, stale-base enforcement, integration, epochs, replay, reference closure, or current/canonical-state authority.
- `ADV-024-A` remains explicit: `StoreWriteResult.referenced_members_verified=False` is transient call state, not a durable closure receipt.
- `ADV-025-A` remains explicit: historical lookup currently revalidates bytes against the schema occupying the current stable schema filename. Historical readability across an incompatible schema migration is not generally proven.
- Decision 006 exact lifecycle-base semantics is integrated through PR #15 merge commit `4f51dea31bd494099266e0e5a13ab34f1b53958b`.
- PR #15 binds `occupancy.base_state_revision_ref`, `work-claim.base_state_revision_ref`, and `return-packet.base_state_revision_ref` to exact canonical immutable state-revision refs. Native CI on tested head `43c6c40e016b08bbf48eacf9d1b8c08325ac5439` reported 58 tests passing / 0 failed / 0 errors plus explicit `py_compile`.
- Lane 02 PR #19 is integrated as merge commit `090b8bde1638eacc277f4df27bf3f254b8225e86`.
- PR #19 preserves `ADV-029-A/B` rejection and repairs `ADV-030-A/B` by routing all nine state-revision exact-member families through the existing Stage 2 `parse_immutable_ref()` semantic parser after structural schema validation, then enforcing the field-required kind.
- The repaired path rejects invalid UTF-8 percent bytes such as `%FF`, valid UTF-8 but non-NFC spellings such as `e%CC%81`, encoded RFC3986-unreserved bytes, and trailing data while preserving parser-canonical NFC references.
- The normal immutable-store state-revision publication path uses that same semantic validation before publication. This is semantic reference-language validation only; it does not prove referenced objects exist.
- Native GitHub Actions run `34727633160` on tested implementation head `f0e02d03f2f693147c180610a42a5bbfca4bff94` completed successfully: 67 deterministic tests / OK plus explicit `py_compile`.
- The preceding run `34727486133` remains preserved failed evidence: 18 new non-NFC test subcases used an overly narrow expected exception class. Production/store semantic rejection held; only the test expectation changed to the existing common `IdentityError` hierarchy.
- Final PR #19 head `f6e5b83e88674c1d2621585adcfae4e084f3ed04` differs from the tested implementation head only by Lane 02 Activation 013's return packet.
- Lane 03 Activation 014 found no new counterexample on the repaired member semantic gate. Its bounded source-derived reproduction recorded 0 / 180 malformed/noncanonical accepts and 594 / 594 parser-canonical cases without schema/parser disagreement; that is Lane 03 bounded evidence, not a replacement full repository run.
- Lane 03's return packet from PR #21 is preserved byte-for-byte on `main` at `coordination/returns/03/2026-09-13_ACTIVATION_014.md` (blob `40d2fd9a79c89bc2a20b96c253f21c862802d63a`) by commit `af5a4ec94a5e00960628e28c638163f17ca7541a`. PR #21 was closed after PR #19 advanced `main`, avoiding duplicate integration.
- No open pull requests remain after this integration pass.
- Work-ledger persistence/coordination, claim/occupancy/return transitions, semantic duplicate-claim handling, stale-base runtime, supersession graph validation, integration runtime, epoch runtime, and replay are still not implemented.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, roots, evidence precision, and universal-vs-domain separation;
- treat the exact member semantic-language gate as integrated on its tested/adversarially challenged surface;
- keep `ADV-024-A` and `ADV-025-A` explicit without silently promoting them to solved;
- open only the smallest `ADV-027` bridge needed before lifecycle transitions: deterministic exactly-one resolution within one exact base revision;
- avoid silently deciding relationship chronology that evidence has not yet fixed, especially return-packet-to-claim semantics;
- prevent array order, newest/current lookup, recency, occupant identity, or hidden chat from becoming relationship authority;
- keep repository state reconstructable without private chat memory.

Current boundary: immutable storage, exact lifecycle bases, and semantic exact-member validation are integrated. The next step is a read-only relationship-resolution primitive. Lifecycle mutation remains closed until that primitive survives deterministic and adversarial evidence and relation-specific semantics are grounded.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **implement the smallest read-only exact-base unique-member resolver for the `ADV-027` family; do not begin claim/occupancy/return mutation runtime.**

Immediate next action:

1. start from current canonical `main` after PR #19 integration and Lane 03 Activation 014 evidence preservation;
2. reuse the integrated immutable store and Stage 2 reference parser; do not create a mutable registry or second identity path;
3. implement one bounded resolver that receives an exact `state-revision` ref, one allowed revision membership family/kind, and one logical object id;
4. load the exact base revision by immutable ref, inspect only the exact member refs named by that revision, and identify members by loading/verifying those exact objects through the store;
5. return one exact immutable member ref/object only when **exactly one** base-local member of the required kind has the requested logical id;
6. fail explicitly on zero matches, multiple matches, wrong-kind configuration, missing referenced objects, corrupted referenced objects, or an invalid/noncanonical base ref;
7. never select by array order, newest version, recency, mutable `current`/`HEAD`, actor identity, schedule position, or hidden chat memory;
8. do not mark the entire revision referentially complete merely because one relationship was resolved; preserve `ADV-024-A` closure truth separately;
9. add deterministic tests for one match, zero match, two exact instances sharing one logical id, wrong kind/member family, missing exact member, and corruption/mismatch propagation;
10. exercise at least the lane, occupancy, and work-claim member families so `ADV-027-A/B/C` has a common primitive, but do **not** yet wire that primitive into lifecycle state transitions;
11. record explicitly that relationship chronology remains a separate question: a resolver primitive existing does not prove every logical relationship should resolve against the object's `base_state_revision_ref`;
12. rerun the complete deterministic suite and explicit compile step, publish a bounded return packet, and stop.

The preferred first API may be a small pure/read-only function or store method. Naming is secondary to the invariant: exact base + exact membership + exactly-one logical match -> exact immutable instance, otherwise explicit failure.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current claim: **wait for Lane 02's concrete exact-base resolver, then attack that exact head without redesigning the lifecycle.**

Immediate next action once the resolver exists:

- construct an exact base containing two different exact lane objects with the same logical `lane_id` and prove resolution fails rather than picking one;
- repeat for occupancy and work-claim member families;
- test zero-match, missing-member, corrupt-member, and wrong-kind/member-family cases;
- verify result identity is the exact immutable ref from the base revision, not a reconstructed newest/current value;
- verify array reordering cannot change a successful or ambiguous outcome;
- verify a partially missing base cannot be mislabeled as globally complete because one unrelated relationship resolves;
- inspect whether any convenience cache/index becomes hidden authority over the immutable base;
- preserve the chronology question explicitly: do not assume return-packet `claim_id` can always be resolved from `return-packet.base_state_revision_ref` until that relationship is separately grounded;
- preserve `ADV-024-A`, `ADV-025-A`, provenance, stale-target, integration-receipt, epoch, replay, portability, and cross-language obligations as downstream state;
- distinguish observed/runtime-tested evidence from inferred risks and do not relabel Lane 02 CI as independent Lane 03 execution.

## Integrated Stage 3 immutable-store acceptance boundary

The integrated store may currently claim only:

- immutable persistence of validated canonical objects on the tested local/Linux filesystem path;
- exact lookup by canonical immutable `axmref:v1` under the current schema/semantic validation set;
- immutable persistence of state-revision v0.2 objects;
- state-revision exact member refs pass the shared Stage 2 semantic parser and required-kind check before normal publication;
- idempotent storage of byte-identical content;
- loud failure on exact-reference/content mismatch, corrupt/non-canonical stored bytes, missing refs, or wrong-schema reinterpretation;
- interrupted pre-publication temp bytes do not become visible through normal exact lookup in the tested implementation;
- same logical id may coexist as multiple exact immutable instances;
- no mutable `current`/`HEAD` pointer exists in this slice.

Important distinction:

```text
revision object stored
    != all referenced members proven present
    != durable closure-check evidence exists
    != a logical relationship resolves uniquely inside that revision
    != revision accepted by an integration engine
    != current institutional state
```

Not tested/not proven: forced power-loss durability at every filesystem boundary; concurrent multi-process writer stress; non-Linux hard-link portability; cross-language full identity reproduction; historical lookup across incompatible schema evolution.

## Active gate — exact-base exactly-one member resolution

The next primitive must satisfy:

```text
exact base revision ref
    + exact membership family / required kind
    + logical id
    -> load exact base
    -> inspect only exact refs named by that base
    -> verify candidate objects through the immutable store
    -> exactly one logical-id match => return that exact immutable instance
    -> zero or multiple matches => explicit failure
```

Forbidden hidden resolution rules:

```text
array order
newest version
recency
mutable current/HEAD
occupant identity
schedule order
private chat memory
```

This primitive does **not** itself decide which lifecycle relationships must use base-local resolution. In particular, return-packet chronology may require an exact claim-instance relationship rather than lookup against the packet's work base. Do not silently settle that question inside a generic resolver.

Only after this primitive survives deterministic evidence and Lane 03 exact-head attack may Lane 01 open the first actual lifecycle transition slice or freeze a relationship-specific Decision 007.

## Frozen downstream obligations

- `ADV-002-C`: artifact provenance base revision must have exact-instance semantics before exact provenance/replay claims.
- `ADV-002-G/H`: integration receipts must bind exact base/result state revisions and exact packet instances before integration/replay claims.
- `ADV-011-C/D/E`: epochs must bind an exact base revision and exact packet membership, with exact or uniquely resolvable lane semantics, before parallel/sequential replay claims.
- `ADV-002-I`: selective stale-target compatibility for modified artifacts must derive or record the exact target instance observed from the packet base.
- `ADV-024-A`: durable closure/evidence state must be bound to an exact revision once closure checking can vary historically.
- `ADV-025-A`: historical schema context must be reconstructable before incompatible schema evolution can coexist with replayable immutable history.
- `ADV-027-A`: before occupancy runtime resolves `lane_id`, prove exactly one lane instance in the exact base or bind an exact lane instance.
- `ADV-027-B`: before work-claim runtime resolves `occupancy_id`, prove exactly one occupancy instance in the intended relationship state or bind an exact occupancy instance.
- `ADV-027-C`: before packet/lifecycle runtime dereferences logical claim/lane ids, define relationship-specific exactly-one resolution or exact-instance semantics; do not choose by recency, array order, mutable current state, or hidden chat.

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
