# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contract layer integrated; Stage 2 identity implementation in bounded portability repair

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable evidence exists.

## Current integration state

- Lane 03 adversarial PR #2 is integrated at `51f93a940e54c19de7d732b5ccb574e95f3a28f3`.
- Lane 01 Decision 001 / first integration wave is integrated at `6c5314d6e2828a32ad9eacd2815a16ed5515a1de`.
- Lane 02 canonical contract PR #3 is integrated at `cff616caf84ded88f79580a51df3e14fdf585b3e`.
- Lane 03 cross-object continuity PR #5 is integrated at `c4904ee7ce508cfa6e1dccacb5f9a6ab2edd379b`.
- Decision 002 defines immutable subject/reference identity requirements.
- Lane 03 Stage 2 canonicalization-oracle PR #6 is integrated at `aaf32fa6d2e3e4f81e80464e051386247b55c83d`.
- Lane 02 reconciled Stage 2 production identity PR #7 remains open at head `f2f10ac03ac832c8962bd3e0a37d76ab15bde923`.
- Lane 03 exact-code portability PR #8 is integrated at `ffacf03d33dd010cd88e11dfb11dc09597fb8900`.
- Decision 003 (`003_CANONICAL_PORTABILITY_SEMANTICS.md`) is integrated and makes the two exact portability repairs normative for Stage 2.
- PR #7's previously reported unchanged-source local evidence remains `21 passed` plus successful `py_compile`; that evidence predates the required portability repair and must not be reused as proof for a changed repair head.
- PR #7 is currently non-mergeable because `main` advanced after its last reconciliation. Treat publication freshness separately from semantic acceptance.
- Stage 2 is **not integrated yet**. The current gate is a minimal Lane 02 repair + fresh deterministic evidence + bounded Lane 03 verification.
- State-store, work-ledger, integration-runtime, and replay complexity remain deferred.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, root boundary, and universal-vs-domain separation;
- hold Stage 2 integration until Decision 003 is encoded and verified;
- keep host-runtime behavior from becoming hidden institutional semantics;
- keep evidence states precise and avoid promoting old test evidence onto changed code;
- maintain repository coordination so later occupants can continue without private chat memory;
- integrate only grounded, non-overlapping specialist work.

Current hold: do not integrate PR #7 until the two exact portability counterexamples are repaired, fresh evidence is recorded for the changed head, Lane 03 verifies the repair, and the branch is reconciled/mergeable.

Avoid duplicating Lane 02's production repair or Lane 03's verification lane.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **repair PR #7 against Decision 003, then reconcile it onto current `main`**.

Immediate next action:

1. keep the existing Stage 2 implementation scope;
2. make object-key ordering explicitly Unicode-scalar-value lexicographic rather than relying on undocumented host default ordering;
3. add the `U+E000` vs `U+10000` regression required by `ADV-021-A`;
4. make `axmref:v1` component encoding explicitly UTF-8 byte based with raw ASCII `A-Z a-z 0-9 - . _ ~` and uppercase `%HH` for every other byte;
5. add the `a!b*a'b(c) -> a%21b%2Aa%27b%28c%29` regression required by `ADV-022-A`;
6. update `IDENTITY_V0.md` so a fresh non-Python implementer can reconstruct both rules without reading Python standard-library behavior;
7. rerun the full deterministic identity suite and compilation checks on the changed head and record exact evidence;
8. reconcile the repaired branch onto current `main` without beginning Stage 3.

Preserve already-grounded Stage 2 properties:

- strict duplicate-key rejection;
- explicit NFC/no-surrogate policy;
- no silent schema-default insertion;
- typed immutable references rather than bare digests;
- logical id distinct from immutable instance identity;
- exact strong-evidence subject binding.

Do **not** start the state store, work ledger, integration engine, model adapter, networking, UI, or Game Studio expansion in this repair.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current claim: **verify the exact repaired PR #7 head after Lane 02 publishes it**.

Integrated exact-code findings:

- `ADV-021-A` — object-key order was under-specified across Unicode scalar vs UTF-16 host sorting;
- `ADV-022-A` — reference percent encoding was under-specified across common host URL encoders.

Negative findings to preserve accurately:

- no current Stage 1 schema `format` keyword was found, so `FormatChecker` is not presently identity-affecting;
- exact strong-evidence binding resisted the mutable-logical-id challenge already covered by `ADV-015-B`.

When Lane 02 repairs PR #7:

- confirm the two Decision 003 witness vectors are encoded in docs/code/tests;
- challenge non-BMP ordering and reference byte spelling on the exact new head;
- confirm fresh test evidence corresponds to the changed blobs;
- do not pull Stage 3 stale-state, lineage, epoch, integration, or replay obligations into this bounded verification;
- if no new failure is found, leave an explicit verification return packet rather than inventing work.

Later integrated oracles that remain out of Stage 2 scope:

- `ADV-002-B` — stale packet/target detection;
- `ADV-011-B` — epoch packet/base coherence and replayable progression;
- `ADV-006-B` — immutable supersession lineage is resolvable and acyclic.

## Coordination cadence

Recommended stagger for recurring activations:

- Lane 01 lead: minute `:57`
- Lane 02 kernel: minute `:12`
- Lane 03 adversarial: minute `:27`

Typical flow:

```text
lead/integration -> kernel implementation -> adversarial challenge -> integration window -> next lead cycle
```

Timing is coordination convenience only and grants no authority.

## Shared return-packet minimum

Each lane should leave:

- base commit/revision inspected;
- bounded claim;
- files changed;
- evidence/test results;
- uncertainty/blockers;
- dependency/downstream effects;
- next recommended action;
- explicit status such as proposed / implemented / automated_tested / runtime_tested / measured / inferred / blocked / not_tested.

## Merge boundary

Inside AXM, the four roots remain the constitutional merge gate:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

No lane, founder, model, specialist, schedule position, or Git permission becomes authority by identity. When evidence is insufficient, preserve uncertainty or dissent instead of converting confidence into canon.
