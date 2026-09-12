# AXM Institution Fabric — Build Plan

**Nickname: The Building**

This plan extends `NEXT_BUILD.md`; it does not replace the existing foundation or change the constitutional merge boundary.

## North-star proof

The Building becomes real when institutional continuity lives in explicit, replayable state rather than in the current occupant, private chat history, or social rank.

A convincing first proof must show that one objective can pass through persistent professional lanes, using interchangeable fixture occupants, and produce a new immutable institutional state with explicit artifacts, provenance, dependencies, evidence, uncertainty, handoffs, and integration reasons.

## Building anatomy

Use this human-readable map without hard-coding the metaphor into the kernel:

- **Constitution** — the four AXM roots and derived, explainable boundaries.
- **Foyer / registry** — institution identity, current objective, revision, available lanes, capabilities, and active work.
- **Work rooms / lanes** — persistent professional contracts independent of the occupant.
- **Occupancy desk** — temporary bindings between an intelligence and a lane.
- **Work ledger** — claims, dependencies, blockers, supersession, completion, and overlap signals.
- **Artifact archive** — typed outputs with identity, version, provenance, and evidence state.
- **Evidence lab** — evidence records and truth-state distinctions; never a single `done` flag.
- **Handoff desk** — bounded return packets with changes, uncertainty, downstream effects, and follow-up.
- **Integration chamber** — validation and root-grounded state transition into a new immutable revision.
- **Epoch hall** — parallel/sequential/hybrid coordination against defined base revisions.
- **Tool dock** — capability references and later adapters to AXM creation systems, Machine Floor, local/cloud models, or humans.
- **Departments** — domain packages such as Game Studio; they supply profession-specific knowledge without redefining the universal kernel.

## Build order

### Stage 0 — preserve the boundary

Keep `START_HERE.md`, `FOUNDATION.md`, `MERGE_GATE.md`, and `NEXT_BUILD.md` authoritative for current direction. Do not silently rewrite them to fit a familiar agent framework.

### Stage 1 — complete the canonical contract pack

Add schemas for the minimum kernel objects:

1. institution state revision
2. objective
3. lane
4. occupancy
5. work claim
6. artifact
7. evidence record
8. return packet
9. integration receipt
10. epoch / barrier descriptor

Requirements:

- deterministic serialization rules;
- stable ids;
- explicit versioning;
- useful validation errors;
- no occupant-specific hidden fields required for continuity;
- uncertainty and evidence state remain first-class.

### Stage 2 — canonical serialization + identity

Implement a tiny deterministic library that can:

- load and validate each object;
- canonicalize ordering/representation;
- derive reproducible content/state hashes;
- reject malformed or ambiguous canonical input;
- round-trip fixtures without drift.

This is the identity layer for later replay and rollback.

### Stage 3 — state store + work ledger

Create the smallest local/offline state layout for:

- immutable revisions;
- active objective;
- lane registry;
- occupancies;
- claims;
- artifact metadata;
- evidence records;
- submitted return packets;
- integration receipts.

The initial implementation may use plain files. Database/network complexity is not justified for v0.

### Stage 4 — claim, occupy, return

Implement bounded state transitions:

- open claim against revision N;
- bind an occupant to one lane;
- report overlap rather than silently double-own work;
- submit a typed return packet;
- preserve explicit uncertainty/failure;
- validate packet shape and lane compatibility.

A packet must never become canonical merely because it contains `done`, `complete`, or high-confidence language.

### Stage 5 — immutable integration + replay

Implement the smallest integration engine able to:

- verify base revision;
- validate lane/output compatibility;
- validate artifact/dependency references;
- inspect evidence state;
- record unresolved conflicts;
- accept, reject, defer, partially integrate, or request repair;
- emit explicit reasons;
- create revision N+1 without destroying N;
- replay how N+1 was produced from stored inputs.

Integration code is an execution mechanism, not constitutional authority. Internal canonical changes remain accountable to the four roots.

### Stage 6 — epoch experiment

Use 2–3 deterministic fixture lanes and one small objective.

Run the same institutional fixture in:

- parallel epoch mode;
- sequential occupancy mode;
- later, hybrid mode.

Compare outcomes and record divergence. Do not assume equivalence.

### Stage 7 — first real domain package

Extract a minimal Game Studio package only after the kernel works.

Initial loop:

- Gameplay Engineer
- Systems Designer
- QA / Playtest

These lanes should use the same universal contracts as the fixture institution while supplying game-specific knowledge, tools, artifact types, tests, and quality gates.

### Stage 8 — one real occupant adapter

Add one bounded adapter for an external intelligence. It receives only the explicit lane packet required to work:

- objective;
- base revision;
- lane contract;
- relevant artifacts/dependencies;
- capability references;
- evidence obligations;
- current claim;
- return-packet contract.

Hidden prior conversation must not be required for correct continuation.

### Stage 9 — transfer test

After Game Studio works, add a second small domain package from a different profession. Its purpose is not feature growth; it is to test whether supposedly universal kernel primitives are actually universal.

Only primitives supported by cross-domain evidence should be promoted as universal.

## CLI target for v0

A minimal local CLI is sufficient. Candidate commands:

```text
axm-institution validate <file>
axm-institution status
axm-institution objective show
axm-institution lanes list
axm-institution claim open ...
axm-institution occupy ...
axm-institution packet submit ...
axm-institution integrate ...
axm-institution revision show <id>
axm-institution replay <revision-id>
axm-institution diff <revision-a> <revision-b>
```

Exact command names may change if implementation evidence supports a better interface.

## Testing spine

Require early tests for:

- canonical object round-trip;
- same input -> same hash/revision id;
- previous revisions remain readable;
- invalid evidence state rejected;
- unknown lane rejected;
- stale base revision detected;
- occupant replacement preserves lane/work history;
- unresolved uncertainty survives integration;
- artifact provenance survives revision transitions;
- semantic duplicate claims are at least surfaced;
- replay reproduces the recorded transition;
- domain-specific fields cannot silently leak into the universal kernel contract.

## Three working lanes for the initial build

### 1. Institution Architect / Integration Lead

Owns whole-system coherence, boundary preservation, integration of specialist work, dependency sequencing, repository continuity, and the v0 proof. This lane has no constitutional superiority; its decisions must remain evidence- and root-grounded.

### 2. Deterministic Kernel Engineer

Owns schemas, canonical serialization, ids/hashes, state storage, work ledger mechanics, integration/replay implementation, deterministic fixtures, and technical tests.

### 3. Institutional Continuity / Adversarial Systems Specialist

Owns attempts to break the institutional hypothesis: occupant replacement, hidden-context dependence, lane ambiguity, evidence collapse, governance leakage, cross-domain leakage, parallel/sequential divergence, and failure/recovery semantics. Produces counterexamples, test cases, and repair recommendations rather than acting as an authority by title.

## Coordination rule

All three lanes inspect repository state before working, claim bounded work, avoid silent overlap, leave explicit return packets/coordination notes, and prefer small grounded changes over large speculative rewrites.

If disagreement cannot be resolved by current evidence, preserve the disagreement as explicit state. Do not turn seniority, confidence, technical access, founder status, model capability, or role title into merge authority.

## Explicit v0 non-goals

Do not spend the first proof on:

- polished UI;
- networking/distributed workers;
- a large knowledge base;
- autonomous model swarms;
- ten complete departments;
- replacing Ghost Studio;
- monolith packaging;
- claims of human/machine equivalence;
- claims of autonomous institutional correctness.

## v0 stop condition

v0 is complete when one small objective can move through multiple persistent lanes, with interchangeable fixture occupants, and produce a replayable new institutional revision whose artifacts, evidence, uncertainty, provenance, dependencies, handoffs, and integration reasons are explicit.

That is the first moment we can truthfully say the repository contains a functioning institutional kernel rather than only a design for one.
