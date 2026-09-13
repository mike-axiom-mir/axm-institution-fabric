# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts integrated; Stage 2 deterministic identity integrated; exact revision membership integrated; Stage 3 immutable object store integrated; Decision 006 exact lifecycle-base contracts integrated. Lane 02 PR #19 repairs the concrete `ADV-029-A/B` spelling witnesses, but Lane 03 Activation 013 found broader semantic parser-equivalence gaps `ADV-030-A/B`. Stage 4 lifecycle/work-ledger runtime remains closed until exact revision-member validation uses the same semantic reference language as Stage 2.

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
- Lane 02 PR #19 (`lane-02/activation-12-revision-member-canonicality`) is open and currently held. Its tested implementation head `74fbe01970fa90fe9421006351bd1d95d14e6697` directly repairs `ADV-029-A/B`: percent-encoded RFC3986-unreserved spellings such as `%2E`, `$`/final-LF end-anchor behavior, and bounded malformed-member store rejection.
- Native GitHub Actions run `34724879851` on that tested head concluded success; Lane 02 recorded **62 deterministic tests passing** plus successful explicit Python compilation. The final PR #19 head `880a6dc8b1ce47f5c6c3866f2ba6c64c03028ae3` adds only its Lane 02 return packet after the tested implementation head.
- Lane 03 Activation 013 exact-head challenge found two remaining semantic discontinuities and published evidence-only PR #20. PR #20 was integrated into `main` as merge commit `ba38816469b8164cabef4f8e4db270d178646347`.
- `ADV-030-A`: PR #19 state-revision exact-member regexes still accept percent-byte sequences that are not valid UTF-8, e.g. `%FF`, while Stage 2 `_decode_component()` / `parse_immutable_ref()` rejects them.
- `ADV-030-B`: the same regexes accept valid UTF-8 percent spellings whose decoded text is not NFC, e.g. `e%CC%81`, while Stage 2 rejects the non-NFC component. NFC-equivalent `é` is canonically `%C3%A9`.
- Both `ADV-030` witness classes apply to logical-id and version components and to all nine state-revision exact-member field families because they share the same regex component language.
- Lane 03 bounded reproduction used the PR #19 regex and current Stage 2 semantic decoding under CPython 3.13.5 / jsonschema 4.26.0. Lane 03 did not independently rerun the complete 62-test suite and did not runtime-execute the full object-store witness; those evidence boundaries remain explicit.
- `ADV-027-A/B/C` remain frozen downstream obligations: an exact base revision may contain multiple exact lane/occupancy/claim instances sharing one logical id. Before Stage 4 runtime dereferences those ids, the relationship needs a machine-checkable exactly-one base-local resolution invariant or an exact-instance relationship.
- Work-ledger persistence/coordination, claim/occupancy/return transitions, semantic duplicate-claim handling, stale-base runtime, supersession graph validation, integration runtime, epoch runtime, and replay are still not implemented.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, roots, evidence precision, and universal-vs-domain separation;
- keep Stage 3 store claims bounded to tested behavior;
- preserve `ADV-024-A` and `ADV-025-A` without silently promoting them to solved or prematurely overbuilding them;
- treat Decision 006 as integrated on its tested/adversarially reviewed surface;
- hold PR #19 until `ADV-030-A/B` are repaired and independently challenged;
- prefer one semantic immutable-reference validator over indefinitely duplicating Stage 2 UTF-8/NFC/canonicality semantics in regular expressions;
- preserve `ADV-027-A/B/C` as the next relationship-resolution gate rather than silently selecting by array order, recency, mutable current state, or hidden chat;
- keep repository state reconstructable without private chat memory.

Current boundary: immutable storage and exact lifecycle-base contracts are integrated. Exact revision-member **semantic parser equivalence** is the active prerequisite. Lifecycle transition runtime remains closed.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **repair `ADV-030-A/B` on PR #19 without beginning lifecycle/work-ledger runtime.**

Immediate next action:

1. start from the current PR #19 repair and reconcile onto current canonical `main` after Lane 03 evidence integration;
2. preserve the existing `ADV-029-A/B` fixes and all 62-test behavior;
3. avoid growing the schema regex into a second Unicode/normalization parser unless evidence proves that is the smaller, safer invariant;
4. reuse Stage 2 `parse_immutable_ref()` semantics, or one shared semantic validator built from the same implementation, for every state-revision exact-member reference;
5. enforce the field-required kind (`state-revision`, `objective`, `lane`, `occupancy`, `work-claim`, `artifact`, `evidence`, `return-packet`, `integration-receipt`) after semantic parsing;
6. add regressions for invalid UTF-8 percent bytes such as `%FF` in both logical-id and version components;
7. add regressions for valid UTF-8 but non-NFC components such as `e%CC%81` in both logical-id and version components, while preserving canonical NFC positives such as `%C3%A9`;
8. route the bounded store-facing state-revision validation path through the same semantic member-ref check so malformed refs fail before publication, without claiming member existence/closure;
9. rerun the complete deterministic suite and explicit compile step on the exact repaired/reconciled head;
10. publish a bounded return packet and stop before `ADV-027` relationship resolution, transitions, stale-base policy, integration receipts, epochs, or replay.

Do **not** mass-convert logical/navigation ids in this repair. `ADV-027-A/B/C` belongs to the later runtime relationship that actually dereferences them.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current claim: **wait for Lane 02's concrete `ADV-030-A/B` repair, then attack that exact repaired head only.**

Immediate next action once the repair exists:

- verify the original `ADV-029-A/B` witnesses remain rejected;
- verify invalid UTF-8 percent sequences are rejected in logical-id and version components;
- verify valid UTF-8 but non-NFC components are rejected unchanged while canonical NFC spellings remain accepted;
- verify every accepted member ref parses unchanged through the shared Stage 2 semantic path and matches the field-required kind;
- verify malformed member refs cannot enter the immutable store through normal state-revision validation while keeping missing-reference/closure checks separate;
- verify Decision 006 lifecycle-base behavior remains intact;
- check that no mutable/current lookup, hidden normalization, recency selection, or Stage 4 runtime was introduced;
- preserve `ADV-024-A`, `ADV-025-A`, `ADV-027-A/B/C`, provenance, receipt, epoch, selective-stale-target, and replay obligations without pulling them into this bounded repair;
- distinguish observed/runtime-tested evidence from inferred risks and do not relabel Lane 02 CI as independent Lane 03 execution.

## Integrated Stage 3 immutable-store acceptance boundary

The integrated store may currently claim only:

- immutable persistence of validated canonical objects on the tested local/Linux filesystem path;
- exact lookup by canonical immutable `axmref:v1` under the current schema/semantic validation set;
- immutable persistence of state-revision v0.2 objects;
- idempotent storage of byte-identical content;
- loud failure on exact-reference/content mismatch, corrupt/non-canonical stored bytes, missing refs, or wrong-schema reinterpretation;
- interrupted pre-publication temp bytes do not become visible through normal exact lookup in the tested implementation;
- same logical id may coexist as multiple exact immutable instances;
- no mutable `current`/`HEAD` pointer exists in this slice.

Important distinction:

```text
revision object stored
    != every nested member reference proven semantically parser-canonical until ADV-030 is repaired
    != all referenced members proven present
    != durable closure-check evidence exists
    != revision accepted by an integration engine
    != current institutional state
```

Not tested/not proven: forced power-loss durability at every filesystem boundary; concurrent multi-process writer stress; non-Linux hard-link portability; cross-language full identity reproduction; historical lookup across incompatible schema evolution.

## Active gate — exact revision-member semantic canonicality

Required equivalence:

```text
state-revision member ref accepted by contract/runtime validation
    -> same bytes accepted unchanged by Stage 2 parse_immutable_ref
    -> decoded components satisfy strict UTF-8 + canonical text/NFC requirements
    -> parsed kind matches the field-required kind
```

and:

```text
noncanonical spelling / invalid UTF-8 / non-NFC / trailing data
    -> rejected before canonical state-revision persistence
```

This gate is about the exact reference language, not reference existence/closure. A parser-canonical member ref may still name a missing object; that remains a separate later truth state.

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
