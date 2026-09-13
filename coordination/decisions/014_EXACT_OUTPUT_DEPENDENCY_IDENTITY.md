# Decision 014 — Exact Output Dependency Identity

Status: **accepted as the next bounded Stage 4 preflight** after Decision 013 and ADV-046. Decision 013 can now reconstruct created outputs and modified-result outputs from one exact return packet and one exact historical context, while preserving their evidence facts without inventing packet acceptance. The next concrete continuity gap is narrower than dependency closure: output artifacts can still name `dependency_refs[]` as arbitrary strings, so an exact output does not yet prove the exact identity of the dependencies it says it used.

## Problem

The canonical artifact contract currently distinguishes work-base provenance from dependency relations, but dependency identity is still weak:

- artifact v0.1 historically accepts arbitrary non-empty `dependency_refs[]` strings;
- artifact v0.2 added exact `provenance.base_state_revision_ref`, but left `dependency_refs[]` as arbitrary non-empty strings;
- the historical contract fixture uses a path-like dependency (`schemas/lane.schema.json`), proving that old dependency strings cannot honestly be re-labelled as immutable institutional refs;
- Decision 013 exact-loads packet outputs and evidence, but deliberately makes no source/dependency-closure claim.

Therefore an exact artifact ref can identify one exact output while its declared dependency string still points only to a mutable path, logical name, or other unresolved token. Later integration or replay must not silently interpret such a token as “the dependency that was meant.”

The missing fact is **dependency target identity**, not dependency validity or closure.

## Decision

Open one read-only preflight that gives new output artifacts an explicit exact dependency-identity language while preserving historical artifacts unchanged.

### Artifact contract boundary

Introduce artifact schema **v0.3** only for the new dependency-identity surface.

For v0.3:

1. `dependency_refs[]` entries must be canonical immutable refs of kind `artifact` using the shared Stage 2 reference language;
2. each declared dependency ref must exact-load and reproduce the same immutable artifact identity through the canonical object store;
3. `dependency_refs[]` remains an ordered presentation array with no ordering authority; identity is the full exact ref;
4. `provenance.base_state_revision_ref` and producer-lane rules from v0.2 remain unchanged;
5. `provenance.source_refs[]`, `evidence_refs[]`, `content_ref`, `version`, and `supersedes_ref` do not become dependency authority.

Historical artifact v0.1 and v0.2 remain historical:

- an empty `dependency_refs[]` list has no dependency fact to reinterpret and may continue through the bounded preflight;
- a non-empty v0.1/v0.2 dependency list remains **operationally unresolved** for exact dependency identity, even if one string happens to look like an `axmref`;
- no path, logical id, newest/current lookup, version, storage order, packet order, or `supersedes_ref` fallback upgrades historical dependency strings into v0.3 meaning.

## Bounded runtime meaning

For one exact packet already grounded by Decision 013:

1. consume the exact packet / claim / claim-base / occupancy / historical-lane context from the canonical mixed compatibility projection rather than rebuilding a parallel authority path;
2. inspect both exact created outputs and exact modification-result outputs;
3. for each output artifact, preserve its exact output ref/value relation;
4. if the artifact is v0.3, parse every dependency through the shared immutable-ref parser, require kind `artifact`, exact-load it, and return the exact dependency ref/value relation;
5. if the artifact is v0.1/v0.2 with non-empty dependencies, fail closed with an explicit historical-semantics-unresolved error;
6. if the artifact has no dependencies, return an empty dependency relation set without implying global closure;
7. preserve created-vs-modified-result category and all Decision 013 compatibility/evidence facts unchanged.

A successful Decision 014 preflight means only: **for every dependency relation that this bounded path claims to understand, the dependency target is one exact immutable artifact and can be exact-loaded without fallback.**

It does not establish that the dependency is allowed, complete, acyclic, historically available at the right moment, semantically necessary, or ready for integration.

## Explicit non-decisions

Decision 014 does **not** decide:

- whether a dependency must be a member of the exact claim base;
- whether same-packet outputs may depend on each other;
- dependency chronology or producer/consumer ordering;
- transitive dependency closure;
- cycle detection;
- whether all real dependencies were declared;
- source provenance identity or closure for `provenance.source_refs[]`;
- evidence source quality or closure;
- logical lineage or `supersedes_ref` validity;
- multiple `required_states` semantics;
- conflicting evidence precedence or invalidation dominance;
- packet acceptance/rejection;
- claim closure;
- successor state publication;
- Stage 5 integration receipts/runtime;
- epochs/barriers or replay.

Those remain later gates. In particular, an exact dependency ref is not evidence that the relationship itself is valid.

## Lane 02 — smallest next implementation

Implement only the **read-only exact output dependency identity preflight**.

Required bounded behavior:

1. add artifact schema v0.3 without changing v0.1/v0.2 historical meaning;
2. require v0.3 dependency entries to use canonical exact `artifact` refs;
3. consume Decision 013's exact mixed-output context and do not fork packet/lane selection logic;
4. exact-load every v0.3 dependency through the shared Stage 2 parser/store path;
5. preserve exact dependency ref/value pairs in a stable read-only operational representation;
6. allow empty historical dependency arrays without claiming more than “no declared dependency relation on this surface”;
7. fail closed on non-empty v0.1/v0.2 dependency arrays rather than reinterpreting them;
8. preserve created-only, modified-only, and mixed packet behavior from Decision 013;
9. preserve ADV-035 through ADV-046 unchanged;
10. stop before dependency membership/closure, source closure, evidence precedence, lineage, packet acceptance, claim closure, successor publication, Stage 5 integration, epochs, or replay.

A schema/version change is required here specifically to avoid silent historical reinterpretation.

## Lane 03 — adversarial surface

Attack the exact Lane 02 implementation for at least:

- a v0.1/v0.2 dependency string that looks exactly like a canonical artifact ref gaining v0.3 standing;
- a bare logical id or path being followed by lookup or recency;
- a canonical exact ref of the wrong kind;
- a missing or corrupt exact dependency target;
- a same-logical-id / different-exact artifact being substituted;
- dependency array reordering changing standing;
- `version` or `supersedes_ref` changing dependency selection;
- `provenance.source_refs[]` or `evidence_refs[]` being treated as dependency authority;
- created and modified-result outputs receiving different hidden dependency semantics;
- ordinary materialization/transport breaking ref/value continuity;
- any new aggregate “dependencies closed” or packet acceptance claim appearing from identity-only evidence.

Do not expand the attack into dependency membership/chronology/closure or packet acceptance until repository state explicitly opens those gates.

## Root grounding

- **Truth:** an exact output is no longer allowed to make a stronger dependency-identity claim from an arbitrary historical string; historical semantics remain explicit rather than rewritten.
- **Agency / non-domination:** dependency standing comes from exact durable identity, not actor intent, founder status, specialist role, Git permission, ordering, recency, or version metadata.
- **Continuity:** a replacement occupant can reconstruct the exact dependency object intended by a v0.3 output without private chat state or mutable-name lookup.
- **Wisdom before speed:** establish dependency identity first; do not jump directly from green mixed compatibility into dependency closure, packet acceptance, integration, epochs, or replay.
