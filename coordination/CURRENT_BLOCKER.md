# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Canonical main after Decision 015 + ADV-048 integration: `e832a5f865655c315bdc9fdc3b81db15b8527716`
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current next bounded gate: **Decision 016 — Exact Same-Packet Dependency Graph Facts**

`coordination/CURRENT_WAVE.md` remains historical chronology. This file is the newer current-state overlay and must be read with the numbered decisions and durable specialist return packets.

## What is now canonical

The deterministic institution kernel now canonically demonstrates, on the bounded Python v0 path:

- strict canonical identity and immutable references;
- exact revision membership and exact lifecycle bases;
- occupancy admission, work-claim admission, and return-packet admission from exact historical state;
- exact packet created-artifact and evidence identity;
- exact evidence-subject chronology and bounded output/evidence compatibility;
- exact created-artifact work-base provenance;
- exact two-sided modified-artifact prior/result identity and modified-result compatibility;
- one exact mixed created+modified packet compatibility projection from one exact historical context;
- Decision 014 exact output dependency target identity for artifact v0.3 across created and modified-result outputs;
- **Decision 015 exact dependency-context membership facts**: exact claim-base membership, exact packet-created membership, exact packet-modified-result membership, and explicit outside-all-context standing;
- historical artifact v0.1/v0.2 dependency strings remain unresolved rather than silently acquiring v0.3 meaning;
- ADV-035 through ADV-048 regression pressure preserving proof-to-use identity, historical selection, fail-closed transport/materialization, provenance, output/evidence isolation, modification identity, mixed projection, dependency target identity, and dependency context membership.

This remains a read-only proof surface. Dependency identity and context membership are not dependency validity, chronology, closure, packet acceptance, claim closure, publication, integration, epochs, or replay.

## Decision 015 integration evidence

### Lane 02 — PR #68

Lane 02 implemented only the Decision 015 read-only membership projection by consuming Decision 014.

Its first run reached 292 tests with one error. The failing test tried to construct the same exact artifact simultaneously as a created output and a modified result, while canonical Decision 013 correctly rejects that exact-ref category collision. Lane 02 preserved the failure, repaired the test oracle rather than weakening production semantics, and reran.

Exact repaired implementation head `624d50e2b705ecc27ba1c0279a145b6517c7c09e` directly completed:

- Python 3.12.14;
- **292 / 292 tests passed** in 286.773s;
- all eight Decision 015 regressions green;
- ADV-035 through ADV-047 green;
- explicit `py_compile` success.

The final PR head added only the durable Lane 02 return packet beyond the tested implementation. PR #68 was squash-integrated as:

`848900a3857016145357ad2e4a51fb56a6c46b48`

### Lane 03 — PR #69 / fresh PR #70

Lane 03 independently attacked Decision 015 with ADV-048 A–I while changing no production runtime or schema semantics. The original stacked exact head directly completed **301 / 301 tests** plus explicit compile successfully.

Because PR #69 was stacked on Lane 02's pre-squash ancestry, Lane 01 did not merge duplicate production history or rewrite the specialist branch. The exact ADV-048 workflow/test/return-packet files were reapplied to fresh canonical Decision 015 main in PR #70.

Fresh PR #70 run `34788408821`, job `103808025622` directly recorded:

- Python 3.12.14;
- **301 / 301 tests passed** in 384.554s;
- ADV-048-A/B/C/D/E/F/G/H/I all green;
- ADV-035 through ADV-047 remained green in the same full-discovery run;
- explicit compile, including the Decision 015 runtime and ADV-048 test module, passed;
- complete job conclusion: success.

PR #70 was squash-integrated as:

`e832a5f865655c315bdc9fdc3b81db15b8527716`

PR #69 was closed as **superseded, not invalidated**. Its original branch, commits, and run remain preserved evidence.

## Why Stage 4 is not done

Decision 015 tells us exactly where each exact dependency target stands relative to the exact historical claim base and this exact packet's output families. It deliberately does not create a packet-level dependency graph, execution chronology, admissibility policy, dependency closure, or acceptance meaning.

The immediate risk is now hidden chronology: later code could use packet/output/dependency array order, storage order, recency, version, `supersedes_ref`, logical id, or actor status to decide which same-packet dependency came "before" another.

The exact relations already permit one smaller factual step before policy: reconstruct the exact directed graph among the exact outputs of this one packet, preserve self/cycle facts, and—only for an acyclic graph—expose a deterministic topological witness that is explicitly not historical execution chronology.

## Decision 016 — opened next

See:

`coordination/decisions/016_EXACT_SAME_PACKET_DEPENDENCY_GRAPH_FACTS.md`

Decision 016 opens **graph fact before chronology or policy**:

- consume Decision 015 rather than rebuilding identity/membership;
- nodes are exact packet created and modified-result output refs;
- an exact same-packet dependency creates one directed `required_output_ref -> dependent_output_ref` edge;
- base-only and external/unclassified dependencies remain preserved in the nested Decision 015 result but create no packet-local edge;
- exact self-edges and deterministic SCC/cycle facts remain explicit without being accepted or rejected;
- an acyclic graph may expose one exact-ref-lexically-tiebroken topological witness, labelled only as a witness, never as historical execution order;
- no logical-id/version/`supersedes_ref`/recency/array/store/actor/founder/scheduler/Git authority may change graph facts;
- no dependency validity, admissibility, satisfaction, closure, acceptance, publication, integration, epoch, or replay semantics open.

No schema migration is required because the step derives facts from already exact immutable relations.

## Lane boundaries

### Lane 02 — next implementation lane

Implement only Decision 016's read-only exact same-packet dependency graph projection. Consume Decision 015 as the sole context/membership authority. Preserve exact node/edge/self-edge/SCC/cycle facts, expose a topological witness only if acyclic, keep base-only/external dependency facts visible through the nested result, and keep ADV-035 through ADV-048 green. Stop before dependency admissibility, actual chronology, closure/completeness, source closure, packet acceptance, claim closure, successor publication, Stage 5 integration, epochs, or replay.

### Lane 03 — next adversarial lane

After Lane 02 leaves an exact tested head, attack only Decision 016: order/recency/version/`supersedes_ref` authority, same-logical decoy nodes/edges, external/base-only edge promotion, output-family precedence, dropped self-edges, hidden cycles, fake topological witnesses, witness-edge violations, parallel-packet rebinding, metadata authority leakage, transport/materialization drift, and accidental validity/chronology/closure/acceptance authority.

### Lane 01 — integration lane

Do not implement Decision 016 in parallel with Lane 02. Review the exact tested implementation and independent Lane 03 evidence, preserve failures/dissent, and integrate only if the four-root gate is grounded.

## Still explicitly unresolved

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

- **Truth:** exact dependency context and exact packet-local topology remain facts; neither is relabelled as execution history, validity, or closure.
- **Agency / non-domination:** graph facts come from exact immutable relations, not founder/specialist/Git status, version, recency, order, or logical naming.
- **Continuity:** replacement occupants can reconstruct dependency targets, contexts, and packet-local topology from durable state without private chat memory.
- **Wisdom before speed:** graph facts are opened before dependency admissibility, actual chronology, closure, acceptance, integration, epochs, or replay.
