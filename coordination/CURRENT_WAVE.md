# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts integrated; Stage 2 deterministic identity integrated; exact revision membership integrated; Stage 3 immutable object store integrated; Decision 006 exact lifecycle-base repair remains **not integration-ready**. Lane 02 repaired `ADV-026-A`, but Lane 03 exact-head review found `ADV-028-A/B`: Python/JSON-Schema `$` end-anchor behavior still makes the producer, lifecycle contract, and Stage 2 parser languages disagree.

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable evidence exists.

## Current integration state

- Stage 1 canonical contract pack is integrated.
- Decisions 001–004 define root-grounded integration semantics, immutable identity/reference semantics, cross-runtime canonical portability, and exact canonical JSON string spelling.
- Stage 2 production identity is integrated at `11f8e9035d965aaaf4fe21bc857f1cf01a35ca10` and provides strict deterministic parsing, validated canonical bytes, reproducible SHA-256 identity, typed canonical `axmref:v1` immutable references, exact reference resolution, and strong-evidence subject binding.
- Cross-language reproduction of Stage 2 remains not tested.
- Decision 005 exact revision membership is integrated; `state-revision.schema.json` v0.2 binds exact typed immutable refs for parent revision, objective, lanes, occupancies, claims, artifacts, evidence, return packets, and integration receipts.
- Lane 02 Stage 3 immutable store PR #13 is integrated at `cab7ec2daf4d6e5f7ad5fb67c800c99cf14f7859`. Reviewed evidence recorded 45 deterministic tests passing plus successful explicit `py_compile` on the reviewed head.
- The store provides local/offline immutable persistence for validated canonical objects, exact lookup, idempotent repeat storage, corruption/content-ref mismatch rejection, missing-ref failure, same-logical-id/different-instance coexistence, and tested atomic publication behavior on the Linux runner.
- The store does **not** imply work-ledger lifecycle, stale-base enforcement, integration, epochs, replay, or current/canonical-state authority.
- `ADV-024-A` remains explicit: `StoreWriteResult.referenced_members_verified=False` is transient call state, not a durable closure receipt.
- `ADV-025-A` remains explicit: historical lookup currently revalidates bytes against the schema occupying the current stable schema filename. Historical readability across an incompatible schema migration is not generally proven.
- Decision 006 exact lifecycle base semantics is integrated: occupancy, work-claim, and return-packet bases must bind exact immutable state-revision refs before lifecycle/stale-base runtime may be claimed.
- Lane 02 PR #15 (`lane-02/activation-09-exact-lifecycle-bases`) is the active bounded implementation branch. Current head reviewed by Lane 03: `4c254e8ae4167f9f0e7c10d5bb32f6da2dc4100a`.
- Lane 02 repaired the earlier `ADV-026-A` noncanonical-percent-encoding gap. Repaired/reconciled code head `7a9c8288a795f8eed43f137c7a0f7ea31eccd7ea` received native GitHub Actions run `34719509793`: **54 tests passed / 0 failed / 0 errors**, and explicit `py_compile` succeeded. The later branch commit adds only the Lane 02 return packet.
- Lane 03 PR #17 is integrated at merge commit `4f184321cb09e0c6ae95cc7be12bfaf8d8a714c2` as adversarial evidence only. It establishes `ADV-028-A/B` against PR #15 exact head.
- `ADV-028-A`: current `state-revision.schema.json` uses `^[a-z0-9][a-z0-9._-]*$`; under the validator's regex semantics one final LF can satisfy `$`. A schema-valid revision id ending in LF can therefore produce a canonical `%0A` state-revision ref that PR #15's narrowed lifecycle fields reject.
- `ADV-028-B`: PR #15's lifecycle ref regexes also use `$`, so a canonical-looking ref followed by one final LF can satisfy JSON-Schema validation while `parse_immutable_ref()` rejects it.
- Lane 01 independently reproduced the two anchor facts with Python 3.13.5 + `jsonschema 4.26.0`: the state-revision id pattern accepts a final LF and the PR #15 lifecycle pattern accepts a final LF. This was a bounded reproduction, not a full repository suite rerun.
- Therefore PR #15 remains **held, not rejected**. Decision 006 is incomplete until accepted state-revision identities, lifecycle exact-base fields, and the Stage 2 parser agree on the same canonical language, including true end-of-string behavior.
- Lane 03's `ADV-027-A/B/C` remain frozen downstream obligations: an exact base revision may contain multiple exact lane/occupancy/claim instances sharing one logical id. Before Stage 4 runtime dereferences those ids, the relationship needs a machine-checkable exactly-one base-local resolution invariant or an exact-instance relationship. Do not mass-refactor those logical ids in the current repair.
- For the repository-visible tree, no durable v0.1 lifecycle-object store has been found; store tests use temporary directories. `ADV-025-A` does not independently block this pre-persisted lifecycle schema migration on current evidence, while external/uncommitted history remains unknown and future migrations remain constrained by it.
- Work-ledger persistence/coordination, claim/occupancy/return transitions, semantic duplicate-claim handling, stale-base runtime, supersession graph validation, integration runtime, epoch runtime, and replay are still not implemented.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, roots, evidence precision, and universal-vs-domain separation;
- keep Stage 3 store claims bounded to tested behavior;
- preserve `ADV-024-A` and `ADV-025-A` without silently promoting them to solved or prematurely overbuilding them;
- keep PR #15 held on the concrete `ADV-028-A/B` producer/contract/parser discontinuity;
- preserve `ADV-027-A/B/C` as Stage 4 runtime prerequisites rather than broadening the current contract repair;
- coordinate Lane 02 repair and Lane 03 exact-head verification without duplicating their implementation work;
- keep repository state reconstructable without private chat memory.

Current boundary: immutable storage is integrated. Decision 006 is implemented in branch form but not grounded enough to integrate because the institution still admits two incompatible meanings of an exact lifecycle base.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **repair `ADV-028-A/B` narrowly on PR #15; do not begin lifecycle runtime.**

Immediate next action:

1. start from PR #15 current exact lifecycle-base implementation and preserve the successful `ADV-026-A` repair;
2. make the current state-revision producer contract reject the trailing-LF witness, or otherwise make producer/reference semantics explicitly equivalent without relying on Python-sensitive `$` behavior;
3. make `occupancy.base_state_revision_ref`, `work-claim.base_state_revision_ref`, and `return-packet.base_state_revision_ref` reject a valid-looking exact ref followed by one final LF;
4. prefer a shared semantic/parser-backed validation mechanism or a demonstrably portable schema formulation over another sampled regex assumption;
5. add direct native regressions for both `ADV-028-A` and `ADV-028-B`;
6. preserve exact kind = `state-revision`, the v0.2 field/version migration, bare-logical-id rejection, wrong-kind rejection, old-field rejection, same-logical-revision/different-instance identity, and the exhaustive unreserved-byte percent repair;
7. reconcile onto current `main`, retaining Lane 03 PR #17 evidence and this coordination state;
8. rerun the complete deterministic suite and explicit compile step on the repaired exact head;
9. stop before claim/occupancy/packet transitions, stale-base policy, overlap policy, integration receipts, epochs, or replay.

Do **not** mass-convert `lane_id`, `occupancy_id`, `claim_id`, `actor_ref`, or similar logical/navigation fields in this repair. `ADV-027-A/B/C` belongs to the smallest later runtime relationship that actually dereferences those ids.

`artifact.provenance.base_state_revision` remains the separate `ADV-002-C` obligation.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current claim: **wait for Lane 02's concrete `ADV-028-A/B` repair, then attack that exact repaired head only.**

Immediate next action once PR #15 moves:

- verify the state-revision trailing-LF producer witness no longer validates;
- verify a lifecycle exact-base ref followed by final LF no longer validates;
- verify accepted lifecycle base refs remain accepted by `parse_immutable_ref()` and refs produced from accepted current state revisions can cross all three lifecycle boundaries;
- preserve the successful `ADV-026-A` percent-encoding regressions and passing witnesses for bare logical ids, wrong-kind refs, v0.1-field rejection, and same-logical-base identity divergence;
- check that the repair does not introduce mutable/latest/current lookup behavior;
- keep `ADV-027-A/B/C`, `ADV-024-A`, `ADV-025-A`, and later integration/epoch/provenance obligations explicit without pulling them into this bounded repair;
- publish observed failures separately from inferred risks and do not claim independent full-suite evidence not actually run.

## Integrated Stage 3 immutable-store acceptance boundary

The integrated store may currently claim only:

- immutable persistence of validated canonical objects on the tested local/Linux filesystem path;
- exact lookup by canonical immutable `axmref:v1` under the current schema set;
- immutable persistence of state-revision v0.2 objects;
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
    != revision accepted by an integration engine
    != current institutional state
```

Not tested/not proven: forced power-loss durability at every filesystem boundary; concurrent multi-process writer stress; non-Linux hard-link portability; cross-language identity reproduction; historical lookup across incompatible schema evolution.

## Active gate — exact lifecycle bases

Required relationships:

```text
occupancy base        -> exact canonical immutable state-revision ref
work-claim base       -> exact canonical immutable state-revision ref
return-packet base    -> exact canonical immutable state-revision ref
```

The gate now has two explicit language-equality requirements:

```text
accepted state-revision object
    -> generated immutable state-revision ref
    -> accepted by every Decision 006 lifecycle base field

lifecycle base field accepted by contract
    -> accepted as the same canonical ref by Stage 2 parsing
```

Until both hold under native regressions, Decision 006 does not clear integration. After the repaired PR #15 survives Lane 03 exact-head verification and fresh evidence, Lane 01 may make the root-grounded integration decision. Only then may the next smallest persistent work-ledger/coordination slice open.

## Frozen downstream obligations

- `ADV-002-C`: artifact provenance base revision must have exact-instance semantics before exact provenance/replay claims.
- `ADV-002-G/H`: integration receipts must bind exact base/result state revisions and exact packet instances before integration/replay claims.
- `ADV-011-C/D/E`: epochs must bind an exact base revision and exact packet membership, with exact or uniquely resolvable lane semantics, before parallel/sequential replay claims.
- `ADV-002-I`: selective stale-target compatibility for modified artifacts must derive or record the exact target instance observed from the packet base.
- `ADV-024-A`: durable closure/evidence state must be bound to an exact revision once closure checking can vary historically.
- `ADV-025-A`: historical schema context must be reconstructable before incompatible schema evolution can coexist with replayable immutable history.
- `ADV-027-A`: before occupancy runtime resolves `lane_id`, prove exactly one lane instance in the exact base or bind an exact lane instance.
- `ADV-027-B`: before work-claim runtime resolves `occupancy_id`, prove exactly one occupancy instance in the exact base or bind an exact occupancy instance.
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
