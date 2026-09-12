# Decision 002 — Immutable Subject and Reference Semantics for Stage 2

Status: canonical coordination rule for the Stage 2 identity layer, derived from the integrated Stage 1 contracts plus Lane 03 cross-object continuity oracles.

Scope: Institution Fabric v0 canonicalization, immutable identity, and later cross-object validation. This is a derived technical/continuity rule, not a new constitutional root and not a grant of authority to any lane, actor, model, founder, or Git permission.

## Why this decision exists

Stage 1 now gives the kernel explicit object shapes, versions, base revisions, evidence records, artifact provenance, return packets, integration receipts, and epochs. Those objects can each be shape-valid while their references still mean the wrong thing across object boundaries.

Lane 03 froze four concrete next-layer oracles:

- `ADV-015-B`: strong evidence can accidentally support a later artifact version than the one actually tested;
- `ADV-002-B`: a packet produced from revision N can accidentally apply to target state already advanced beyond N;
- `ADV-011-B`: packets inside an epoch can carry bases inconsistent with the epoch's replay semantics;
- `ADV-006-B`: artifact supersession can become self-referential, forward-referential, or cyclic.

A deterministic-looking repository is not enough if a replacement occupant must guess what an opaque reference string was intended to mean.

## Stage 2 invariant

Institution Fabric must distinguish **logical identity** from **immutable instance identity**.

A stable logical id may name a continuing thing such as `artifact.rules`. It must not, by itself, prove which exact version/content/evidence instance is being referenced.

For v0:

1. **Canonical bytes come before content identity.**
   - Stage 2 must define one deterministic representation for supported kernel objects.
   - Semantically identical supported input must canonicalize reproducibly.
   - malformed or ambiguous canonical input must fail rather than be silently normalized into a different meaning.

2. **Immutable instances need reproducible identity.**
   - versioned/content-bearing objects must have an immutable instance identity grounded in canonical content.
   - the implementation may use a content hash, a typed id+version+hash reference, or another deterministic representation, but the meaning must be explicit and machine-checkable.
   - a mutable logical id alone is insufficient wherever truth, provenance, replay, or supersession depends on the exact instance.

3. **Strong evidence binds the exact subject instance.**
   - `compiled`, `automated_tested`, `runtime_tested`, `visually_inspected`, `playtested`, and `measured` evidence must resolve to the exact immutable subject instance the evidence actually supports.
   - a new artifact version must not inherit strong evidence merely because its stable logical id matches an older tested version.

4. **Supersession is immutable lineage, not a naming convention.**
   - `supersedes` must resolve to an existing prior immutable artifact instance.
   - self-supersession, forward references, unresolved references, and cycles are invalid.
   - lineage must remain reconstructable without private chat knowledge.

5. **Base revisions are compatibility claims.**
   - work claims, occupancies, packets, receipts, and epochs that declare a base revision must later be checked against actual repository/state history.
   - when relevant target/dependency state has advanced incompatibly, integration must reject, defer, or request explicit repair/rebase rather than silently apply stale work.

6. **Epoch progression must be replayable from explicit state.**
   - parallel epoch packets must be demonstrably bound to the epoch base.
   - sequential/hybrid progression must eventually record explicit step/base progression sufficient for replay.
   - array position, occupant memory, schedule order, or conversational chronology must not become hidden semantics.

7. **Unresolved reference meaning fails loudly.**
   - when the kernel cannot determine which immutable instance a consequential reference denotes, it must preserve the unresolved state instead of guessing from names, recency, actor confidence, or authority.

## Implementation boundary

Lane 02 owns the smallest deterministic Stage 2 implementation and may choose the exact reference encoding if it satisfies these invariants.

Stage 2 should initially prove:

- canonical load/validation for the Stage 1 object pack;
- deterministic canonical bytes;
- reproducible hashes/instance ids;
- explicit immutable reference construction/parsing;
- round-trip without drift;
- exact evidence-to-subject-instance binding at the identity layer where practical.

Stage 3/4 state and ledger work should enforce repository-level existence, stale-base, lineage, and epoch/base relationships that isolated object canonicalization cannot prove.

Stage 5 integration/replay must consume those explicit identities rather than inventing another reference convention.

Do not pull the state store, scheduler, model adapter, or Game Studio package into Stage 2 merely to make the identity library look more complete.

## Root grounding

### Truth
Evidence and provenance must identify the exact thing actually observed or tested. Stable names cannot stand in for unverified version identity.

### Agency / non-domination
No powerful occupant, founder, model, role title, or Git permission can make an unresolved or stale reference true by assertion.

### Continuity
A replacement occupant must reconstruct exact subject identity, lineage, and base relationships from stored state rather than hidden convention.

### Wisdom before speed
Freeze reference meaning while the kernel is small, before state-store and replay code make an accidental string convention expensive to unwind.

## Evidence boundary

This decision defines required semantics. It does **not** claim that immutable-reference enforcement, stale-base validation, lineage validation, or replay exists yet. Those remain implementation and test obligations for later stages.
