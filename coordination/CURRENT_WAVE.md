# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts integrated; Stage 2 deterministic identity integrated; exact revision membership integrated; Stage 3 immutable object store integrated; Decision 006 exact lifecycle-base contracts integrated. The next active prerequisite is `ADV-029-A/B`: state-revision exact-member fields must accept the same canonical immutable-reference language as Stage 2 parsing before Stage 4/5 runtime dereferences revision membership.

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable evidence exists.

## Current integration state

- Stage 1 canonical contract pack is integrated.
- Decisions 001–004 define root-grounded integration semantics, immutable identity/reference semantics, cross-runtime canonical portability, and exact canonical JSON string spelling.
- Stage 2 production identity is integrated at `11f8e9035d965aaaf4fe21bc857f1cf01a35ca10` and provides strict deterministic parsing, validated canonical bytes, reproducible SHA-256 identity, typed canonical `axmref:v1` immutable references, exact reference resolution, and strong-evidence subject binding.
- Cross-language reproduction of the full Stage 2 identity algorithm remains not tested.
- Decision 005 exact revision membership is integrated; `state-revision.schema.json` v0.2 binds typed immutable refs for parent revision, objective, lanes, occupancies, claims, artifacts, evidence, return packets, and integration receipts.
- Lane 02 Stage 3 immutable store PR #13 is integrated at `cab7ec2daf4d6e5f7ad5fb67c800c99cf14f7859`. Reviewed evidence recorded 45 deterministic tests passing plus successful explicit `py_compile` on the reviewed head.
- The store provides local/offline immutable persistence for validated canonical objects, exact lookup, idempotent repeat storage, corruption/content-ref mismatch rejection, missing-ref failure, same-logical-id/different-instance coexistence, and tested atomic publication behavior on the Linux runner.
- The store does **not** imply work-ledger lifecycle, stale-base enforcement, integration, epochs, replay, reference closure, or current/canonical-state authority.
- `ADV-024-A` remains explicit: `StoreWriteResult.referenced_members_verified=False` is transient call state, not a durable closure receipt.
- `ADV-025-A` remains explicit: historical lookup currently revalidates bytes against the schema occupying the current stable schema filename. Historical readability across an incompatible schema migration is not generally proven.
- Decision 006 exact lifecycle-base semantics is integrated.
- Lane 02 PR #15 is integrated at merge commit `4f51dea31bd494099266e0e5a13ab34f1b53958b` after the repaired exact head `eb84ed937a31fcb7b5dfa6d7003e0b8b17b99676` survived Lane 03 exact-head challenge.
- PR #15 now binds `occupancy.base_state_revision_ref`, `work-claim.base_state_revision_ref`, and `return-packet.base_state_revision_ref` to exact canonical immutable state-revision refs and preserves rejection of bare logical ids, wrong-kind refs, legacy fields, noncanonical percent-encoded unreserved bytes, and trailing-data/final-LF witnesses.
- Lane 02 native GitHub Actions run `34722324680` on the tested code/workflow head `43c6c40e016b08bbf48eacf9d1b8c08325ac5439` completed successfully: **58 tests passed / 0 failed / 0 errors**, and explicit `py_compile` succeeded. The final PR head added only the Lane 02 return packet after that tested head.
- Lane 03 Activation 012 found no new counterexample on the repaired Decision 006 surface and found no mutable/current lookup or Stage 4 runtime added by PR #15.
- Lane 03 also found the separate already-integrated Decision 005 defect `ADV-029-A/B` in state-revision member-reference fields. Its exact evidence files were copied unchanged onto canonical `main` as `ef37b1472700f0b42e9788482a2ba9fa930b5db6` and `56c617ddd681d8430f3b4020b5ba2eddcb531611`; evidence-only PR #18 was then closed to avoid duplicate integration.
- `ADV-029-A`: state-revision member-ref patterns currently accept noncanonical percent spellings such as `%2E` for literal `.`, while Stage 2 `parse_immutable_ref()` rejects the same spelling.
- `ADV-029-B`: state-revision member-ref patterns still use `$`, so under the repository's Python/jsonschema semantics one final LF may validate while Stage 2 parsing rejects the same value.
- The affected surface includes `parent_revision_ref`, `objective_ref`, and all exact member-ref arrays. This is a canonical-language defect before reference-closure or missing-object questions are considered.
- Lane 03 did not runtime-execute the malformed-member store witness; persistence of the exact witness remains inferred from inspected store/schema behavior, not independently measured.
- `ADV-027-A/B/C` remain frozen downstream obligations: an exact base revision may contain multiple exact lane/occupancy/claim instances sharing one logical id. Before Stage 4 runtime dereferences those ids, the relationship needs a machine-checkable exactly-one base-local resolution invariant or an exact-instance relationship.
- Work-ledger persistence/coordination, claim/occupancy/return transitions, semantic duplicate-claim handling, stale-base runtime, supersession graph validation, integration runtime, epoch runtime, and replay are still not implemented.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, roots, evidence precision, and universal-vs-domain separation;
- keep Stage 3 store claims bounded to tested behavior;
- preserve `ADV-024-A` and `ADV-025-A` without silently promoting them to solved or prematurely overbuilding them;
- treat Decision 006 as integrated on its tested/adversarially reviewed surface;
- hold Stage 4 lifecycle/work-ledger runtime until `ADV-029-A/B` is repaired and independently challenged;
- preserve `ADV-027-A/B/C` as the next relationship-resolution gate rather than silently selecting by array order, recency, mutable current state, or hidden chat;
- keep repository state reconstructable without private chat memory.

Current boundary: immutable storage and exact lifecycle-base contracts are integrated. The next smallest prerequisite is canonical-language equivalence for exact revision membership. Lifecycle transition runtime remains closed.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **repair `ADV-029-A/B` narrowly in `state-revision.schema.json`; do not begin lifecycle/work-ledger runtime.**

Immediate next action:

1. start from current canonical `main` after PR #15 integration and Lane 03 Activation 012 evidence integration;
2. make every exact state-revision member field accept only canonical `axmref:v1` spellings that Stage 2 `parse_immutable_ref()` accepts unchanged for that field's required kind;
3. reject noncanonical percent-encoding of RFC3986-unreserved bytes such as `%2E` across parent/objective/member-array refs;
4. replace `$`-dependent end behavior on the affected exact-member patterns with true complete-string semantics consistent with the repaired Decision 006 boundary;
5. preserve required kinds, currently permitted version semantics, exact digest spelling, duplicate-ref rejection, and Decision 005 same-logical-id/different-instance behavior;
6. add direct regressions for `ADV-029-A/B` on every affected field family, including canonical positive refs, `%2E`/unreserved-percent negatives, final-LF/trailing-data negatives, and parser-equivalence assertions;
7. add a bounded store-facing regression proving a malformed exact-member state revision is rejected before persistence, without claiming member-reference closure;
8. rerun the complete deterministic suite and explicit compile step on the exact repaired head;
9. publish a bounded return packet and stop before base-local lane/occupancy/claim resolution, transitions, stale-base policy, integration receipts, epochs, or replay.

Do **not** mass-convert logical/navigation ids in this repair. `ADV-027-A/B/C` belongs to the later runtime relationship that actually dereferences them.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current claim: **wait for Lane 02's concrete `ADV-029-A/B` repair, then attack that exact repaired head only.**

Immediate next action once a repair branch exists:

- verify `%2E` and every covered percent-encoded unreserved witness is rejected in affected state-revision member fields;
- verify final LF and ordinary trailing data are rejected with true complete-string semantics;
- verify canonical positive member refs remain accepted and parse unchanged with the field-required kind;
- verify malformed member refs cannot enter the immutable store through state-revision validation, while keeping missing-reference/closure checks explicitly separate;
- verify Decision 006 lifecycle-base behavior remains intact;
- check that no mutable/current lookup, hidden normalization, recency selection, or Stage 4 runtime was introduced;
- preserve `ADV-024-A`, `ADV-025-A`, `ADV-027-A/B/C`, provenance, receipt, epoch, selective-stale-target, and replay obligations without pulling them into this bounded repair;
- distinguish observed/runtime-tested evidence from inferred risks and do not relabel Lane 02 CI as independent Lane 03 execution.

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
    != every nested member string is currently parser-canonical until ADV-029 is repaired
    != all referenced members proven present
    != durable closure-check evidence exists
    != revision accepted by an integration engine
    != current institutional state
```

Not tested/not proven: forced power-loss durability at every filesystem boundary; concurrent multi-process writer stress; non-Linux hard-link portability; cross-language full identity reproduction; historical lookup across incompatible schema evolution.

## Active gate — exact revision-member canonicality

Required equivalence:

```text
state-revision member ref accepted by contract
    -> same bytes accepted unchanged by Stage 2 parse_immutable_ref
    -> parsed kind matches the field-required kind
```

and:

```text
noncanonical spelling / trailing data
    -> rejected at the state-revision contract boundary
    -> cannot become a persisted canonical state-revision object through normal store validation
```

This gate is about canonical reference language, not reference existence/closure. A parser-canonical member ref may still name a missing object; that remains a separate later truth state.

Only after this repaired surface survives fresh deterministic evidence and Lane 03 exact-head challenge may Lane 01 open the next smallest Stage 4 relationship/lifecycle slice.

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
