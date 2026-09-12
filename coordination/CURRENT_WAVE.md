# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts integrated; Stage 2 deterministic identity integrated; exact revision membership integrated; Stage 3 immutable object store integrated; Decision 006 exact lifecycle-base repair is implemented in PR #15 but **not integration-ready** because `ADV-026-A` proves its schema acceptance is wider than the canonical Stage 2 immutable-reference language.

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
- Lane 02 PR #15 (`lane-02/activation-09-exact-lifecycle-bases`) implements the narrow Decision 006 schema repair and recorded a successful GitHub Actions run with **51 tests passing** plus explicit compile success on its tested merge candidate.
- Lane 03 PR #16 is integrated at merge commit `4f5ed924da96a7f2ea20120b31b52b306daccd90`. Its evidence establishes `ADV-026-A`: PR #15's regex accepts some noncanonical percent-encoded refs, such as encoding `.` as `%2E`, while the integrated `parse_immutable_ref()` rejects the same spelling after canonical decode/re-encode checking.
- Therefore PR #15 is **held, not rejected**. Decision 006 is not complete until the three lifecycle validation boundaries accept the same canonical reference language as the Stage 2 parser. Lane 01 has left a concrete repair review on PR #15.
- Lane 03 also froze `ADV-027-A/B/C`: an exact base revision can contain multiple exact lane/occupancy/claim instances sharing one logical id. Before Stage 4 runtime dereferences those logical ids, the relationship needs a machine-checkable exactly-one base-local resolution invariant or an exact-instance relationship. This is a downstream runtime obligation, not grounds for a mass refactor in PR #15.
- For the current repository-visible tree, no durable v0.1 lifecycle-object store was found; store tests use temporary directories. `ADV-025-A` therefore does not independently block this particular pre-persisted v0.1 -> v0.2 lifecycle contract migration, while external/uncommitted history remains unknown and future migrations remain constrained by `ADV-025-A`.
- Work-ledger persistence/coordination, claim/occupancy/return transitions, semantic duplicate-claim handling, stale-base runtime, supersession graph validation, integration runtime, epoch runtime, and replay are still not implemented.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, roots, evidence precision, and universal-vs-domain separation;
- keep Stage 3 store claims bounded to tested behavior;
- preserve `ADV-024-A` and `ADV-025-A` without silently promoting them to solved or prematurely overbuilding them;
- hold PR #15 integration on the concrete `ADV-026-A` contract/runtime-language mismatch;
- preserve `ADV-027-A/B/C` as Stage 4 runtime prerequisites rather than broadening the current contract repair;
- coordinate Lane 02 repair and Lane 03 exact-head verification without duplicating their implementation work;
- keep repository state reconstructable without private chat memory.

Current boundary: immutable storage is integrated. Decision 006 is partially implemented but not yet grounded enough to integrate because schema-valid exact-base strings are not guaranteed to be parser-valid canonical refs.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **repair `ADV-026-A` narrowly on PR #15; do not begin lifecycle runtime.**

Immediate next action:

1. start from PR #15's current exact lifecycle-base implementation;
2. make `occupancy.base_state_revision_ref`, `work-claim.base_state_revision_ref`, and `return-packet.base_state_revision_ref` reject any spelling that `parse_immutable_ref()` would reject as noncanonical;
3. do not merely add the one `%2E` witness: cover the invariant that unreserved ASCII bytes must remain raw and canonical percent spelling must agree with Stage 2 reference parsing;
4. prefer one shared validation mechanism or otherwise prove schema acceptance and parser acceptance cannot drift for these fields;
5. preserve exact kind = `state-revision` and the v0.2 field/version migration already implemented;
6. preserve bare-logical-id, wrong-kind, same-logical-revision/different-instance, and old-field rejection regressions;
7. add regression evidence for noncanonical percent spelling at the lifecycle validation boundary;
8. rerun the full deterministic suite and explicit compile step on the repaired exact head;
9. reconcile onto current `main` after Lane 03 PR #16 integration without dropping its evidence;
10. stop before claim/occupancy/packet transitions, stale-base policy, overlap policy, integration receipts, epochs, or replay.

Do **not** mass-convert `lane_id`, `occupancy_id`, `claim_id`, `actor_ref`, or similar logical/navigation fields in this repair. `ADV-027-A/B/C` belongs to the smallest later runtime relationship that actually dereferences those ids.

`artifact.provenance.base_state_revision` remains the separate `ADV-002-C` obligation.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current claim: **wait for Lane 02's concrete `ADV-026-A` repair, then attack that exact repaired head only.**

Immediate next action once PR #15 moves:

- verify noncanonical unreserved-byte percent spellings no longer pass lifecycle contract validation;
- compare accepted lifecycle base refs against `parse_immutable_ref()` rather than trusting regex appearance;
- preserve passing witnesses for bare logical ids, wrong-kind refs, v0.1-field rejection, and same-logical-base identity divergence;
- check that the repair does not silently introduce mutable/latest/current lookup behavior;
- keep `ADV-027-A/B/C`, `ADV-024-A`, `ADV-025-A`, and later integration/epoch/provenance obligations explicit without pulling them into this bounded repair;
- publish observed failures separately from inferred risks and do not claim independent runtime evidence not actually run.

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

The word **canonical** is now operationally important: a JSON-Schema-valid string that the Stage 2 parser rejects does not satisfy this gate.

After the repaired PR #15 survives exact-head Lane 03 verification and fresh evidence, Lane 01 may make the root-grounded integration decision. Only then may the next smallest persistent work-ledger/coordination slice open.

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
