# NEXT BUILD — AXM Institution Fabric

This is the recommended first implementation sequence for a dedicated builder chat.

## v0 objective

Prove that institutional continuity can live outside the occupant.

Do **not** start by wiring a cloud model into every lane. Build the deterministic mechanics first so failures can be attributed to the institution rather than model behavior.

## Phase 1 — canonical objects

Implement minimal serializable objects for:

- institution state revision;
- objective;
- lane;
- occupancy;
- work claim;
- artifact;
- evidence record;
- return packet.

Acceptance condition: fixtures round-trip deterministically and invalid objects fail with useful errors.

## Phase 2 — claim + handoff

Implement:

1. open a work claim against a base revision;
2. bind a temporary occupant to a lane;
3. submit a return packet;
4. validate packet outputs against the lane contract;
5. preserve explicit uncertainty and evidence states.

Acceptance condition: no packet can become integrated merely because it says "done".

## Phase 3 — immutable integration

Implement a small integration engine that:

- reads a base revision;
- validates a packet;
- records artifact additions/changes;
- records dependency effects;
- produces a new revision id;
- preserves the old revision;
- emits an integration receipt with reasons.

Acceptance condition: the full transition can be replayed and explained from stored data.

## Phase 4 — epoch experiment

Create two or three deterministic fixture lanes and one objective.

Run the same fixture in two modes:

```text
A. parallel epoch
all lanes read revision N -> packets -> integration -> revision N+1

B. sequential occupancy
one occupant rotates through the same lane contracts against the defined epoch semantics
```

Measure and document divergence instead of assuming equivalence.

## Phase 5 — first Game Studio package

Only after the kernel works, extract a tiny game-studio package with 2–3 real role capsules.

Good first candidates:

- Gameplay Engineer
- Systems Designer
- QA / Playtest

Why these three: they create a useful implementation -> rules -> verification loop without requiring the whole studio on day one.

Use the existing AXM Ghost Studio experiment as evidence about real role needs, but preserve this repository's universal boundary.

## Phase 6 — real occupant adapter

Add one adapter allowing an external intelligence to occupy one lane.

The adapter should receive a bounded lane packet containing:

- objective;
- base state revision;
- role contract;
- relevant artifacts/dependencies;
- available capability references;
- evidence obligations;
- current claim;
- required return-packet format.

The adapter must not require hidden prior conversation to function.

## Tests to require early

- same input fixture -> same state revision hash;
- invalid evidence state rejected;
- unknown lane id rejected;
- packet base revision mismatch detected;
- semantic duplicate claim is at least reportable even before sophisticated overlap detection exists;
- previous revision remains readable after integration;
- unresolved uncertainty survives integration;
- occupant change does not erase lane/work history.

## Explicit non-goals for v0

Do not spend the first build on:

- a beautiful UI;
- ten complete game roles;
- autonomous merge/canon claims;
- model benchmarking;
- huge knowledge bases;
- distributed networking;
- annual monolith packaging;
- pretending Institution Fabric already replaces ordinary studios.

## Stop condition

v0 is complete when one small objective can move through multiple persistent lanes, with interchangeable fixture occupants, and produce a replayable new institutional state whose artifacts, evidence, uncertainty, provenance, and handoffs are all explicit.

At that point the project has a real floor to build upward from.
