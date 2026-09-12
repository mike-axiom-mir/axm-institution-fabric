# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contract layer integrated; Stage 2 identity work active

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable evidence exists.

## Current integration state

- Lane 03 adversarial PR #2 is integrated at `51f93a940e54c19de7d732b5ccb574e95f3a28f3`.
- Lane 01 Decision 001 / first integration wave is integrated at `6c5314d6e2828a32ad9eacd2815a16ed5515a1de`.
- Lane 02 canonical contract PR #3 is integrated at `cff616caf84ded88f79580a51df3e14fdf585b3e`.
- Lane 03 cross-object continuity PR #5 is integrated at `c4904ee7ce508cfa6e1dccacb5f9a6ab2edd379b`.
- `coordination/decisions/002_IMMUTABLE_REFERENCE_IDENTITY.md` now defines the Stage 2 identity/reference invariants.
- Stage 1 is frozen enough to build on at the **contract layer**: ten v0 object schemas, explicit schema versioning, epoch/barrier shape, Decision 001 receipt semantics, and named adversarial regression fixtures are integrated.
- Stage 1 is not a functioning institution proof. Lane 02 reports a local deterministic contract suite of 7 passed / 0 failed / 0 errors; no GitHub Actions run was found for that head and Lane 01 did not independently execute the suite.
- Stage 2 is now the active build boundary: canonical serialization + immutable identity only. State-store, work-ledger, integration-runtime, and replay complexity remain deferred.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, root boundary, and universal-vs-domain separation;
- review Stage 2 implementation against Decision 002 and the integrated adversarial oracles;
- prevent identity/reference conventions from becoming hidden institutional semantics;
- keep evidence states precise and avoid promoting reported tests into stronger evidence;
- maintain repository coordination so later occupants can continue without private chat memory;
- integrate only grounded, non-overlapping specialist work.

Avoid duplicating Lane 02's canonicalization/identity implementation or Lane 03's adversarial fixture work.

## Lane 02 — Deterministic Kernel Engineer

Current next claim: **Stage 2 canonical serialization + immutable identity**.

Implement the smallest production identity layer that can:

1. load + validate the integrated Stage 1 objects;
2. produce deterministic canonical representation;
3. derive reproducible content/instance hashes;
4. construct and parse explicit immutable references;
5. round-trip supported objects without drift;
6. reject malformed or ambiguous canonical input rather than silently changing meaning;
7. prove at least one exact evidence-to-artifact-instance binding regression.

Respect Decision 002:

- distinguish logical ids from immutable instance identity;
- do not let a later artifact version inherit strong evidence by stable name alone;
- prepare reference semantics that later state validators can use for stale-base, lineage, and epoch/base checks;
- keep exact reference encoding minimal and explicit.

Do **not** start the state store, work ledger, integration engine, model adapter, networking, UI, or Game Studio expansion in this stage.

Required evidence before Stage 2 integration review:

- exact tests and results;
- same supported input -> same canonical bytes/hash;
- round-trip without drift;
- ambiguous/malformed canonical inputs fail loudly;
- immutable refs resolve the intended exact instance in fixture tests;
- explicit truth boundary for what remains cross-object/state validation.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current next claim: challenge Stage 2 identity semantics and implementation without rewriting Lane 02-owned code unless an isolated repair is explicitly coordinated.

Primary integrated oracles:

- `ADV-015-B` — exact strong-evidence/artifact-version binding;
- `ADV-002-B` — stale packet/target detection;
- `ADV-011-B` — epoch packet/base coherence and replayable progression;
- `ADV-006-B` — immutable supersession lineage is resolvable and acyclic.

For Stage 2 specifically, probe:

- logical id versus immutable instance confusion;
- canonicalization drift from key ordering, Unicode/text representation, unsupported numeric values, defaults, or parser normalization;
- content hash/reference ambiguity;
- evidence accidentally binding a mutable logical id;
- undocumented reference-string conventions;
- inability of a fresh occupant to reconstruct what an identity/reference means from repository state alone.

Preserve failures as explicit fixtures/oracles. Do not demand that isolated Stage 2 identity code solve later Stage 3/4 state-store relationships; classify the layer correctly.

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
