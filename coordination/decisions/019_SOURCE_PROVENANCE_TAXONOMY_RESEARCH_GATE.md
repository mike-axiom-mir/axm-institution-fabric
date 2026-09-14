# Decision 019 — Source Provenance Taxonomy Research Gate

Date: 2026-09-14
Status: **research gate accepted; no implementation or schema migration is authorized by this decision**
Stage: **Stage 4 — claim / occupancy / return lifecycle**

## Why this gate exists

Decision 018 makes the reachable dependency frontier explicit without inventing dependency policy. The next unresolved continuity surface is source provenance, but the repository does not yet contain enough grounded semantics to truthfully turn historical source strings into immutable institutional identities.

Two existing universal-kernel surfaces currently use deliberately broad source strings:

1. `artifact.provenance.source_refs[]` is an array of arbitrary non-empty strings in artifact schema v0.1, v0.2, and v0.3.
2. `evidence-record.source_refs[]` is an array of arbitrary non-empty strings in evidence-record schema v0.1.

The historical valid contract fixture proves that these fields have already carried path-like values such as `NEXT_BUILD.md`, `BUILD_PLAN.md`, `coordination/decisions/...`, and `fixtures/contracts/valid.json`. Those values are useful provenance statements, but they are not exact immutable institution-object identities merely because a later implementation could parse or resolve them.

Therefore the next safe step is **taxonomy research before exact-source implementation**.

## Constitutional boundary

This gate is grounded by the four AXM roots:

- **Truth:** preserve what historical source strings actually asserted; do not silently relabel locations, paths, URLs, Git-ish strings, or exact-looking strings as stronger immutable evidence than their contract defined.
- **Agency / non-domination:** no founder, specialist, resolver, filesystem location, network service, newest version, or parser convention may become hidden source authority.
- **Continuity:** a future occupant must be able to reconstruct whether a source relation is exact, content-addressed, location-only, external, unavailable, or still opaque from durable state rather than private convention.
- **Wisdom before speed:** define the source categories and their identity strength before adding runtime closure, trust, quality, acceptance, or policy semantics.

## Historical non-reinterpretation rule

Until an explicit versioned contract says otherwise:

- historical `artifact.provenance.source_refs[]` values remain opaque source strings;
- historical `evidence-record.source_refs[]` values remain opaque source strings;
- an `axmref:`-looking historical string does **not** gain exact-reference standing by lexical shape alone;
- path-like, URL-like, Git-like, hash-like, or logical-id-like strings do not gain existence, immutability, recency, trust, or closure authority;
- `content_ref`, `dependency_refs`, `evidence_refs`, `supersedes_ref`, and source provenance remain separate relations and must not be cross-laundered.

## Research questions that must be answered before implementation

The next architecture pass must inventory the smallest universal source classes actually required by AXM Institution Fabric and record examples/counterexamples for each. At minimum it must determine whether the universal kernel needs distinct representations for:

- exact immutable AXM object sources;
- content-addressed byte/blob sources that are not AXM objects;
- repository/file snapshot sources where a path alone is insufficient identity;
- external/network sources whose bytes may be unavailable later;
- human or machine assertions that name a source without proving retrievability;
- unresolved historical opaque source strings.

For every proposed class, the research must state separately:

1. **identity** — what exactly is named;
2. **existence/retrievability** — whether the named thing can be loaded now;
3. **integrity** — whether bytes/content can be reproduced and verified;
4. **provenance relation** — what relation the source has to the subject;
5. **quality/trust** — explicitly separate from identity and existence;
6. **closure** — explicitly unopened unless separately grounded;
7. **offline/replay behavior** — what survives without network or original occupant;
8. **migration** — how historical opaque strings remain truthful rather than being silently upgraded.

## Forbidden shortcuts

This research gate rejects the following shortcuts unless a later numbered decision grounds them with evidence:

- treating every source as an artifact;
- treating every path or URL as immutable identity;
- treating every syntactically valid `axmref` in a historical opaque field as authoritative;
- treating source presence as evidence quality, trust, satisfaction, closure, acceptance, or permission;
- selecting a source by newest version, recency, lexical order, array order, resolver preference, network availability, or Git permission;
- requiring internet, a specific repository host, a specific filesystem layout, or a model-specific source type in the universal kernel;
- rewriting artifact/evidence history in place.

## What this decision does not open

Decision 019 does **not** open:

- a new artifact or evidence schema version;
- exact source-reference parsing in operational paths;
- source target loading;
- source completeness/closure;
- evidence quality or precedence;
- dependency admissibility or satisfaction;
- packet acceptance/rejection;
- claim closure;
- successor state publication;
- Stage 5 integration receipts/runtime;
- epochs/barriers;
- replay;
- model-heavy autonomy.

## Required research return packet

Before Lane 02 receives an implementation assignment, Lane 01 should leave a durable research packet containing:

- repository-wide inventory of current source-bearing fields and representative values;
- proposed minimal universal source taxonomy;
- at least one rejected over-broad taxonomy with reasons;
- migration/non-reinterpretation rules;
- offline and replay implications;
- adversarial cases for stale locations, mutable URLs/paths, same-label/different-bytes, exact-looking opaque strings, missing sources, and conflicting source claims;
- a recommendation either to open a bounded implementation decision or to keep source identity unresolved.

## Current lane allocation

- **Lane 01:** research and bound the source taxonomy; do not implement source semantics yet.
- **Lane 02:** no source-provenance implementation is authorized by this gate; remain available for the next explicit bounded implementation decision.
- **Lane 03:** do not invent an attack target until Lane 01 publishes a concrete taxonomy proposal; then challenge identity-strength laundering, hidden resolver authority, migration drift, and accidental trust/closure semantics.

## Stop condition

Stop this gate when the repository contains enough explicit source categories, examples, counterexamples, migration rules, and truth boundaries for another occupant to implement the next smallest source-provenance step without relying on private chat state or guessing what `source_refs[]` meant.
