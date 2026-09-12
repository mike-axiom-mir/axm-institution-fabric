# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts integrated; Stage 2 deterministic identity integrated; Decision 005 revision-membership repair integrated; Stage 3 immutable object-store slice open

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable evidence exists.

## Current integration state

- Stage 1 canonical contract pack is integrated.
- Decisions 001–004 define root-grounded integration semantics, immutable identity/reference semantics, cross-runtime canonical portability, and exact canonical JSON string spelling.
- Lane 02 Stage 2 production identity PR #7 is integrated at `11f8e9035d965aaaf4fe21bc857f1cf01a35ca10` after the bounded adversarial chain through `ADV-023-A`.
- Stage 2 provides strict deterministic parsing, validated canonical bytes, reproducible SHA-256 identity, typed `axmref:v1` immutable references, exact reference resolution, and strong-evidence subject binding.
- Cross-language reproduction of Stage 2 remains not tested.
- Decision 005 (`005_EXACT_REVISION_MEMBERSHIP.md`) is integrated at `c08e24fb1190fb1dfe4cdb083ff64ab4e0b85a69`.
- Lane 03 exact-target/stale-base audit PR #12 is integrated at `4456971da380566b7c3f4aed48381f360b4fb09d`.
- The audit found no conflict with the narrow Decision 005 repair and froze later obligations for exact base/result revision refs, exact packet membership, epoch lane resolution, and selective stale-target compatibility.
- Lane 02 Decision 005 repair PR #11 is integrated at `c09efc390c0b67c7872fc76dd294c8325c8ea7d7`.
- `state-revision.schema.json` is now version `0.2` and binds exact typed immutable refs for parent revision, objective, lanes, occupancies, claims, artifacts, evidence, return packets, and integration receipts.
- PR #11 was reconciled onto the integrated Lane 03 audit without changing its tested schema/fixture/test/workflow blobs. Fresh GitHub Actions run `34712799899` on reconciled head `37d4d570f66d85068a7117f35e2454a296147784` completed successfully for deterministic tests and explicit `py_compile`.
- The earlier exact code/test/workflow commit for the Decision 005 repair reported 34 tests passing. A compare from that tested commit to the reconciled head shows only Lane 02/Lane 03 coordination-return files and the Lane 03 audit fixture were added; the schema/fixture/test/workflow blobs remained unchanged.
- State-store runtime, work-ledger lifecycle, stale-base transition enforcement, supersession graph validation, epoch runtime, integration runtime, and replay are still not implemented.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, root boundary, evidence precision, and universal-vs-domain separation;
- keep Stage 3 claims bounded to storage/exact-lookup behavior actually tested;
- prevent a stored object from being silently promoted into a claim that all of its referenced objects exist or that it is an accepted current/canonical snapshot;
- coordinate Lane 02 store implementation and Lane 03 store-adversarial work without semantic overlap;
- maintain repository state so a later occupant can reconstruct the build without private chat memory.

Current boundary: the Decision 005 prerequisite is cleared. A deliberately small local/offline immutable object store may now be built. Work-ledger/lifecycle/integration/epoch/replay semantics remain held.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **implement the smallest real Stage 3 immutable object-store runtime; do not begin the wider work ledger or transition engine.**

Immediate next action:

1. start from current canonical `main` after PR #11/#12 integration;
2. reuse the integrated Stage 2 validator/canonical-byte/reference implementation instead of inventing a second identity path;
3. implement local/offline immutable persistence for validated canonical objects;
4. make exact lookup accept a typed `axmref:v1` and return only bytes/object content whose recomputed immutable identity exactly matches that ref;
5. make storing the same byte-identical object idempotent;
6. fail loudly if a claimed ref/path and canonical bytes disagree or if stored bytes no longer reproduce the requested ref;
7. ensure an interrupted/partial write cannot become visible through normal exact lookup as a valid canonical object;
8. persist repaired state-revision v0.2 objects through the same identity/store path;
9. keep any mutable convenience pointer/index outside object identity and do not grant it merge/canonical authority;
10. add deterministic tests for write/read identity, idempotence, corruption/mismatch rejection, invalid-object rejection, missing-ref lookup, state-revision persistence, and interrupted-write visibility;
11. record whether state-revision member refs were merely stored as exact names or also proven to exist. Do not call a revision referentially complete unless every member ref has been resolved exactly;
12. stop before implementing claim/occupancy/packet transitions, semantic duplicate-claim handling, stale-base policy, integration receipts, epochs, or replay.

The store may choose a simple filesystem layout. The layout is implementation detail; the invariant is exact immutable identity and visibility behavior, not a particular directory naming scheme.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current claim: **attack the Stage 3 store boundary without editing Lane 02's implementation branch unless a later repair is explicitly opened.**

Immediate next action:

- preserve the integrated `ADV-002-C` through `ADV-002-I` and `ADV-011-C` through `ADV-011-E` as later-stage obligations rather than pulling them into the store prematurely;
- construct store-focused adversarial cases for content/ref mismatch, corruption after write, missing exact refs, idempotent repeat storage, partial/interrupted visibility, and same-logical-id/different-instance coexistence;
- check that a state revision containing exact refs cannot be described as referentially complete merely because the revision object itself was persisted;
- test or inspect whether any mutable `current`/`HEAD` convenience mechanism can rewrite identity, hide history, or act as silent merge authority;
- distinguish observed runtime failures from inferred risks when runtime coverage is not available;
- publish machine-readable or deterministic regression oracles and a bounded return packet;
- do not redesign the store or begin work-ledger/integration semantics in the adversarial lane.

## Stage 3 first runtime slice — acceptance boundary

The first storage slice is deliberately small and local/offline. It may claim only what evidence proves:

- immutable persistence of validated canonical objects;
- exact lookup by immutable `axmref:v1`;
- immutable persistence of repaired state-revision v0.2 objects;
- idempotent storage of byte-identical content;
- loud failure on exact-reference/content mismatch or corrupted content;
- interrupted writes not becoming visible as valid canonical objects;
- any mutable `current`/`HEAD` pointer is navigation only, never identity or merge authority.

Important distinction:

```text
revision object stored
    != all referenced members proven present
    != revision accepted by an integration engine
    != current institutional state
```

If the first store slice does not yet validate full revision-reference closure, preserve that explicitly. A later closure check may promote evidence from “revision bytes stored” to “all named members resolve exactly”; storage alone must not silently do so.

Claim/occupy/return transitions, semantic duplicate-claim handling, stale-base compatibility, integration, epoch progression, and replay remain later slices.

## Frozen downstream obligations from Lane 03 audit

Before later stages may make stronger claims:

- artifact provenance base revision must have exact-instance semantics before exact provenance/replay claims;
- occupancy, work-claim, and return-packet base revisions must have exact-instance semantics before lifecycle/stale-base claims;
- integration receipts must bind exact base/result state revisions and exact packet instances before integration/replay claims;
- epochs must bind an exact base revision and exact packet membership, with exact or uniquely resolvable lane semantics, before parallel/sequential replay claims;
- selective stale-target compatibility for modified artifacts must derive or record the exact target instance observed from the packet base.

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
