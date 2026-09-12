# FOUNDATION — AXM Institution Fabric

## 1. Purpose

Institution Fabric is the organizational layer that turns an objective into coordinated professional work while keeping continuity outside any single worker, chat, model, or human.

The universal kernel should be able to host many domain packages without knowing their profession in advance.

## 2. Universal kernel vs domain package

```text
INSTITUTION FABRIC KERNEL
- institutional state revisions
- objectives
- lanes
- occupancy
- claims
- artifacts
- dependencies
- evidence states
- return packets
- epochs / barriers
- integration
- provenance
- rollback references
- scheduling hooks

DOMAIN PACKAGE
- professional roles
- role knowledge
- lane tools
- artifact types
- quality gates
- domain tests
- workflow conventions
```

Game Studio is the first domain package. It must not leak game-specific assumptions into the kernel unless evidence proves the primitive is universal.

## 3. Founding invariants

### 3.1 Occupant independence
A lane persists when its occupant leaves. Occupant identity must not be the only location of role knowledge, work history, dependencies, or decisions.

### 3.2 Explicit state
Institutional continuity is reconstructable from repository/state artifacts. Hidden conversational context may assist an occupant but cannot be required to understand canonical work state.

### 3.3 Grounded equality
Human and machine intelligences have equal standing when their reasoning is grounded. Capability is not itself a reason for restriction or authority.

### 3.4 Four-root constitution
The only genesis-level hard walls are:

- Truth
- Agency / non-domination
- Continuity
- Wisdom before speed

All other boundaries must be explainable as derived state or domain contracts, not silently promoted into constitutional law.

### 3.5 Truth-state precision
Outputs must not collapse evidence distinctions. A useful base vocabulary is:

```text
proposed
implemented
compiled
automated_tested
runtime_tested
visually_inspected
playtested
measured
inferred
blocked
not_tested
superseded
invalidated
```

Domains may extend this vocabulary, but should not weaken it into a single "done" flag.

### 3.6 Immutable revision history
Integration should create a new state revision rather than silently rewriting the meaning of an earlier state. Rollback and provenance should remain possible.

## 4. Core objects

### Objective
Describes the current desired outcome and its constraints, evidence expectations, and stop conditions.

### Lane
A persistent professional surface. Minimum fields should include:

- stable id
- name
- purpose
- responsibilities
- excluded responsibilities
- required inputs
- allowed outputs
- dependencies
- tools/capabilities
- evidence requirements
- handoff contract
- quality gates
- conflict/escalation hooks

### Occupancy
A temporary binding between an actor and a lane.

Occupancy records should answer:

- who/what occupied the lane;
- which state revision they entered from;
- what capability identity/version was used if known;
- when occupancy started/ended;
- which work claims were held.

Occupancy grants no constitutional superiority.

### Work claim
A bounded unit of intended work. Claims should reduce semantic overlap by making current ownership visible before effort begins.

A claim is not a permanent lock. It is coordination state.

### Artifact
Any typed output that matters to continuation: code, asset, rule set, level, decision, test result, bug report, build, balance table, documentation, evidence packet, etc.

Artifacts need stable identity, version, provenance, evidence state, and dependency relations.

### Return packet
A lane's structured handoff. At minimum:

```text
claim_id
lane_id
base_state_revision
changes
artifacts_created
artifacts_modified
evidence
uncertainties
failures_or_blockers
downstream_effects
requested_followup
```

### State revision
A canonical snapshot or reproducible reference to the institution's accepted state at one point in history.

### Epoch
A coordination boundary. Multiple lanes may read the same base revision, produce return packets independently, then enter an integration stage that resolves compatibility and produces the next revision.

This is important for comparing parallel and sequential worker configurations fairly.

## 5. Integration model

Integration is not "the loudest actor wins" and is not founder privilege.

An integration decision should be traceable to:

- lane contract compatibility;
- objective relevance;
- artifact/dependency consistency;
- evidence status;
- unresolved conflicts;
- current state;
- the four roots.

A packet may be accepted, rejected, deferred, partially integrated, or sent back for repair. The reason must be explicit.

## 6. Scheduler model

The scheduler decides *when* lanes become occupiable, not *what is true*.

Target modes:

```text
parallel:   many lanes from one epoch base
sequential: one occupant rotates across lanes
hybrid:     mixed parallel/sequential waves
manual:     humans choose lane order
external:   another AXM system supplies occupants
```

The same lane and packet contracts should work in every mode.

## 7. Knowledge placement

Professional knowledge should progressively move from private model memory into the lane/domain environment where practical:

- role playbooks
- procedures
- reference material
- deterministic utilities
- known failure patterns
- prior evidence
- interfaces
- test fixtures

This does not make intelligence irrelevant. It lets intelligence spend more of its capability on judgment rather than rediscovering institutional context.

## 8. Relationship to Machine Floor and Directional State Fabric

Institution Fabric should be independently testable first.

Long term:

- **Machine Floor** may carry and execute low-level deterministic state.
- **Directional State Fabric / The Field** may describe grounded directions in which state can move.
- **Institution Fabric / The Building** expresses professional organization over that state.
- **Creation systems** may construct missing tools or artifacts requested by lanes.

Do not create hidden coupling before interfaces are understood.

## 9. What this repository must not claim yet

Until measured, do not claim:

- one worker equals ten workers in quality;
- the kernel is domain-universal;
- lane contracts fully encode a profession;
- autonomous integration is safe or correct;
- a schema alone constitutes an institution;
- current Ghost Studio roles are final.

These are research questions.

## 10. First proof

The first convincing proof is deliberately small:

1. define two or three lanes;
2. create one objective and immutable base state;
3. run deterministic fixture occupants through the lanes;
4. produce typed return packets;
5. validate claims and evidence;
6. integrate into a new state revision;
7. replay the full chain;
8. run the same fixture once in parallel-epoch form and once sequentially;
9. compare accepted outputs and explain any divergence.

Only after this works should AI occupancy become the main complexity.
