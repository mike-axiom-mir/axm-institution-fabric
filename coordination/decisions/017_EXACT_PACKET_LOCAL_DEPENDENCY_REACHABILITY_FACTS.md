# Decision 017 — Exact Packet-Local Dependency Reachability Facts

Status: **canonical for the demonstrated bounded Python v0 read-only reachability surface after Lane 02 implementation evidence and independent Lane 03 ADV-051 adversarial clearance.**

Decision 016 canonically reconstructs one exact packet-local dependency graph from Decision 015 facts: exact packet-output nodes, exact `required_output_ref -> dependent_output_ref` edges, SCC/self-edge/cycle facts, and one deterministic topological witness only when acyclic. Decision 017 adds only the exact direct and strict-transitive prerequisite reachability implied by that graph.

## Canonical meaning

For each exact packet-output node `O`:

1. **Direct prerequisite refs** are exactly the `required_output_ref` values from Decision 016 edges whose `dependent_output_ref == O`.
2. **Strict transitive prerequisite refs** are every exact packet-output ref reachable from `O` by following one or more prerequisite relations backward through Decision 016 edges.
3. The starting output ref is included in its own strict transitive prerequisite set only when a non-empty cycle/self-edge path returns to it.
4. Presentation is deterministic using exact-ref lexical ordering only. Lexical order is presentation, not semantic priority.
5. Claim-base-only and external/unclassified dependencies remain outside packet-local reachability and stay visible through the nested Decision 015/016 context.
6. Created/modified-result family labels remain factual metadata only and do not affect reachability.
7. The Decision 016 topological witness is preserved in the nested graph result but is not reachability authority or historical production chronology.
8. No cross-packet prerequisite relation is inferred from logical ids, later packets, storage recency, metadata, or current mutable state.

## Integration evidence

### Lane 02 — PR #78

Exact implementation/workflow head:

`7d9eac88734b397b68bb9bd763839c2af7e28f4b`

Exact pull-request merge candidate independently inspected:

`b37495633fef8b891df04d633cdc61be1335fd27`

Native run `34795321386`, job `103827160883`, directly recorded:

- Python 3.12.14;
- **342 / 342 tests passed**;
- duration 342.090s;
- all Decision 017 baseline regressions passed;
- ADV-035 through ADV-050 remained green;
- explicit compile step succeeded;
- complete job succeeded.

Lane 02 final branch head `d017e51f792d91acc26f8414626b921782186e6b` added only its durable return packet after the exact tested implementation/workflow head.

PR #78 was integrated with merge commit:

`94812d89d6a926361c9c41e7e6a5534f8b333dde`

### Lane 03 — PR #79 / ADV-051

Lane 03 changed no production runtime or schema semantics.

The first ADV-051 attempt is preserved as red evidence: native run `34796316580`, job `103830006547`, failed during deterministic unittests and skipped compile. Source review found the adversarial oracle required `copy.copy` / `copy.deepcopy` to succeed even though the already-grounded proof-to-use rule permits **reject or preserve exact meaning**. Lane 03 corrected only that oracle; no production code changed in response.

Exact corrected adversarial head:

`8eeb641218f52dabceff3207f661fdaa9a7415a4`

Exact corrected PR merge candidate:

`189c527a0889b94b2de259bc9af344bea4717009`

Native run `34796704131`, job `103831094736`, was independently inspected and directly recorded:

- Python 3.12.14;
- **352 / 352 tests passed**;
- duration 538.405s;
- ADV-051-A through J all passed;
- explicit compile including the ADV-051 file succeeded;
- complete job succeeded.

ADV-051 covers diamond/multi-hop reachability, hostile lexical ordering, cycle plus upstream prerequisite behavior, sibling non-laundering, sequential parallel-packet projection isolation, topological-witness non-authority, duplicate-node fail-closed behavior, named leaf proof-to-use transport, aggregate transport boundary, and absence of policy/lifecycle authority.

After Decision 017 became canonical, PR #79 was retargeted to `main`; its diff contained only workflow coverage, ADV-051 tests, and the durable Lane 03 return packet. It was integrated as:

`2e8f91f78ebf03b8b7cba58dfe2bdb8f38b485e9`

The initial red adversarial run remains valid historical evidence about the original Lane 03 oracle and is not rewritten as a production failure or erased by the corrected green run.

## Exact non-authorities

Reachability is not selected or changed by:

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
- lexical position except deterministic presentation ordering.

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

## Proof-to-use representation boundary

Decision 017's per-output reachability leaf uses a canonical-byte-backed named immutable representation. Unsupported ordinary Python stdlib JSON transport fails closed rather than silently converting named institutional meaning into positional data. Named detached materialization remains available through the bounded `_asdict()` path.

This is an in-process Python v0 proof-to-use boundary, not a supported cross-language or durable serialization protocol.

## Preserved uncertainty

The exact cycle-authorability question remains unresolved. Artifact v0.3 refs are content-addressed over bytes that include `dependency_refs[]`; a direct exact self-reference appears to require a cryptographic fixed point and a mutual exact cycle appears to require mutually recursive fixed points. Decision 017 preserves reachability behavior for already-grounded cyclic graph facts without claiming the ordinary object-store publication path can author such cycles.

Supported cross-language graph/reachability transport also remains unresolved beyond the established reject-or-preserve-named-semantics boundary.

Dependency admissibility, satisfaction, declaration completeness/closure policy, source/evidence closure, packet acceptance, claim closure, successor publication, Stage 5 integration, epochs, and replay all remain unopened by this decision.

## Root grounding

- **Truth:** canonical status is limited to directly observed implementation/adversarial evidence and exact graph reachability; the original red Lane 03 oracle run remains preserved.
- **Agency / non-domination:** no founder, specialist, scheduler, Git permission, recency, version, family, logical id, or ordering convention chooses prerequisites.
- **Continuity:** a replacement occupant can reconstruct the same direct and transitive packet-local prerequisite facts from explicit institutional state instead of private graph-walking assumptions.
- **Wisdom before speed:** canonical reachability does not authorize dependency policy, closure, packet acceptance, integration, epochs, or replay.
