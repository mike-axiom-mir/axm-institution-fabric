# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts integrated; Stage 2 deterministic identity integrated; exact revision membership integrated; Stage 3 immutable object store integrated; exact lifecycle-base repair is the next gate before work-ledger/lifecycle runtime

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable evidence exists.

## Current integration state

- Stage 1 canonical contract pack is integrated.
- Decisions 001–004 define root-grounded integration semantics, immutable identity/reference semantics, cross-runtime canonical portability, and exact canonical JSON string spelling.
- Lane 02 Stage 2 production identity PR #7 is integrated at `11f8e9035d965aaaf4fe21bc857f1cf01a35ca10` after the bounded adversarial chain through `ADV-023-A`.
- Stage 2 provides strict deterministic parsing, validated canonical bytes, reproducible SHA-256 identity, typed `axmref:v1` immutable references, exact reference resolution, and strong-evidence subject binding.
- Cross-language reproduction of Stage 2 remains not tested.
- Decision 005 exact revision membership is integrated; `state-revision.schema.json` is version `0.2` and binds exact typed immutable refs for parent revision, objective, lanes, occupancies, claims, artifacts, evidence, return packets, and integration receipts.
- Lane 03's exact-target/stale-base audit is integrated and freezes downstream exact-instance obligations as `ADV-002-C` through `ADV-002-I` and `ADV-011-C` through `ADV-011-E`.
- Lane 02 Stage 3 immutable store PR #13 is integrated at merge commit `cab7ec2daf4d6e5f7ad5fb67c800c99cf14f7859`.
- The PR #13 merge-candidate GitHub Actions run `34713825913` completed successfully; Lane 02/Lane 03 evidence records **45 tests passing** and successful explicit `py_compile` on the exact reviewed head.
- The integrated store provides local/offline immutable persistence for validated canonical objects, exact `axmref:v1` lookup, idempotent repeat storage, loud corruption/content-ref mismatch rejection, missing-ref failure, same-logical-id/different-instance coexistence, and atomic publication behavior on the tested Linux runner.
- The store does **not** implement or imply work-ledger lifecycle, stale-base transition enforcement, integration, epochs, replay, or current/canonical-state authority.
- Lane 03's Stage 3 store audit is integrated as `adversarial/fixtures/STAGE3_STORE_CONTINUITY_GAPS.json` plus its Activation 009 return packet. PR #14 itself was closed after PR #13 changed `main`; its two exact files were copied unchanged onto `main` as commits `251f99a0c61eafbd94b4d2c21a02254332512f32` and `20dd6fad10be1c2fa7cfe7fbce41a6fb7c95267c` to avoid duplicate integration.
- `ADV-024-A` remains explicit: `StoreWriteResult.referenced_members_verified=False` is a transient call result, not a durable per-revision closure receipt. Storage alone must be treated as closure-unverified until a later immutable closure/evidence mechanism proves otherwise.
- `ADV-025-A` remains explicit: historical lookup currently revalidates bytes against the schema occupying the current stable schema filename. Long-term historical readability across an incompatible schema migration is **not proven**; reconstructable historical schema context must be repaired before the first migration that would invalidate stored history.
- Decision 006 exact lifecycle base semantics is integrated. Occupancy, work-claim, and return-packet base relationships must bind exact immutable state-revision refs before lifecycle/stale-base runtime may be claimed.
- Work-ledger storage/coordination, claim/occupancy/return transitions, semantic duplicate-claim handling, stale-base runtime, supersession graph validation, integration runtime, epoch runtime, and replay are still not implemented.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, root boundary, evidence precision, and universal-vs-domain separation;
- keep the integrated store's claims bounded to behavior actually tested;
- preserve `ADV-024-A` and `ADV-025-A` without either overbuilding them prematurely or allowing later code to silently erase them;
- hold lifecycle runtime until Decision 006's exact-base contract precondition is implemented and regression-tested;
- coordinate Lane 02 contract repair and Lane 03 adversarial verification without semantic overlap;
- maintain repository state so a later occupant can reconstruct the build without private chat memory.

Current boundary: the immutable store is now real and integrated. The next smallest dependency is exact lifecycle-base semantics, not the transition engine itself.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **implement Decision 006's smallest exact-base contract repair; do not begin lifecycle transitions or stale-base policy yet.**

Immediate next action:

1. start from current canonical `main` after the Stage 3 store and Decision 006 integration;
2. repair `occupancy.base_state_revision`, `work-claim.base_state_revision`, and `return-packet.base_state_revision` to bind exact typed `axmref:v1:state-revision` instances; a visible `_ref` field rename is preferred if it keeps migration/tests clearer;
3. increment affected schema versions where the contract shape changes rather than silently rewriting the meaning of v0.1;
4. update deterministic fixtures through the integrated Stage 2 identity path;
5. add regressions where two state revisions share one logical id but have different immutable refs and prove the lifecycle object identity changes with the exact base;
6. reject bare logical revision ids and wrong-kind immutable refs in the repaired fields;
7. keep `lane_id`, `occupancy_id`, `claim_id`, `actor_ref`, and similar logical/navigation fields unchanged unless concrete evidence shows exact-instance ambiguity; Decision 006 forbids mass refactoring for naming symmetry;
8. preserve existing evidence, uncertainty, blocker, and handoff fields unchanged unless the exact-base repair requires a narrowly justified fixture update;
9. rerun the full deterministic suite and explicit compile checks;
10. stop before claim open/close transitions, occupancy transitions, packet submission, stale-base rejection, overlap policy, integration receipts, epochs, or replay.

`artifact.provenance.base_state_revision` remains `ADV-002-C`. It may be repaired in the same branch only if the change stays demonstrably narrow and does not obscure the Decision 006 lifecycle gate; otherwise leave it as the explicit later provenance/replay obligation.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current claim: **attack the exact lifecycle-base repair once a concrete Lane 02 branch/PR exists; do not redesign the lifecycle runtime before its contracts are grounded.**

Immediate next action:

- verify that each repaired occupancy/work-claim/return-packet base binds one exact `state-revision` ref rather than a logical label, recency rule, mutable pointer, or hidden lookup convention;
- use the existing same-logical-id/different-instance witness from `STAGE3_EXACT_TARGET_STALE_BASE_AUDIT.json`;
- check wrong-kind refs, bare logical ids, stale fixture leakage, and any compatibility code that silently accepts the old ambiguous form;
- check whether logical lane/claim/occupancy ids become ambiguous under the repaired exact base; preserve a new oracle only if a concrete counterexample exists rather than mass-promoting ids to refs;
- preserve `ADV-024-A`/`ADV-025-A` as separate store-history obligations rather than reopening already-tested store mechanics without new evidence;
- distinguish source inspection, automated evidence owned by Lane 02/CI, inferred risk, and runtime reproduction explicitly;
- do not begin integration-receipt, epoch, or replay repairs early.

## Integrated Stage 3 immutable-store acceptance boundary

The integrated store may currently claim only what the evidence supports:

- immutable persistence of validated canonical objects on the tested local/Linux filesystem path;
- exact lookup by immutable `axmref:v1` under the current schema set;
- immutable persistence of repaired state-revision v0.2 objects;
- idempotent storage of byte-identical content;
- loud failure on exact-reference/content mismatch, non-canonical/corrupt stored bytes, missing refs, or wrong-schema reinterpretation;
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

Additional not-tested/not-proven boundaries:

- forced power-loss durability at every filesystem boundary;
- concurrent multi-process writer stress;
- non-Linux hard-link portability;
- cross-language Stage 2 identity reproduction;
- historical lookup across incompatible schema evolution.

## Next gate — exact lifecycle bases

Decision 006 must be implemented and tested before lifecycle runtime can claim grounded state transitions.

Required relationships:

```text
occupancy base        -> exact immutable state-revision ref
work-claim base       -> exact immutable state-revision ref
return-packet base    -> exact immutable state-revision ref
```

This gate repairs what the lifecycle objects *mean*. It does not itself implement transition policy.

After this gate survives Lane 03 verification, the next smallest Stage 3 slice may create persistent work-ledger/coordination state using the immutable store while keeping transition semantics bounded and explicit.

## Frozen downstream obligations

Before later stages may make stronger claims:

- `ADV-002-C`: artifact provenance base revision must have exact-instance semantics before exact provenance/replay claims;
- `ADV-002-D/E/F`: occupancy, work-claim, and return-packet bases must be exact before lifecycle/stale-base claims — now elevated into Decision 006;
- `ADV-002-G/H`: integration receipts must bind exact base/result state revisions and exact packet instances before integration/replay claims;
- `ADV-011-C/D/E`: epochs must bind an exact base revision and exact packet membership, with exact or uniquely resolvable lane semantics, before parallel/sequential replay claims;
- `ADV-002-I`: selective stale-target compatibility for modified artifacts must derive or record the exact target instance observed from the packet base;
- `ADV-024-A`: durable closure/evidence state must be bound to an exact revision once closure checking can vary historically;
- `ADV-025-A`: historical schema context must be reconstructable before incompatible schema evolution can coexist with replayable immutable history.

These are recorded obligations, not evidence that the corresponding runtimes exist.

## Shared return-packet minimum

Each lane should leave:

- base commit/revision inspected;
- bounded claim;
- files changed;
- evidence/test results;
- uncertainty/blockers;
- dependency/downstream effects;
- next recommended action;
- explicit status such as proposed / implemented / compiled / automated_tested / runtime_tested / measured / inferred / blocked / not_tested.

## Merge boundary

Inside AXM, the four roots remain the constitutional merge gate:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

No lane, founder, model, specialist, schedule position, CI result, or Git permission becomes authority by identity. When evidence is insufficient, preserve uncertainty or dissent instead of converting confidence into canon.
