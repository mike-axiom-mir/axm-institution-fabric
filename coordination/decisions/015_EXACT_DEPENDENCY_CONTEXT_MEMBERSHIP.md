# Decision 015 — Exact Dependency Context Membership

Status: **accepted as the next bounded Stage 4 preflight** after Decision 014 and ADV-047.

Decision 014 now proves the exact immutable identity of dependency targets declared by artifact v0.3 packet outputs. ADV-047 independently preserved that identity against corruption, same-logical/version/`supersedes_ref` decoys, historical-string laundering, metadata authority leakage, materialization drift, and unsupported transport. The next missing fact is not dependency validity or closure. It is the narrower question: **where does each already-exact dependency stand relative to the exact historical claim base and the exact packet outputs?**

## Problem

An exact-loadable dependency is not automatically a historically available dependency.

The exact claim-base state revision already contains an exact `artifact_refs[]` membership set under the Stage 2/Decision 005 identity model. Decision 013 also already identifies the packet's exact created outputs and exact modification-result outputs. Decision 014, however, deliberately stops before comparing dependency targets to either context.

Without one explicit factual projection, later code could make either of two ungrounded jumps:

- treat every exact-loadable artifact as though it were a member of the exact claim base; or
- require every dependency to be a claim-base member and thereby silently forbid same-packet dependency relations before any same-packet chronology policy has been decided.

Both would turn policy assumptions into hidden institutional truth.

## Decision

Open one **read-only dependency-context membership projection** that consumes Decision 014 rather than rebuilding dependency identity or packet context.

For every exact dependency relation already resolved by Decision 014, preserve the exact dependency ref/value and add only these factual observations:

1. **Exact claim-base membership** — whether the dependency's exact immutable artifact ref appears in the exact claim-base state revision's `artifact_refs[]` set.
2. **Exact packet-output membership** — which, if any, exact packet output family contains the same exact immutable artifact ref:
   - `created`;
   - `modified_result`.
3. If neither relation is present, preserve that state explicitly as an exact external/unclassified target. Do not reject it merely for being outside those two contexts.
4. If more than one factual relation is simultaneously true, preserve all true facts. Do not invent precedence.

The projection must exact-load and validate the exact `claim_base_ref` through the shared immutable-reference/store path before using its `artifact_refs[]` membership. Membership is exact-ref equality only.

## Explicit non-authorities

The following must not influence membership classification:

- logical artifact id;
- artifact `version`;
- `supersedes_ref`;
- store insertion order or recency;
- dependency array order;
- packet array order;
- `provenance.source_refs[]`;
- artifact-local `evidence_refs[]`;
- actor/founder/specialist identity;
- scheduler position;
- Git permission.

A same-logical-id artifact in the claim base is **not** membership for a different exact dependency ref.

## Bounded runtime meaning

A successful Decision 015 preflight means only that a replacement occupant can reconstruct these exact facts for each Decision 014 dependency target:

- exact target identity;
- whether that exact target is an exact member of the exact claim base;
- whether that exact target is also one of the exact packet outputs and, if so, which output family.

A successful result does **not** mean:

- the dependency is allowed;
- a non-base dependency is invalid;
- a same-packet dependency is valid;
- the dependency existed before its consumer in any causal chronology beyond immutable snapshot membership;
- self-dependency is permitted or forbidden;
- dependency closure is complete;
- transitive dependencies are closed;
- the graph is acyclic;
- all real dependencies were declared;
- packet acceptance/rejection;
- evidence closure;
- claim closure;
- successor publication;
- Stage 5 integration;
- epoch/barrier completion;
- replay correctness.

In particular, Decision 015 is **classification before policy**.

## Lane 02 — smallest implementation

Implement only a read-only `Decision 015` preflight that:

1. consumes `preflight_output_dependency_identity(...)` as the dependency/context authority;
2. exact-loads the exact `claim_base_ref` as a `state-revision` through the shared Stage 2/store path;
3. constructs exact claim-base artifact membership from that revision's `artifact_refs[]` without logical-id fallback;
4. constructs exact packet output membership from Decision 014/013's already-grounded created and modified-result exact refs;
5. returns per-output/per-dependency immutable membership facts while preserving the existing exact relation objects;
6. preserves an exact dependency outside both contexts as explicit factual state rather than acceptance or rejection;
7. gives no precedence if a target appears in more than one factual context;
8. preserves historical empty-dependency behavior without claiming dependency closure;
9. keeps ADV-035 through ADV-047 green;
10. stops before dependency validity, same-packet chronology policy, closure/cycles/completeness, source closure, evidence precedence, lineage, packet acceptance, claim closure, successor publication, Stage 5 integration, epochs, or replay.

No artifact schema version change is required for this step because Decision 015 adds no new artifact-authored claim; it derives factual membership from already exact immutable refs and the already exact historical contexts.

## Lane 03 — adversarial surface

Attack the exact Lane 02 implementation for at least:

- same-logical-id / different-exact artifact in the claim base being misclassified as membership;
- higher version / `supersedes_ref` / later stored decoys changing membership;
- claim-base `artifact_refs[]` order changing facts;
- dependency array order changing facts;
- same-packet created and modified-result output families cross-laundering each other;
- an exact external target being silently rejected or promoted to valid;
- an exact target with more than one factual context being collapsed by precedence;
- source/evidence metadata being treated as membership;
- corrupt/missing/wrong-kind exact claim-base state failing closed;
- detached materialization or unsupported transport changing exact membership facts;
- any aggregate `dependencies_valid`, `dependencies_closed`, `accepted`, `rejected`, `complete`, `closed`, or packet-level `satisfied` authority appearing.

Do not expand this attack into chronology policy, transitive graph closure, cycles, completeness, source closure, evidence precedence, or acceptance unless a later durable decision opens those gates.

## Root grounding

- **Truth:** distinguish exact target identity from exact historical membership instead of narrating every loadable object as historically available.
- **Agency / non-domination:** membership is a deterministic fact of exact immutable refs, not status, recency, version, ordering, founder identity, specialist role, or Git permission.
- **Continuity:** a replacement occupant can recover dependency context from durable repository/store state without hidden chat or mutable-name lookup.
- **Wisdom before speed:** classify exact context before choosing dependency validity, chronology, closure, packet acceptance, integration, epochs, or replay.
