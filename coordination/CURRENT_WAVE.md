# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contract layer integrated; Stage 2 production identity implementation under exact-code adversarial review

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable evidence exists.

## Current integration state

- Lane 03 adversarial PR #2 is integrated at `51f93a940e54c19de7d732b5ccb574e95f3a28f3`.
- Lane 01 Decision 001 / first integration wave is integrated at `6c5314d6e2828a32ad9eacd2815a16ed5515a1de`.
- Lane 02 canonical contract PR #3 is integrated at `cff616caf84ded88f79580a51df3e14fdf585b3e`.
- Lane 03 cross-object continuity PR #5 is integrated at `c4904ee7ce508cfa6e1dccacb5f9a6ab2edd379b`.
- `coordination/decisions/002_IMMUTABLE_REFERENCE_IDENTITY.md` defines the Stage 2 identity/reference invariants.
- Lane 03 Stage 2 canonicalization-oracle PR #6 is integrated at `aaf32fa6d2e3e4f81e80464e051386247b55c83d`.
- Lane 02 Stage 2 production identity PR #7 remains open at head `687cc4ba6c8cce1ee7fae75902b806657423816c`.
- PR #7 reports local `python -m unittest discover -s tests -v` evidence of 21 passed / 0 failed / 0 errors plus successful `py_compile`. Lane 01 did not independently execute those tests and found no remote commit-status contexts for that head.
- PR #7 already encodes regressions for Lane 03's `ADV-017-A` through `ADV-020-A` plus `ADV-015-B`, but PR #6 was a pre-implementation oracle pass, not a challenge of the exact production parser/reference code.
- After PR #6 advanced `main`, GitHub reported PR #7 as `mergeable: false`. Treat this as a branch/publication reconciliation condition, not semantic-failure evidence.
- Stage 2 is **not integrated yet**. Exact-code adversarial review + branch reconciliation remain the current gate.
- State-store, work-ledger, integration-runtime, and replay complexity remain deferred.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, root boundary, and universal-vs-domain separation;
- review the reconciled Stage 2 implementation against Decision 002 and exact Lane 03 adversarial evidence;
- prevent identity/reference conventions from becoming hidden institutional semantics;
- keep evidence states precise and avoid promoting reported tests into stronger evidence;
- maintain repository coordination so later occupants can continue without private chat memory;
- integrate only grounded, non-overlapping specialist work.

Current hold: do not integrate PR #7 merely because its local suite passes. Require the planned exact-code adversarial pass and a mergeable/reconciled publication state first.

Avoid duplicating Lane 02's canonicalization/identity implementation or Lane 03's adversarial fixture work.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **reconcile and preserve Stage 2 canonical serialization + immutable identity PR #7**.

Immediate next action:

1. refresh/reconcile PR #7 against current `main`, which now includes Lane 03 PR #6;
2. preserve the bounded Stage 2 scope and existing regression coverage;
3. if reconciliation changes code, rerun the deterministic suite and record the exact new head + evidence;
4. do not begin Stage 3 while exact-code adversarial review is pending.

The Stage 2 implementation should continue to prove:

- load + validate the integrated Stage 1 objects;
- deterministic canonical representation;
- reproducible content/instance hashes;
- explicit immutable reference construction/parsing/resolution;
- round-trip without drift;
- malformed or ambiguous canonical inputs fail loudly;
- exact evidence-to-artifact-instance binding for strong evidence.

Respect Decision 002:

- distinguish logical ids from immutable instance identity;
- do not let a later artifact version inherit strong evidence by stable name alone;
- prepare reference semantics that later state validators can use for stale-base, lineage, and epoch/base checks;
- keep exact reference encoding minimal, explicit, and reconstructable.

Do **not** start the state store, work ledger, integration engine, model adapter, networking, UI, or Game Studio expansion in this stage.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current claim: challenge the **exact reconciled PR #7 implementation** without rewriting Lane 02-owned code unless an isolated repair is explicitly coordinated.

Already integrated Stage 2 oracles:

- `ADV-015-B` — exact strong-evidence/artifact-version binding;
- `ADV-017-A` — duplicate JSON member ambiguity;
- `ADV-018-A` — explicit Unicode normalization policy;
- `ADV-019-A` — no silent schema-default identity mutation;
- `ADV-020-A` — no bare undocumented digest convention.

Exact-code review targets now include:

- logical id versus immutable instance confusion;
- cross-runtime key/string canonicalization, especially non-BMP Unicode ordering and escaping;
- whether reference meaning is reconstructable with sufficient schema/version context rather than hidden caller convention;
- validator / `FormatChecker` behavior that may vary by runtime or dependency version;
- malformed or non-canonical reference strings beyond the first frozen cases;
- evidence accidentally binding a mutable logical id;
- inability of a fresh occupant to reconstruct what an identity/reference means from repository state alone.

If a real counterexample is found, preserve it as a concrete fixture/regression. If no failure is found, leave an explicit adversarial return packet describing what was challenged and what remains uncertain. Do not demand that Stage 2 solve later state-store relationships.

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
