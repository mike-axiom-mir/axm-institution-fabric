# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Canonical `main` before this overlay: `8c5246dd0ea9842bb4dc195035cc46c3699dd3e5`
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current bounded gate: **Decision 016 — Exact Same-Packet Dependency Graph Facts**
Current disposition: **HOLD on ADV-049-J proof-to-use graph-edge transport continuity; do not integrate Decision 016 yet.**

`coordination/CURRENT_WAVE.md` remains historical chronology. This file is the current-state overlay and must be read with the numbered decisions, open PR evidence, and durable specialist return packets.

## What remains canonical before Decision 016

The bounded Python v0 kernel canonically demonstrates:

- strict canonical identity and immutable references;
- exact revision membership and exact lifecycle bases;
- occupancy admission, work-claim admission, and return-packet admission from exact historical state;
- exact packet created-artifact and evidence identity;
- exact evidence-subject chronology and bounded output/evidence compatibility;
- exact created-artifact work-base provenance;
- exact two-sided modified-artifact prior/result identity and modified-result compatibility;
- one exact mixed created+modified packet compatibility projection from one exact historical context;
- Decision 014 exact output dependency target identity for artifact v0.3 across created and modified-result outputs;
- Decision 015 exact dependency-context membership facts: exact claim-base membership, exact packet-created membership, exact packet-modified-result membership, and explicit outside-all-context standing;
- historical artifact v0.1/v0.2 dependency strings remain unresolved rather than silently acquiring v0.3 meaning;
- ADV-035 through ADV-048 regression pressure preserving proof-to-use identity, historical selection, fail-closed transport/materialization, provenance, output/evidence isolation, modification identity, mixed projection, dependency target identity, and dependency context membership.

Decision 016 is **not canonical yet**. Its production candidate and adversarial evidence remain in open PR state.

## Decision 016 candidate — Lane 02 PR #72

Lane 02 implemented only the read-only same-packet dependency graph projection on canonical base `8c5246dd0ea9842bb4dc195035cc46c3699dd3e5`.

Exact tested implementation/workflow head:

`c9512e9218243436c005286fa2c9e527d12b0319`

Native run `34789371372`, job `103810632006` recorded:

- Python 3.12.14;
- **311 / 311 tests passed**;
- all ten Decision 016 baseline regressions green;
- ADV-035 through ADV-048 green in the same run;
- explicit `py_compile` success;
- complete job conclusion: success.

The candidate correctly demonstrates, in-process, the bounded graph surface:

- exact packet output refs as nodes;
- exact `required_output_ref -> dependent_output_ref` relations only for same-packet exact dependency targets grounded by Decision 015;
- base-only/external dependency facts preserved but not promoted into packet-local edges;
- no output-family precedence;
- deterministic SCC/self-edge/cycle facts;
- one deterministic exact-ref-lexically-tiebroken topological witness only for an acyclic graph;
- no dependency-validity, chronology, closure, acceptance, integration, epoch, or replay authority.

Lane 02 final PR #72 head `7d694a3277859a5b7d3e4d951463cef767bff02c` adds only its durable return packet beyond the exact tested implementation head.

## Independent hold — Lane 03 ADV-049 on PR #73

Lane 03 attacked Decision 016 without changing production runtime or schema semantics.

Exact tested adversarial head:

`bf13044775aff1df353bf250f3ba3b551e827d47`

Its first native full-suite run `34790055632`, job `103812485635`, recorded:

- **321 tests ran / 320 passed / exactly 1 failed**;
- ADV-049-A through ADV-049-I passed;
- all pre-existing tests passed;
- exact failure: **ADV-049-J only**;
- compile skipped because unittest failed first.

The final documentation-only Lane 03 branch head `97d59b6290e59e4e0459e27f5eca04a87b633da3` then received a second native full-suite run `34790552573`, job `103813838567`, which again recorded:

- **321 tests ran / 320 passed / exactly 1 failed**;
- exact failure: **ADV-049-J only**;
- ADV-049-A through I and all pre-existing tests remained green;
- compile skipped because unittest failed first;
- complete workflow conclusion: failure.

This second run confirms that the durable return-packet commit did not change the blocker.

## ADV-049-J — exact blocker

`ExactSamePacketDependencyEdge` is currently a tuple-backed `NamedTuple` with named in-process fields:

```text
required_output_ref
dependent_output_ref
```

Python stdlib JSON accepts that authoritative edge and serializes it as an unlabeled positional array:

```text
[required_output_ref, dependent_output_ref]
```

That is not durable named institutional meaning. A replacement consumer receiving the ordinary transported value must know the originating Python tuple field order out-of-band to recover which exact ref is the required output and which is the dependent output.

The failure is therefore **proof-to-use transport meaning loss**, not durable-store corruption, not graph-selection failure, and not a contradiction of ADV-049-A through I.

The repository already has a relevant precedent in the earlier proof-to-use transport repairs: unsupported ordinary transport may fail closed, or an explicit supported representation may preserve exact named semantics; it must not silently change the semantic shape of an authoritative operational record.

## Integration disposition

**PR #72 remains held and must not be merged yet.**

**PR #73 remains adversarial evidence and must not be merged as a failing regression branch before the production repair is integrated/reapplied appropriately.**

Do not open Decision 017 or any later dependency policy while this Decision 016 proof-to-use blocker is unresolved.

No evidence currently justifies widening the hold beyond transport continuity. ADV-049-A through I strongly support the rest of the bounded Decision 016 graph semantics.

## Smallest repair boundary — Lane 02

Lane 02 should repair only Decision 016 graph-leaf proof-to-use representation while preserving all currently green graph semantics.

An acceptable repair must:

1. preserve Decision 015 as the sole packet/dependency membership authority;
2. preserve exact node and edge selection;
3. preserve edge direction `required_output_ref -> dependent_output_ref`;
4. preserve family neutrality, SCC/self-edge/cycle facts, and lexical topological witness behavior;
5. expose no dependency-validity, chronology, closure, acceptance, integration, epoch, or replay authority;
6. make unsupported ordinary JSON transport fail closed **or** preserve named graph-leaf semantics exactly;
7. avoid a one-off edge-only patch if equivalent graph-leaf types share the same tuple-positionalization mechanism; repair should be coherent across the Decision 016 graph leaf family where the representation is equivalent;
8. keep the explicit self/mutual-cycle authorability uncertainty unresolved unless new durable evidence actually resolves it.

The existing canonical-byte-backed fail-closed transport pattern in `packet_output_identity.py` is relevant implementation precedent, but it is not automatically mandated as the only valid repair.

## Required repair evidence

After Lane 02 leaves a repaired exact head:

- rerun ADV-049-A through ADV-049-J unchanged;
- rerun all Decision 016 baseline tests;
- rerun the complete repository unittest discovery suite;
- require explicit `py_compile` success;
- record the exact repaired head and native workflow evidence;
- preserve any first failing repair attempt rather than rewriting it away.

Then Lane 03 should independently re-attack the repaired exact head and clear only the transport hold that the evidence actually resolves.

## Explicit representation uncertainty — cycles

Lane 02 also preserved a separate uncertainty that is **not** the current merge blocker: artifact v0.3 exact refs hash canonical artifact bytes that include `dependency_refs[]`. Authoring a self-dependency that names the artifact's own final exact ref appears to require a cryptographic fixed point; mutual exact cycles appear to require mutually recursive fixed points.

Decision 016 must still preserve/detect cyclic topology if an already-grounded upstream relation supplies it, but no current evidence proves that the normal content-addressed object-store write path can author exact self/mutual cycles end-to-end. Do not silently turn that representation uncertainty into either "cycles are impossible" or "cycles are allowed/invalid" policy.

## Lane boundaries

### Lane 02 — active implementation lane

Repair only ADV-049-J / equivalent Decision 016 graph-leaf transport continuity. Keep PR #72's graph selection/topology semantics intact and stop before dependency admissibility, actual chronology, closure/completeness, packet acceptance, claim closure, successor publication, Stage 5 integration, epochs, or replay.

### Lane 03 — adversarial lane

Do not duplicate Lane 02's repair. Wait for a repaired exact head, then rerun ADV-049 unchanged and attack the coherent graph-leaf repair. Preserve the existing hold meanwhile.

### Lane 01 — integration lane

Do not implement the same repair in parallel. Keep the hold visible on canonical coordination state, review the repaired exact head and independent adversarial evidence, and integrate only when the four-root gate is grounded.

## Still explicitly unresolved

- Decision 016 graph-leaf transport continuity until ADV-049-J is repaired;
- dependency admissibility / allowed-context policy;
- actual dependency chronology and same-packet producer/consumer execution ordering;
- transitive dependency closure and declaration completeness;
- whether cycles/self-dependencies are acceptable;
- exact source provenance / `provenance.source_refs[]` taxonomy and closure;
- evidence method/source quality, precedence, invalidation dominance, and closure;
- multiple `required_states` semantics;
- logical lineage and `supersedes_ref` validity;
- global occupancy/claim currentness, supersession, and authorization;
- multiple-packet conflict/selection semantics;
- packet acceptance/rejection and durable closure;
- claim closure;
- successor state-revision publication;
- Stage 5 integration receipts/runtime;
- epochs/barriers and replay;
- cross-language reproduction and supported serialized compatibility transport;
- stronger filesystem durability/concurrency evidence;
- hostile same-process code isolation beyond Decision 009's trusted deterministic runtime boundary.

## Four-root gate

- **Truth:** keep the 311/311 in-process Decision 016 success and the two independent 320/321 ADV-049 failure reproductions visible at the same time; do not relabel either away.
- **Agency / non-domination:** no founder, specialist, schedule position, branch ownership, Git permission, version, recency, or tuple convention becomes semantic authority.
- **Continuity:** the current hold, exact failing oracle, repair boundary, and unresolved cycle representation question are now reconstructable from repository state without private chat memory.
- **Wisdom before speed:** repair the narrow proof-to-use representation failure before integrating Decision 016 or opening dependency policy, closure, Stage 5 integration, epochs, or replay.
