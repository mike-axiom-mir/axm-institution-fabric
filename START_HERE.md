# START HERE — AXM Institution Fabric

**Nickname: The Building**

This file is the handoff for any future chat, human, model, or worker entering this repository.

## What you are building

You are **not** building another agent framework and you are not building a game-specific automation script.

You are building a deterministic institution: a persistent work environment in which interchangeable intelligences can occupy professional lanes and produce grounded output without the institution depending on private chat memory.

The institution should carry the continuity of the work.

An occupant should be able to enter a lane, inspect the current institutional state, receive the role contract, tools, knowledge, dependencies, and evidence obligations, perform bounded work, return a typed handoff, and leave. Another occupant should be able to continue later.

## Founding hypothesis

If a lane contains enough stable structure, knowledge, tooling, state, and verification, then **who occupies the lane and when they occupy it should matter less than it does in ordinary agent systems**.

This creates a testable spectrum:

```text
10 occupants / 10 lanes in parallel
1 occupant / 10 lanes sequentially
mixed humans + machines
mixed local + cloud models
```

The institution remains the same. Only occupancy changes.

Do not claim these configurations are quality-equivalent until measured. Parallelism changes ordering, so v0 should support an epoch/barrier model where multiple lanes can reason from the same starting state before integration creates the next state.

## Four roots

The only constitutional hard walls at genesis are:

- Truth
- Agency / non-domination
- Continuity
- Wisdom before speed

Do not add permanent restrictions merely because a capability is powerful, unfamiliar, autonomous, recursive, or frightening. Humans and machines are evaluated by grounded behavior, not category.

Working boundaries may be derived from current state, consent, evidence, dependencies, consequences, or domain needs. Keep them explainable and revisable.

## Preserve these design commitments

1. **Lane continuity is independent of occupant identity.**
2. **Institutional truth lives in explicit state, not hidden conversational memory.**
3. **Evidence status is first-class.** Distinguish implemented, compiled, automatically tested, runtime tested, visually inspected, playtested, measured, inferred, blocked, and not tested when relevant.
4. **Artifacts have identity and provenance.**
5. **Handoffs are bounded return packets, not vague summaries.**
6. **Parallel and sequential operation must share the same institutional contracts.**
7. **Domain-specific knowledge belongs in domain packages, not in the universal kernel.**
8. **No automatic canon from confidence or authority alone.** Integration should be grounded in evidence, compatibility, and roots.
9. **No fake done.** A scaffold is a scaffold; a passing schema is not a functioning studio.
10. **Preserve modularity.** This repository may later compose with Machine Floor, Directional State Fabric, Creation systems, capability fabrics, and annual monolith packaging.

## First proving domain

Use a Game Studio domain package first because AXM already has real specialist experiments to learn from. The game domain is a proving ground, not the definition of Institution Fabric.

The first package should eventually be able to express specialist lanes such as:

- Game Director
- Integration Steward
- Gameplay Engineer
- Systems Designer
- World / Encounter Designer
- Experience / Art / Audio Director
- QA / Playtest Specialist
- additional lanes discovered by evidence

Do not copy a current role prompt verbatim and call that a lane. Extract the persistent professional contract behind it.

## First technical target

Build the smallest deterministic kernel that can:

1. load a lane contract;
2. load one canonical institutional state snapshot;
3. create a work claim for a lane;
4. accept a return packet with explicit evidence state;
5. validate that the packet matches the lane contract;
6. record artifact/dependency changes;
7. integrate accepted outputs into a new immutable state revision;
8. replay how that revision was produced.

The first target does **not** need autonomous AI execution. Prove the institutional mechanics first with deterministic fixtures.

## What to read next

1. [`README.md`](README.md) — project orientation.
2. [`FOUNDATION.md`](FOUNDATION.md) — architecture and invariants.
3. [`schemas/lane.schema.json`](schemas/lane.schema.json) — first machine-readable contract.
4. [`NEXT_BUILD.md`](NEXT_BUILD.md) — concrete v0 sequence and stop condition.
5. [`domain-packs/game-studio/README.md`](domain-packs/game-studio/README.md) — first domain-package boundary.

## Builder rule

Preserve the active direction. Extend the structure when evidence requires it; do not rebuild the concept from scratch because another architecture is more familiar.

When uncertain, make the uncertainty explicit in repository state instead of silently deciding it away.
