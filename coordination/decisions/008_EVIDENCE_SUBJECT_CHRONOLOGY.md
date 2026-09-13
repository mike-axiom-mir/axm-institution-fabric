# Decision 008 — Evidence Subject Chronology Before Output Compatibility

Status: accepted Stage 4 precondition

## Context

Stage 4 now has exact immutable selection for return-packet created artifacts and packet evidence records. That is necessary but not sufficient for lane output/evidence compatibility.

The current universal contracts expose three separate facts:

- `lane.outputs[]` declares output `type` values and `lane.evidence_requirements[]` declares required evidence states for an output type;
- an `artifact` carries its own `type` and an `evidence_refs[]` field;
- an `evidence-record` carries a `subject_ref` and `state`;
- a return packet can now operationally bind exact immutable created-artifact and evidence-record instances.

A compatibility check that compares only artifact type and evidence state would still allow unrelated evidence to be laundered into support for an output. Exact evidence identity proves *which evidence record* was selected; it does not prove *what exact output instance that record is evidence about*.

## Concrete counterexample

Assume lane `lane-02` requires `automated_tested` evidence for output type `kernel_contracts`.

1. Packet P names exact artifact A with `type = kernel_contracts`.
2. P also names exact evidence E with `state = automated_tested`.
3. E's `subject_ref` names a different source, artifact, path, or logical object.
4. A compatibility routine that checks only `A.type` and `E.state` passes.
5. The institution has therefore converted unrelated evidence into support for A without an explicit relationship.

That violates Truth and makes later reconstruction depend on the occupant knowing which evidence was "really meant" for which output.

## Chronology / cycle constraint

There is also a content-addressed chronology constraint.

If artifact A embeds exact evidence ref E in `A.evidence_refs`, while evidence E embeds exact artifact ref A in `E.subject_ref`, both immutable hashes depend on the other exact hash:

```text
A exact identity depends on E exact identity
E exact identity depends on A exact identity
```

The v0 kernel must not require such a reciprocal exact-reference cycle or invent a newest/current lookup to escape it.

For evidence produced after an artifact exists, the acyclic order is:

```text
exact artifact A
    -> exact evidence E whose subject_ref names A
    -> exact return packet P that names A and E
```

This order also follows Decision 007's general rule: a relationship to an object created later cannot be reconstructed from earlier state by hidden recency rules; bind the later relationship explicitly at the point where it exists.

## Decision

Before packet output/evidence compatibility may treat an evidence record as satisfying a created artifact's requirement, **evidence-to-output subject binding must be exact and one-way for this Stage 4 slice**.

### A. What counts as evidence for one created artifact

For the bounded created-artifact compatibility path:

```text
packet created-artifact ref A
packet evidence-record ref E
E.subject_ref
    -> must parse as one canonical exact immutable artifact ref
    -> must equal A exactly
```

Only then may E's `state` be considered evidence about A.

A bare logical artifact id, filesystem path, content path, newest artifact, same-logical-id different exact instance, mutable current/HEAD pointer, or occupant interpretation does not satisfy this exact subject-binding precondition.

### B. Packet evidence is the operational source for this slice

The already-grounded exact `return-packet.evidence_refs` relationship is the packet-level evidence set available to later compatibility.

`artifact.evidence_refs` does **not** become authoritative for post-artifact evidence compatibility in this decision. It remains contract data whose chronology and exact semantics need separate grounding. In particular, it must not be used to manufacture a reciprocal exact-reference cycle or to override an exact `evidence.subject_ref` mismatch.

This does not delete or reinterpret historical artifact data. It only limits what later runtime may treat as authoritative evidence for this specific compatibility path.

### C. Existing evidence objects remain valid outside this path

An evidence record whose `subject_ref` is a path, content reference, logical id, test name, or other non-exact subject may still be a valid evidence object under its current schema and may be useful for other purposes.

It simply cannot satisfy **exact created-artifact output compatibility** until a future grounded relation explains how that subject proves the exact artifact instance.

### D. No mass schema rewrite yet

The current `evidence-record.schema.json` allows `subject_ref` to be a general string. This decision does not silently rewrite historical schema semantics.

The first implementation may add a read-only/fail-closed subject-binding precondition that accepts only canonical exact artifact refs when evidence is being used for exact created-artifact compatibility. A future schema version may encode that distinction explicitly after implementation/adversarial evidence justifies it.

## Smallest next implementation opened

Lane 02 may implement only a read-only exact evidence-subject resolver around the already-grounded packet output/evidence identity result.

Required behavior:

1. take one exact resolved packet/artifact/evidence surface;
2. parse each candidate `evidence.subject_ref` through the shared Stage 2 immutable-reference parser;
3. require kind `artifact` for evidence being considered against a created artifact;
4. bind an evidence record only to the exact created-artifact ref it names;
5. expose unmatched/non-artifact subject evidence explicitly rather than assigning it by type, array order, recency, or logical id;
6. preserve the existing `artifacts_modified` fail-closed boundary;
7. remain read-only — do not close claims, publish revisions, integrate packets, or mutate evidence.

Required regressions:

- exact evidence subject A binds to exact created artifact A;
- same logical artifact id but different exact artifact ref does not bind;
- bare logical id/path/content string does not count as exact artifact subject evidence;
- wrong-kind exact subject ref fails closed for artifact compatibility;
- packet evidence for unrelated artifact B cannot satisfy artifact A even when type/state appear compatible;
- array order/newest/storage order/current state cannot choose a subject;
- `artifact.evidence_refs` cannot override or rebind a contradictory exact evidence subject;
- ADV-035/036/037/038 exact-value and materialization invariants remain green.

Stop after this exact subject-binding precondition. Do not yet decide full lane output compatibility, the meaning of multiple `required_states`, evidence quality sufficiency, artifact provenance closure, modified-artifact compatibility, claim closure, successor revision publication, integration, epochs, or replay.

## Scope boundary / unresolved questions

Still separate:

- whether every lane `required_states` entry is conjunctive, alternative, ordered, or quality-ranked;
- whether one evidence record may satisfy more than one explicit output requirement;
- evidence method/source quality beyond the current schema constraints;
- artifact `evidence_refs` chronology and whether a future schema should distinguish pre-artifact evidence, post-artifact attestations, or derived indexes;
- exact artifact provenance base semantics (`ADV-002-C`);
- modified-artifact exact prior/result identity and stale-target compatibility (`ADV-002-I`);
- multiple-packet selection/conflict semantics;
- occupancy/claim currentness, supersession, authorization, and stale-base policy;
- historical schema reconstruction and durable closure proof;
- claim closure/status publication;
- successor state revision publication;
- integration receipts/runtime;
- epochs/barriers and replay;
- cross-language transport and stronger filesystem durability evidence.

These remain explicit obligations rather than being inferred from this decision.

## Root grounding

### Truth

Exact evidence identity without exact subject identity is insufficient to claim that the evidence supports an exact output. The subject relation must be explicit before evidence state can be used as output proof.

### Agency / non-domination

Array order, recency, matching type, actor intent, role title, founder status, schedule position, or Git permission cannot silently decide which output an evidence record supports.

### Continuity

A replacement occupant can reconstruct the relation from exact immutable refs alone: artifact A exists, evidence E exactly names A, and packet P exactly names both. No private explanation of "which test was meant for which artifact" is required.

### Wisdom before speed

Open only the subject-binding precondition. Do not rush from exact selection directly into broad compatibility while the evidence-to-output relation is still ambiguous.

## Evidence boundary

This decision is grounded in the canonical Stage 2 immutable-reference model, Decision 007 chronology, the current lane/artifact/evidence/return-packet contracts, the integrated exact packet output/evidence selection surface, and the demonstrated requirement to keep proof-to-use meaning explicit.

It is not evidence that evidence-subject resolution, output compatibility, evidence closure, claim closure, successor publication, integration, epochs, or replay already work.
