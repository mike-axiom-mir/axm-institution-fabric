# Decision 016 — Exact Same-Packet Dependency Graph Facts

Status: **canonical as of 2026-09-14 after Lane 02 repair and independent Lane 03 re-attack. Historical pre-repair failure evidence remains valid and preserved.**

Decision 015 reconstructs, for every exact Decision 014 dependency target, whether that exact target is present in the exact historical claim base and/or one of the exact outputs of the same return packet. ADV-048 independently preserves those facts against later revisions, same-logical/version/`supersedes_ref` decoys, presentation order, output-family laundering, metadata authority leakage, missing/corrupt historical state, parallel packet rebinding, materialization drift, and accidental acceptance authority.

The missing fact addressed here is narrower than dependency validity: **what exact dependency graph exists among the outputs of this one exact packet?**

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

Provide one **read-only exact same-packet dependency graph projection** that consumes Decision 015 rather than rebuilding packet, output, dependency, or membership selection.

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

## Canonical implementation boundary

The integrated runtime consumes `preflight_dependency_context_membership(...)` as the sole authority for exact packet context and dependency membership, constructs exact packet-output nodes and packet-local edges, preserves nested Decision 015 facts, records deterministic SCC/self-edge/cycle facts, and exposes a lexical-tie-broken topological witness only for acyclic graphs.

The equivalent named graph leaf family is canonical-byte-backed and immutable:

- `ExactPacketOutputNode`;
- `ExactSamePacketDependencyEdge`;
- `ExactStronglyConnectedComponent`.

Unsupported Python stdlib JSON transport fails closed instead of silently converting those named records into positional arrays. `_asdict()` is a detached named materialization path, not an authority rewrite.

The aggregate graph remains a read-only in-process projection; this decision does not claim a supported cross-language graph protocol.

## Integration evidence and preserved failure history

The original in-process Decision 016 candidate passed its bounded graph tests but Lane 03 ADV-049 found one proof-to-use transport failure: tuple-backed `ExactSamePacketDependencyEdge` could become an unlabeled `[required, dependent]` JSON array. Two native Lane 03 runs each recorded **321 tests / 320 passed / exactly ADV-049-J failed**, with ADV-049-A through I and all prior tests green.

Lane 02 repaired the equivalent graph leaf family coherently. Exact repaired tested head:

`0d8a79142d87eb6a060cb167cb086f194d1ed2d2`

Native run `34792255883`, job `103818527871`, directly recorded:

- **324 / 324 tests passed**;
- ADV-049-A through J all passed;
- three coherent node/edge/SCC transport regressions passed;
- all Decision 016 baseline regressions passed;
- explicit `py_compile` success.

Lane 03 then independently re-attacked the repair with ADV-050 at exact tested head:

`becb799c4d2845f891abdf9fed1d927fa98c90fa`

Native run `34792949677`, job `103820507263`, recorded full deterministic unittest discovery success, explicit compile success, and complete job success. ADV-050 covers physical named edge payload, nested transport, detached materialization, copy/deepcopy handling, and the aggregate positional-transport trap.

Decision 016 production/history was integrated through PR #72 as merge commit:

`82713b5c2f65a3ad827c43f26aaf4f4e05f4df9d`

ADV-050 evidence was integrated through PR #76 as:

`340ef608693b9706e71f86c8d8c3f4cb2e13f525`

Historical failing PR #73 was closed as **superseded, not invalidated**. Its failure evidence remains part of the truth record.

## Preserved representation uncertainty

Artifact v0.3 exact refs hash canonical artifact bytes that include `dependency_refs[]`. Authoring a direct exact self-dependency appears to require a cryptographic fixed point; mutual exact cycles appear to require mutually recursive fixed points.

Decision 016 preserves/detects already-grounded cyclic topology at the deterministic graph-kernel layer. Current evidence does **not** prove that the normal content-addressed object-store publication path can author exact self/mutual cycles end-to-end. Do not silently convert that uncertainty into validity policy or an impossibility claim.

## Root grounding

- **Truth:** represent exact dependency topology as topology, preserve both pre-repair failures and repaired/adversarial success, and do not invent execution history or acceptance.
- **Agency / non-domination:** no founder, specialist, scheduler, Git, recency, version, array-order, logical-id, or tuple convention determines graph facts.
- **Continuity:** a replacement occupant can reconstruct packet-local topology and named edge meaning solely from durable exact state and repository evidence.
- **Wisdom before speed:** expose graph facts before choosing dependency admissibility, chronology, closure, acceptance, integration, epochs, or replay.
