# AXM Institution Fabric

**Nickname: The Building**

AXM Institution Fabric is the deterministic work environment that intelligences can inhabit to produce professional work together.

The central idea is simple:

> **The lane belongs to the institution, not to whoever occupies it.**

A human, cloud model, local model, future machine intelligence, or mixed team may occupy a lane. The occupant matters for judgment and quality, but the institution should carry the role contract, professional context, tools, shared state, evidence requirements, dependencies, handoffs, and continuity.

This repository is not a game studio itself. The first proving domain is a **Game Studio package**, because AXM already has specialist-role experiments there. The architecture must remain domain-general so the same building can later host software engineering, research, media production, or domains not yet defined.

## Why this exists

AXM has been learning how to model workers: specialists, perspectives, builders, testers, directors, evidence standards, return packets, and coordination. Institution Fabric models the thing those workers work **inside**.

The target flow is:

```text
objective
   -> canonical institutional state
   -> specialist lane(s)
   -> lane-specific knowledge + deterministic tools
   -> typed artifacts + evidence
   -> handoff / integration
   -> new institutional state
```

The same work should be runnable by:

- ten occupants in ten lanes in parallel;
- one occupant rotating through ten lanes sequentially;
- a mixed human + AI team;
- local and cloud intelligences with different strengths;
- future machine-floor or creation-system occupants.

The organization should preserve continuity when occupants change.

## Constitutional roots

At genesis, AXM recognizes four hard roots:

1. **Truth**
2. **Agency / non-domination**
3. **Continuity**
4. **Wisdom before speed**

Humans and machines do not receive higher or lower standing merely because of category, capability, familiarity, or fear. Behavior must be grounded against the roots.

Institution Fabric may derive working constraints from current state, consent, evidence, dependencies, real consequences, and domain requirements. Those constraints are not automatically constitutional walls.

## Core concepts

### Lane
A persistent professional work surface. A lane defines purpose, inputs, outputs, knowledge, tools, evidence obligations, dependencies, and handoff rules.

### Occupant
Any intelligence currently performing the lane. Occupancy is temporary; the lane is persistent.

### Role capsule
The machine-readable contract that lets an occupant enter a lane without depending on private chat memory.

### Artifact
A typed output with identity, provenance, version, evidence state, and dependency relations.

### Work ledger
The deterministic record of available work, claims, blockers, dependencies, completion, supersession, and invalidation.

### Return packet
A bounded handoff that records what changed, why, evidence, unresolved uncertainty, downstream effects, and requested follow-up.

### Epoch / barrier
A coordination mechanism allowing parallel and sequential occupants to reason from the same starting state before integration creates the next state.

### Domain package
The role set, knowledge, tools, artifact types, quality standards, and workflow specific to one profession or production domain.

## First proving domain: Game Studio

The first domain package should learn from AXM Ghost Studio without copying its temporary coordination assumptions blindly.

Candidate lanes include game direction, integration, gameplay engineering, systems design, world/encounter design, experience/art/audio direction, QA/playtest, and additional specialist lanes as the experiment matures.

The goal is not to hard-code "game" into Institution Fabric. The goal is to discover which institutional primitives survive when the Game Studio package is replaced by another domain.

## Relationship to other AXM layers

```text
Directional State Fabric (The Field)
    how grounded state may move

Institution Fabric (The Building)
    how intelligences organize useful work

Machine / State Floor
    deterministic execution and preserved machine state

Creation systems
    construct missing tools, artifacts, and capability
```

These are intended to become composable layers, not a single premature monolith.

## Current status

**Seed / research scaffold.**

This repository currently defines the invariant direction and the first machine-readable lane contract. It does **not** yet claim to be a functioning autonomous institution.

Start with [`START_HERE.md`](START_HERE.md), then read [`FOUNDATION.md`](FOUNDATION.md) and [`NEXT_BUILD.md`](NEXT_BUILD.md).
