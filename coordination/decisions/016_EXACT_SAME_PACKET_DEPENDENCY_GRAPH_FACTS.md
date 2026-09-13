# Decision 016 — Exact Same-Packet Dependency Graph Facts

Status: **accepted as the next bounded Stage 4 preflight after Decision 015 and ADV-048, subject to implementation and adversarial evidence before integration.**

Decision 015 now reconstructs, for every exact Decision 014 dependency target, whether that exact target is present in the exact historical claim base and/or one of the exact outputs of the same return packet. ADV-048 independently preserves those facts against later revisions, same-logical/version/`supersedes_ref` decoys, presentation order, output-family laundering, metadata authority leakage, missing/corrupt historical state, parallel packet rebinding, materialization drift, and accidental acceptance authority.

The next missing fact is narrower than dependency validity: **what exact dependency graph exists among the outputs of this one exact packet?**

## Problem

Decision 015 exposes packet-output membership per dependency, but later code could still invent packet-level ordering or chronology from:

- `artifacts_created[]` / `artifacts_modified[]` array order;
- dependency declaration order;
- store insertion order or recency;
- artifact version;
- `supersedes_ref`;
- logical ids;
- actor, founder, specialist, scheduler, or Git authority.

None of those is a grounded chronology source.

At the same time, exact same-packet dependency relations already contain useful deterministic facts. A dependency from one exact packet output to another exact packet output is an exact directed relation. A replacement occupant should be able to reconstruct the packet-local graph, including self-relations and cycles, without silently turning that graph into execution history or acceptance policy.

## Decision

Open one **read-only exact same-packet dependency graph projection** that consumes Decision 015 rather than rebuilding packet, output, dependency, or membership selection.

For one exact packet:

1. Graph nodes are the exact immutable refs of the packet's exact created outputs and exact modified-result outputs already grounded by Decision 015/013.
2. For every dependency relation on an output where Decision 015 says the exact dependency target is a packet output, create one exact directed edge:

   ```text
   required_output_ref -> dependent_output_ref
   ```

   The edge means only that the dependent output declares the required output's exact artifact as a dependency. It does **not** prove that the required output was physically produced first.
3. Preserve output-family facts for nodes and dependency-context facts through the nested Decision 015 result. Do not use category as precedence.
4. Preserve exact self-edges as facts. Do not silently reject or delete them.
5. Detect strongly connected components / cycle facts deterministically. A cycle is a graph fact only; this decision does not declare it valid or invalid.
6. When and only when the exact same-packet graph is acyclic, the projection may expose one deterministic **topological witness** using exact-ref lexical ordering solely as a presentation tie-breaker. The witness means only that at least one ordering is consistent with the declared edges. It is **not** historical execution chronology, scheduler authority, acceptance authority, or a required production order.
7. Exact dependencies that are claim-base-only or external/unclassified remain preserved in the nested Decision 015 projection but create no same-packet graph edge.
8. No cross-packet edge is inferred from logical id, later packets, storage state, provenance/source metadata, or any mutable/current lookup.

## Exact non-authorities

The graph and any witness must not be selected or changed by:

- logical artifact id;
- artifact `version`;
- `supersedes_ref`;
- `provenance.source_refs[]`;
- artifact-local `evidence_refs[]`;
- packet/output/dependency array order;
- store insertion order or recency;
- newest/current lookup;
- actor/founder/specialist identity;
- scheduler position;
- Git permission.

Exact immutable refs and the exact Decision 015 relations are the only graph-selection authority.

## Bounded runtime meaning

A successful Decision 016 projection establishes only that a replacement occupant can reconstruct:

- the exact packet-local output node set;
- the exact declared dependency edges between those output nodes;
- exact self-edge and cycle/SCC facts;
- and, for an acyclic graph, one deterministic non-authoritative topological witness.

It does **not** establish:

- that same-packet dependencies are allowed;
- that claim-base-only dependencies are sufficient or valid;
- that external dependencies are invalid;
- actual production timestamps or execution chronology;
- dependency satisfaction;
- transitive dependency closure or declaration completeness;
- whether cycles or self-dependencies are acceptable;
- exact source-provenance taxonomy or closure;
- evidence quality, precedence, invalidation, or closure;
- packet acceptance/rejection;
- claim closure;
- successor state-revision publication;
- Stage 5 integration;
- epoch/barrier completion;
- replay correctness.

This is **graph fact before chronology or policy**.

## Lane 02 — smallest implementation

Implement only a read-only Decision 016 projection that:

1. consumes `preflight_dependency_context_membership(...)` as the sole authority for the exact packet context and dependency membership facts;
2. constructs one exact node per packet created/modified-result output ref;
3. constructs an exact edge only when a dependency target is exactly one of those packet outputs;
4. preserves the underlying Decision 015 result so base-only/external dependency facts are not erased;
5. records self-edges and deterministic SCC/cycle facts without assigning validity;
6. if acyclic, computes one deterministic topological witness with exact-ref lexical tie-breaking and labels it explicitly as a witness rather than chronology;
7. if cyclic, exposes no fake topological witness;
8. exposes no `dependencies_valid`, `dependencies_closed`, `accepted`, `rejected`, `complete`, `closed`, packet-level `satisfied`, or execution-time field;
9. keeps ADV-035 through ADV-048 green;
10. stops before dependency admissibility, same-packet chronology policy, closure/completeness, source closure, evidence precedence, lineage policy, packet acceptance, claim closure, successor publication, Stage 5 integration, epochs, or replay.

No schema migration is required for this step because it derives graph facts from already exact immutable relations and adds no new artifact-authored or packet-authored claim.

## Lane 03 — adversarial surface

Attack the exact Lane 02 head for at least:

- packet/output/dependency array order changing node, edge, SCC, cycle, or witness facts;
- same-logical-id / higher-version / `supersedes_ref` decoys becoming graph nodes or edges;
- claim-base-only or external dependencies being promoted into same-packet edges;
- created/modified-result family facts being collapsed into hidden precedence;
- exact self-dependencies being silently dropped or automatically rejected;
- two-node and larger cycles being hidden, broken by presentation order, or assigned a fake topological witness;
- an acyclic graph's witness violating an exact dependency edge;
- later/parallel packet outputs rebinding an earlier packet's graph;
- source/evidence metadata changing graph structure;
- detached materialization or unsupported transport changing exact graph facts;
- any accidental execution-chronology, validity, closure, acceptance, integration, epoch, or replay authority appearing.

Do not expand the attack into deciding whether same-packet edges, self-dependencies, or cycles are permitted. That policy remains closed until a later durable decision.

## Root grounding

- **Truth:** represent exact dependency topology as topology, not as invented execution history or acceptance.
- **Agency / non-domination:** no founder, specialist, scheduler, Git, recency, version, array-order, or logical-id authority determines graph facts.
- **Continuity:** a replacement occupant can reconstruct the packet-local dependency topology, including cycles, solely from durable exact state.
- **Wisdom before speed:** expose graph facts before choosing dependency admissibility, chronology, closure, acceptance, integration, epochs, or replay.
