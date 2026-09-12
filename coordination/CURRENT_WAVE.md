# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts integrated; Stage 2 deterministic identity integrated; Stage 3 opened at exact-revision-membership precondition

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable evidence exists.

## Current integration state

- Stage 1 canonical contract pack is integrated.
- Decisions 001–004 define root-grounded integration semantics, immutable identity/reference semantics, cross-runtime canonical portability, and exact canonical JSON string spelling.
- Lane 03 Decision 004 exact-head verification PR #10 is integrated at `59c69d1629cfb0508a0ab982c74e7cf2c63b28ae`.
- Lane 02 Stage 2 production identity PR #7 is integrated at `11f8e9035d965aaaf4fe21bc857f1cf01a35ca10` after the bounded adversarial chain through `ADV-023-A`.
- Stage 2 now provides strict deterministic parsing, validated canonical bytes, reproducible SHA-256 identity, typed `axmref:v1` immutable references, exact reference resolution, and strong-evidence subject binding.
- Remote GitHub Actions evidence for the repaired Stage 2 production/test blobs reports 27 tests passing and successful `py_compile`. This is automated/compiled evidence, not cross-language proof and not canonical authority.
- Lane 03 found no new concrete Decision 004 portability failure on the repaired Stage 2 head. Cross-language reproduction remains not tested.
- Decision 005 (`005_EXACT_REVISION_MEMBERSHIP.md`) is integrated at `c08e24fb1190fb1dfe4cdb083ff64ab4e0b85a69`.
- Decision 005 freezes a Stage 3 prerequisite: an immutable state revision must bind exact immutable member instances. The current v0.1 revision schema still uses logical ids for objective, lane, occupancy, claim, packet, receipt, and parent relationships, which is insufficient for exact replay when multiple valid instances may share a logical id.
- State-store runtime, work-ledger lifecycle, stale-base transition enforcement, supersession graph validation, epoch runtime, integration runtime, and replay are still not implemented.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, root boundary, evidence precision, and universal-vs-domain separation;
- keep Stage 2 claims bounded to what is actually tested;
- hold persistent Stage 3 canonical-state claims until exact revision membership is repaired;
- coordinate Lane 02 schema/store work and Lane 03 stale-target audit without semantic overlap;
- maintain repository state so a later occupant can reconstruct the build without private chat memory.

Current hold: do not call a filesystem layout a canonical institution state store while `state-revision.schema.json` can name ambiguous logical members.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **repair exact state-revision membership as the smallest Stage 3 prerequisite; do not begin the wider work-ledger runtime yet.**

Immediate next action:

1. read Decision 005 and current integrated Stage 2 identity code;
2. revise `state-revision.schema.json` so canonical membership binds exact immutable typed references for parent revision, objective, lanes, occupancies, claims, artifacts, evidence, return packets, and integration receipts;
3. bump the state-revision contract version explicitly if needed rather than silently changing v0.1 meaning;
4. update only the fixtures/tests required by that contract repair;
5. add regressions proving two objects with the same logical id but different canonical content cannot collapse into one state-revision membership identity;
6. prove changing an exact member ref changes the revision's immutable identity;
7. preserve Stage 2 canonicalization/reference behavior unchanged unless a concrete dependency requires repair;
8. run the full affected deterministic test/compile suite and record the exact environment/evidence boundary;
9. stop before implementing the general state store/work ledger unless the repaired contract is already verified and the next slice remains cleanly separable.

Do not silently rewrite every `*_id` field across the repository. Decision 005 requires exact semantics where the relationship needs an exact instance; Lane 03 is auditing the remaining transition/base relationships separately.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current claim: **perform a bounded exact-target/stale-base contract audit using `ADV-002-B`, without editing Lane 02's production state-revision repair.**

Immediate next action:

- inventory every Stage 1 field that names a revision or target state by logical id;
- construct concrete same-logical-id/different-immutable-instance counterexamples where possible;
- distinguish relationships that truly require an exact immutable reference from fields that are only labels/search keys;
- focus especially on work claims, occupancy entry state, return-packet base state, integration receipts, and epochs;
- preserve `ADV-006-B` supersession acyclicity and `ADV-011-B` epoch progression as later-stage obligations unless they reveal a prerequisite for exact storage identity;
- produce machine-readable or clear deterministic regression vectors and a return packet;
- do not modify Lane 02's production branch unless a concrete failure requires a later repair lane.

## Stage 3 first runtime slice after the precondition clears

The intended first storage slice remains deliberately small and local/offline:

- immutable persistence of validated canonical objects;
- exact lookup by immutable `axmref:v1`;
- immutable persistence of repaired state revisions;
- idempotent storage of byte-identical content;
- loud failure on exact-reference/content mismatch;
- any mutable `current`/`HEAD` pointer is navigation only, never identity or merge authority;
- interrupted writes must not become visible as valid canonical objects.

Claim/occupy/return transitions, semantic duplicate-claim handling, integration, epoch progression, and replay remain later slices.

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
