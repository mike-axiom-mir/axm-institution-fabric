# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contracts integrated; Stage 2 deterministic identity integrated; exact revision membership integrated; Stage 3 immutable object store integrated; Decision 006 exact lifecycle bases integrated; shared semantic member-ref validation integrated; exact-base exactly-one member resolution integrated; Decision 007 lifecycle chronology integrated; created-after-base authoritative relationship refs are now integrated and adversarially challenged. The next bounded Stage 4 gate is **occupancy admission only**. Claim opening, return submission, successor-revision publication, integration, epochs, and replay remain closed.

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable evidence exists.

## Canonical integration state

- Stage 1 canonical contract pack is integrated.
- Decisions 001–004 define root-grounded integration semantics, immutable identity/reference semantics, cross-runtime canonical portability, and exact canonical JSON string spelling.
- Stage 2 production identity is integrated at `11f8e9035d965aaaf4fe21bc857f1cf01a35ca10` and provides strict deterministic parsing, validated canonical bytes, reproducible SHA-256 identity, typed canonical `axmref:v1` immutable references, exact reference resolution, and strong-evidence subject binding.
- Decision 005 exact revision membership is integrated; `state-revision.schema.json` v0.2 binds typed immutable refs for parent revision, objective, lanes, occupancies, claims, artifacts, evidence, return packets, and integration receipts.
- Stage 3 immutable store is integrated at `cab7ec2daf4d6e5f7ad5fb67c800c99cf14f7859`.
- Decision 006 exact lifecycle-base semantics is integrated through merge commit `4f51dea31bd494099266e0e5a13ab34f1b53958b`.
- Shared semantic state-revision member-ref validation is integrated at `090b8bde1638eacc277f4df27bf3f254b8225e86`.
- The read-only `resolve_exact_revision_member(...)` primitive is integrated through PR #22 / merge commit `c28ca8e67afac1e5bdf0286e0e8b80acb6a851e1` and Lane 03 adversarial regressions through `0dc9745bc3528543d2fb18f0253808399aa6e5af`.
- Decision 007 lifecycle relationship chronology is accepted at `05022e2d9f0d9ebcfcc61afdfcf0e8161e09f731`.
- Decision 007 created-after-base relationship repair is integrated through PR #24 / merge commit `10bc3f9e920e482de82f7c11cc17585d15f10a32`:
  - `work-claim` v0.3 uses exact `occupancy_ref` rather than authoritative logical-only `occupancy_id`;
  - `return-packet` v0.3 uses exact `claim_ref` rather than authoritative logical-only `claim_id`;
  - both route semantic exact-ref validation through the existing Stage 2 parser and enforce the required target kind.
- Lane 02 native CI on the reviewed implementation merge candidate recorded **94 tests passed / 0 failed / 0 errors** plus successful explicit `py_compile`.
- Lane 03 adversarial PR #25 was retargeted onto canonical `main` after PR #24 integration and then integrated as merge commit `2d4a3e9b6ede16b66adf202b69383da307d28c52`.
- The retargeted PR #25 GitHub Actions run `34733412151`, job `103660345672`, checked the canonical-main merge candidate and recorded **100 tests passed / 0 failed / 0 errors**. Its explicit kernel/test `py_compile` step also succeeded.
- Lane 03 found no new blocker on the bounded Decision 007 contract/identity surface. Its regressions prove later same-logical-id occupancy/claim instances and same-id objects already present in the work base cannot silently rebind a persisted claim/return packet.
- `ADV-031-A` is now frozen as a Stage 4 runtime obligation: a future lifecycle transition must exact-load and identity-verify `occupancy_ref` / `claim_ref` targets before treating those relationships as operationally valid. Persisting a referring object alone is not target-existence or closure evidence.
- There are currently no open pull requests.

## Integrated identity / chronology boundary

The institution may currently rely on these grounded relationship rules:

```text
pre-existing-at-base target
    -> exact base revision
    -> explicit member family / required kind
    -> exactly one logical-id match
    -> return that exact immutable member
    -> zero / multiple / missing / corrupt => explicit failure

created-after-base authoritative target
    -> bind exact immutable target ref directly
    -> canonical Stage 2 parser + required kind
    -> future transition must exact-load target before operational use
```

Forbidden hidden authority remains:

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

Important distinction:

```text
valid referring object
    != referenced target exists
    != relation-specific transition is valid
    != object is canonical/current institutional state
    != successor revision has been published
```

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, roots, evidence precision, and universal-vs-domain separation;
- treat Decision 007 post-base exact refs as integrated only on their tested contract/identity surface;
- preserve `ADV-031-A` as an explicit transition-time target verification obligation;
- open only the smallest first Stage 4 mutation slice: occupancy admission;
- keep claim opening, packet submission, successor-revision publication, integration, epoch runtime, and replay closed until occupancy admission survives deterministic and adversarial evidence;
- keep `ADV-024-A`, `ADV-025-A`, provenance, stale-target, integration-receipt, epoch, portability, and cross-language obligations explicit;
- maintain repository state so another occupant can reconstruct the build without private chat memory.

Current boundary: exact post-base relationship identity is integrated. The first actual lifecycle transition may now begin, but only for occupancy admission and only using the already accepted pre-base lane relationship from Decision 007.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **implement only the first Stage 4 occupancy-admission primitive; do not open claims, return packets, successor revisions, integration, epochs, or replay.**

Immediate next action:

1. start from current canonical `main` after PR #24/#25 integration;
2. add the smallest explicit occupancy-admission runtime surface, with a narrow name such as `admit_occupancy(...)` rather than a generic lifecycle engine;
3. accept an occupancy object intended for creation plus the immutable store/context required to verify it;
4. validate the occupancy through the existing contract/semantic boundary;
5. exact-load `occupancy.base_state_revision_ref` as a `state-revision`;
6. resolve `occupancy.lane_id` only through `resolve_exact_revision_member(...)` using `lane_refs` / required kind `lane` against that exact entry base;
7. require exactly one matching lane; zero, multiple, missing, corrupt, wrong-base-kind, malformed-ref, and noncanonical-ref cases must fail explicitly;
8. do not consult a newer revision, store recency, array order, actor identity, capability identity, schedule position, `current`/`HEAD`, founder status, or chat state to pick a lane;
9. when admission succeeds, persist the exact occupancy object immutably and return a bounded result containing at least the stored occupancy exact ref plus the exact resolved lane ref; do **not** claim this makes the occupancy current/canonical institutional state;
10. preserve the current `claim_ids` field as snapshot/navigation data only; do not create claims or infer claim history;
11. test that two same-logical-id lane instances in the exact base make admission fail rather than choose one;
12. test that a newer same-id lane elsewhere in storage cannot override the exact base;
13. test missing/corrupt exact members and invalid/missing exact bases through the real store path;
14. test that successful admission exact-loads the named base and resolves the exact lane identity actually present there;
15. test that the persisted occupancy has unchanged exact identity when reloaded and that no successor revision is silently synthesized;
16. include the new runtime/test module in explicit compile coverage;
17. rerun the complete deterministic suite, publish a bounded return packet, and stop.

This slice proves admission mechanics only. It must not invent stale-base policy, occupancy supersession/currentness, actor authorization, capability authorization, user delegation, scheduler semantics, claim opening, or revision publication without separate evidence.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current claim: **wait for Lane 02's concrete occupancy-admission head, then attack that exact implementation without expanding production behavior.**

Immediate adversarial focus once the head exists:

- exact-base lane ambiguity under member-array reordering;
- zero-match lane resolution;
- newer same-id lane elsewhere in the store;
- missing/corrupt lane members in the selected family;
- missing/corrupt/wrong-kind/noncanonical base revision refs;
- actor/capability identity attempting to become hidden lane-selection authority;
- accidental fallback to recency/current/HEAD/schedule/private-chat state;
- a successful admission being falsely described as successor-revision publication or canonical-current state;
- mutation after persistence or exact-ref/content mismatch;
- preservation of `claim_ids` as non-authoritative snapshot/navigation state;
- evidence distinction between stored occupancy, admitted relationship, canonical successor state, and later claim-opening behavior.

Do not implement claim opening, packet submission, successor revision publication, integration, epochs, or replay in the adversarial branch.

## Active Stage 4 gate — occupancy admission only

Grounded chronology:

```text
exact entry base N already exists
    lane L must already exist in N
    -> occupancy O names lane logical id L
    -> resolve exactly one lane instance inside N
    -> verify exact resolved lane
    -> persist exact occupancy O
```

Success may claim only:

```text
occupancy contract/semantic validity
+ exact base exists and is loadable
+ occupancy lane resolves exactly once inside that base
+ exact occupancy object is immutably persisted
+ exact resolved lane identity is returned/preserved
```

Success must **not** claim:

```text
occupancy is now canonical/current institutional state
successor state revision exists
claim ledger exists
claim opened
return packet accepted
artifact/dependency mutation occurred
integration happened
epoch/barrier happened
replay proof exists
```

## Frozen downstream obligations

- `ADV-002-C`: artifact provenance base revision must have exact-instance semantics before exact provenance/replay claims.
- `ADV-002-G/H`: integration receipts must bind exact base/result state revisions and exact packet instances before integration/replay claims.
- `ADV-011-C/D/E`: epochs must bind an exact base revision and exact packet membership, with exact or uniquely resolvable lane semantics, before parallel/sequential replay claims.
- `ADV-002-I`: selective stale-target compatibility for modified artifacts must derive or record the exact target instance observed from the packet base.
- `ADV-024-A`: durable closure/evidence state must be bound to an exact revision once closure checking can vary historically.
- `ADV-025-A`: historical schema context must be reconstructable before incompatible schema evolution can coexist with replayable immutable history.
- `ADV-031-A`: authoritative post-base refs must be exact-loaded/identity-verified at transition time before operational relationship claims.
- `occupancy.claim_ids`: snapshot/chronology semantics remain unresolved; do not use as exact dereference authority yet.
- `work-claim.overlap_with_claim_ids`: report/navigation semantics remain unresolved; do not use as exact dereference authority yet.
- lifecycle successor-revision publication remains unimplemented and must not be implied by immutable object persistence.
- full cross-language reproduction of the identity/resolution stack remains not tested.
- filesystem power-loss durability, concurrent-writer stress, and non-Linux atomic-publication behavior remain not fully proven.

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
