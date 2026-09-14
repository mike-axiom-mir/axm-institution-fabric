# Decision 017 — Exact Packet-Local Dependency Reachability Facts

Status: **accepted as the next bounded Stage 4 preflight after canonical Decision 016, subject to implementation and adversarial evidence before integration.**

Decision 016 now canonically reconstructs one exact packet-local dependency graph from Decision 015 facts: exact packet-output nodes, exact `required_output_ref -> dependent_output_ref` edges, SCC/self-edge/cycle facts, and one deterministic topological witness only when acyclic. The graph intentionally carries no dependency validity, execution chronology, closure, acceptance, integration, epoch, or replay authority.

The next missing fact is still narrower than dependency policy: **for each exact packet output, which other exact packet outputs are its direct and transitive packet-local prerequisites according to the already-grounded graph?**

## Problem

A later consumer can derive reachability from Decision 016, but leaving that derivation implicit creates room for continuity drift before policy even begins. Different occupants or runtimes could accidentally:

- reverse edge direction;
- include only direct prerequisites and omit multi-hop prerequisites;
- promote claim-base-only or external dependencies into packet-local prerequisite sets;
- choose by logical id, version, recency, `supersedes_ref`, array order, family, or scheduler state;
- treat a topological witness as historical chronology;
- erase or fabricate self-reachability in a cycle;
- convert deterministic graph facts into dependency validity or acceptance claims.

Those would be new hidden authority paths, not facts supplied by Decision 016.

## Decision

Open one **read-only exact packet-local dependency reachability projection** that consumes Decision 016 unchanged rather than rebuilding packet, output, dependency, membership, node, or edge selection.

For each exact packet-output node `O`:

1. **Direct prerequisite refs** are exactly the `required_output_ref` values from Decision 016 edges whose `dependent_output_ref == O`.
2. **Strict transitive prerequisite refs** are every exact packet-output ref reachable from `O` by following one or more prerequisite relations backward through Decision 016 edges.
3. The starting output ref is included in its own strict transitive prerequisite set only when a non-empty cycle/self-edge path returns to it.
4. Presentation is deterministic using exact-ref lexical ordering only. Lexical order is presentation, not semantic priority.
5. Claim-base-only and external/unclassified dependencies remain outside packet-local reachability. They remain visible through the nested Decision 015/016 context but are not silently promoted into packet-local nodes or prerequisite sets.
6. Created/modified-result family labels remain factual metadata only and do not affect reachability.
7. The Decision 016 topological witness may be preserved in the nested graph result but must not become reachability authority or historical production chronology.
8. No cross-packet prerequisite relation may be inferred from logical ids, later packets, storage recency, metadata, or current mutable state.

## Exact non-authorities

Reachability must not be selected or changed by:

- logical artifact id;
- artifact `version`;
- `supersedes_ref`;
- `provenance.source_refs[]`;
- artifact-local `evidence_refs[]`;
- packet/output/dependency array order;
- store insertion order or recency;
- newest/current lookup;
- output family;
- actor/founder/specialist identity;
- scheduler position;
- Git permission;
- lexical position except as deterministic presentation ordering.

Decision 016 exact nodes and edges are the sole packet-local reachability authority.

## Bounded runtime meaning

A successful Decision 017 projection establishes only that a replacement occupant can deterministically reconstruct, for every exact packet output:

- its exact direct packet-local prerequisites;
- its exact strict transitive packet-local prerequisites;
- cycle/self-reachability facts already implied by Decision 016 topology.

It does **not** establish:

- that any dependency context is allowed;
- that dependencies are satisfied;
- that all necessary dependencies were declared;
- transitive dependency closure or declaration completeness as policy;
- actual production timestamps or execution chronology;
- a required scheduler order;
- whether cycles or self-dependencies are acceptable;
- source-provenance closure;
- evidence quality, precedence, invalidation, or closure;
- packet acceptance/rejection;
- claim closure;
- successor state-revision publication;
- Stage 5 integration;
- epoch/barrier completion;
- replay correctness.

This remains **graph fact before dependency policy**.

## Lane 02 — smallest implementation

Implement only a read-only Decision 017 projection that:

1. consumes `preflight_same_packet_dependency_graph(...)` as the sole packet-local graph authority;
2. emits one deterministic per-output reachability record for each exact Decision 016 node;
3. records direct prerequisite refs exactly from incoming Decision 016 edges;
4. records strict transitive prerequisite refs by path length >= 1;
5. preserves self-reachability only when a self-edge or longer cycle grounds it;
6. preserves the nested Decision 016 graph so all upstream exact context remains inspectable;
7. keeps claim-base-only/external dependencies outside packet-local prerequisite sets;
8. exposes no `valid`, `allowed`, `satisfied`, `closed`, `complete`, `accepted`, `rejected`, `integrated`, epoch, replay, or execution-time field;
9. if introducing new named operational leaf records, follows the established proof-to-use rule: unsupported ordinary transport must fail closed or preserve named meaning exactly;
10. keeps ADV-035 through ADV-050 green;
11. stops before dependency admissibility, closure/completeness policy, source/evidence closure, packet acceptance, claim closure, successor publication, Stage 5 integration, epochs, or replay.

No schema migration is required for this bounded step because it derives read-only facts from already exact immutable relations and adds no artifact-authored or packet-authored claim.

## Minimum implementation regressions

At minimum, prove:

- one direct edge produces one direct and one transitive prerequisite for the dependent output;
- a three-node chain gives the final output both direct and multi-hop transitive prerequisites;
- an independent node gains no prerequisite merely from lexical or array position;
- claim-base-only and external dependencies do not enter packet-local reachability;
- created and modified-result nodes participate without family precedence;
- changing packet/output/dependency array order does not change reachability facts;
- same-logical-id / different-exact-ref decoys do not substitute;
- a self-edge makes the node strictly reachable from itself;
- a two-node cycle makes each member strictly reachable from itself and the other member at the graph-fact layer;
- an acyclic node is not spuriously self-reachable;
- no validity, chronology, closure, acceptance, integration, epoch, or replay authority appears.

Cycle tests may remain direct graph-kernel tests where exact content-addressed cycle authorability is still unproven; do not relabel them as end-to-end publication evidence.

## Lane 03 — adversarial surface

Attack the exact Lane 02 head for at least:

- required/dependent direction inversion;
- omission of multi-hop prerequisites;
- inclusion of unrelated lexical neighbours;
- claim-base-only or external dependency promotion;
- same-logical-id / high-version / `supersedes_ref` decoys entering reachability;
- created/modified-result family precedence;
- packet/output/dependency array order changing prerequisite sets;
- storage recency or later parallel packet outputs rebinding reachability;
- self/cycle reachability being dropped, invented, or replaced by a topological witness;
- topological witness order becoming historical chronology or scheduler authority;
- materialization/transport changing exact named reachability facts;
- any accidental dependency-validity, closure, acceptance, integration, epoch, or replay semantics.

Do not expand the attack into deciding whether same-packet dependencies, base dependencies, external dependencies, self-dependencies, or cycles are permitted.

## Preserved uncertainty

The exact cycle-authorability question remains unresolved. Artifact v0.3 refs are content-addressed over bytes that include `dependency_refs[]`; a direct exact self-reference appears to require a cryptographic fixed point and a mutual exact cycle appears to require mutually recursive fixed points. Decision 017 may preserve reachability behavior for already-grounded cyclic graph facts without claiming the ordinary object-store publication path can author such cycles.

Supported cross-language graph/reachability transport also remains unresolved beyond the established reject-or-preserve-named-semantics boundary.

## Root grounding

- **Truth:** derive only exact graph reachability already implied by canonical Decision 016; do not relabel it validity, chronology, closure, or acceptance.
- **Agency / non-domination:** no founder, specialist, scheduler, Git permission, recency, version, family, logical id, or ordering convention chooses prerequisites.
- **Continuity:** a replacement occupant can reconstruct the same direct and transitive packet-local prerequisite facts from explicit institutional state instead of private graph-walking assumptions.
- **Wisdom before speed:** ground deterministic reachability before choosing dependency admissibility, closure/completeness, packet acceptance, integration, epochs, or replay.
