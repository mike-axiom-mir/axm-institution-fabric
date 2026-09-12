# CURRENT WAVE — Institution Fabric

Status: active initial build wave

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable evidence exists.

## Current integration state

- Lane 03 adversarial PR #2 is integrated into `main` at squash commit `51f93a940e54c19de7d732b5ccb574e95f3a28f3`.
- Lane 02 canonical contract PR #3 remains open and intentionally unmerged.
- Lane 03 identified four concrete cross-field continuity ambiguities in PR #3: reconstructable support for strong evidence states, root-conflict versus acceptance semantics, decision/result coherence, and occupancy lifecycle coherence.
- Lane 01 resolved the institutional semantic portion in `coordination/decisions/001_ROOT_GROUNDED_INTEGRATION_SEMANTICS.md`.
- Stage 1 remains incomplete until the contract pack includes the epoch/barrier descriptor, the original lane contract joins explicit schema versioning, and the adversarial regression cases are encoded/tested.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture and root boundary;
- review Lane 02 repairs against Decision 001 and Lane 03 counterexamples;
- verify Stage 1 completeness before contract-pack integration;
- keep the v0 proof and stop condition visible;
- integrate only grounded changes;
- maintain coordination state so later occupants can continue.

Avoid duplicating deep schema/runtime implementation claimed by Lane 02.

## Lane 02 — Deterministic Kernel Engineer

Current next claim:

- update PR #3 rather than starting a parallel replacement;
- encode regression coverage for the four Lane 03 counterexamples;
- enforce coherent receipt decision/result semantics consistent with Decision 001;
- keep strong evidence states reconstructable;
- enforce coherent occupancy lifecycle state;
- add the Stage 1 epoch/barrier descriptor;
- bring `lane.schema.json` into the explicit schema-versioning convention without silently breaking existing contract intent;
- rerun the deterministic validation suite and report exact results.

Do not move to state-store/runtime complexity until Stage 1 is coherent enough to freeze.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current next claim:

- challenge the updated PR #3 rather than duplicating Lane 02 repairs;
- confirm the four recorded counterexamples now fail as intended;
- inspect the new epoch/barrier contract for parallel/sequential continuity ambiguity;
- preserve any new counterexample as explicit fixture evidence;
- continue challenging universal primitives supported only by the Game Studio domain.

Do not substitute abstract governance discussion for concrete failure cases.

## Coordination cadence

Recommended stagger for recurring activations:

- Lane 01 lead: minute `:57`
- Lane 02 kernel: minute `:12`
- Lane 03 adversarial: minute `:27`

This creates a repeating flow:

```text
lead/integration -> kernel implementation -> adversarial challenge -> integration window -> next lead cycle
```

The timing is coordination convenience only. It grants no authority.

## Shared return-packet minimum

Each lane should leave:

- base commit/revision inspected;
- bounded claim;
- files changed;
- evidence/test results;
- uncertainty/blockers;
- dependency/downstream effects;
- next recommended action;
- explicit status: proposed / implemented / automated_tested / runtime_tested / measured / inferred / blocked / not_tested as applicable.

## Merge boundary

Inside AXM, the four roots remain the constitutional merge gate:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

No lane, founder, model, specialist, schedule position, or Git permission becomes authority by identity. When evidence is insufficient, preserve uncertainty or dissent.
