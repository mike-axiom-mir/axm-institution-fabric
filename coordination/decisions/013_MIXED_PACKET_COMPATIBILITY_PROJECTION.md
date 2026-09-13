# Decision 013 — Mixed Packet Compatibility Projection

Status: **accepted as the next bounded Stage 4 preflight** after Decision 012. Decision 012 now gives a tested read-only compatibility result for exact modification **result** endpoints, while the older created-output compatibility path remains intentionally unable to operate when `artifacts_modified[]` is non-empty. This decision opens only the smallest composition layer needed to inspect created outputs and modified results from the same exact v0.4 packet without inventing packet acceptance semantics.

## Problem

The canonical Stage 4 surfaces are now individually stronger than their composition:

```text
created output path
  -> exact packet-created artifact identity
  -> exact evidence subject binding
  -> narrow one-state output/evidence compatibility
  -> currently fails closed when artifacts_modified[] is non-empty

modified result path
  -> Decision 011 exact prior/result identity
  -> Decision 010 result provenance
  -> Decision 012 narrow one-state result/evidence compatibility
```

This means a v0.4 packet that truthfully contains both created artifacts and modified-artifact relations cannot yet obtain one read-only institutional projection of **both** output families. Calling the old created-output resolver would reject the packet solely because modifications are present; treating modification results as created artifacts would erase Decision 011's prior/result distinction; and running independent ad-hoc lookups risks reconstructing different lane or evidence contexts.

The missing fact is composition, not acceptance.

## Decision

Add one read-only mixed-packet compatibility projection that composes the already-grounded created-output and modified-result rules while preserving their boundaries.

For one exact v0.4 return packet `P`:

1. reconstruct one exact historical packet/claim/base/occupancy/lane context from durable state;
2. treat `artifacts_created[]` only as exact created-result refs;
3. treat `artifacts_modified[]` only through Decision 011 explicit `{prior_artifact_ref, result_artifact_ref}` relations;
4. evaluate created artifacts using the already-canonical exact subject-binding and one-output / one-evidence-requirement / one-required-state compatibility semantics;
5. evaluate modification results using Decision 012 unchanged;
6. require both output families to refer to the same exact packet, claim, claim base, occupancy, and historical lane context before exposing them together;
7. bind packet evidence only by exact evidence-record identity plus exact `subject_ref`; evidence does not move between created and modified outputs by type, logical id, order, recency, version, `supersedes_ref`, or actor intent;
8. preserve unmatched, additional, conflicting, and invalidated evidence explicitly;
9. if one exact artifact ref is simultaneously classified by the packet as a created artifact and as a modification result, fail closed at this composition preflight rather than silently choosing or deduplicating a category; this does **not** yet declare the packet globally invalid;
10. return the per-output compatibility facts without inventing one packet-level `accepted`, `complete`, `closed`, or aggregate `satisfied` boolean.

A successful mixed projection means only that the same exact historical context can reconstruct both already-supported output families and their bounded compatibility facts. It is not packet acceptance.

## Required representation boundary

The old created-output identity resolver remains historically valid for the surface it proved, including its fail-closed treatment of non-empty `artifacts_modified[]`. Do not silently rewrite that older proof to pretend it always understood v0.4 modification pairs.

A new shared helper or mixed-packet resolver may reuse the exact packet/context already grounded by Decision 011, then exact-load `artifacts_created[]` and packet `evidence_refs[]` directly through the existing Stage 2 immutable-reference language. The implementation must preserve all existing proof-to-use and exact-reference invariants rather than weakening `_load_exact_relation(...)`, the object store, or historical resolvers to make composition convenient.

If an implementation uses separately-produced component results, it must prove that their `packet_ref`, exact claim/base/occupancy/lane context, and authoritative exact refs agree before composing them. Logical-id equality is insufficient.

## No aggregate acceptance semantics

Decision 013 deliberately does **not** answer questions such as:

- whether every output must be individually `satisfied` before packet acceptance;
- whether one conflicting or `invalidated` evidence record defeats a satisfying record;
- whether missing evidence causes rejection, deferment, or repair;
- whether created and modified outputs have different acceptance policy;
- whether output ordering matters;
- whether one packet may partially integrate;
- whether a claim may close;
- whether a successor state may be published.

Those are later evidence-closure / packet-admission / integration semantics. This projection must preserve the facts needed to decide them later without deciding them now.

## Historical contract boundary

- Return-packet v0.3 non-empty `artifacts_modified[]` remains operationally unresolved and cannot enter mixed compatibility by resemblance or exact-looking strings.
- Return-packet v0.4 modifications enter only through Decision 011 and Decision 012.
- Existing created-output packets with no modifications keep their demonstrated behavior.
- No logical-id, newest/current, storage order, packet order, version, `supersedes_ref`, scheduler position, founder status, or Git permission becomes output-family or evidence authority.

## Lane 02 — smallest next implementation

Implement only a **read-only mixed created+modified compatibility projection**.

Required bounded behavior:

1. start from the exact packet and historical context already grounded by the canonical Stage 4 lifecycle / Decision 011 machinery;
2. exact-load created artifact refs and evidence refs without invoking the older `artifacts_modified[]` fail-closed assumption as if it were a v0.4 semantic rule;
3. preserve the current created-output subject-binding and compatibility semantics unchanged for each exact created artifact;
4. consume Decision 012 unchanged for each exact modification result;
5. prove exact context agreement before combining component results;
6. fail closed on created/result exact-ref category collision instead of choosing by order or deduplicating silently;
7. preserve all unmatched/conflicting evidence and component `satisfied` facts independently;
8. expose no packet-level acceptance/closure boolean;
9. preserve ADV-035 through ADV-045 and all canonical Decision 008–012 boundaries;
10. remain read-only and stop before evidence conflict precedence, source/dependency closure, lineage/supersession semantics, packet acceptance, claim closure, successor revision publication, Stage 5 integration, epochs, or replay.

A small shared exact-context / compatibility helper refactor is acceptable only when regression evidence shows that created-only and modified-only behavior remains unchanged.

## Lane 03 — adversarial surface

Attack the exact Lane 02 implementation for at least:

- a mixed packet where created and modified components accidentally reconstruct different historical lane/context authority;
- the same exact artifact ref classified as both created and modification result;
- same-logical/different-exact artifacts across the two families being collapsed together;
- evidence for a created artifact being pooled into a modification result, and vice versa;
- one exact evidence record being reassigned by artifact type, packet order, storage order, version, `supersedes_ref`, recency, actor, scheduler, founder, or Git permission;
- conflicting or `invalidated` exact evidence disappearing during composition;
- a false component result being silently converted into packet rejection or a true component result into packet acceptance;
- multiple `required_states` accidentally acquiring semantics through the mixed wrapper;
- historical v0.3 modified entries leaking into the mixed path;
- representation/materialization regressions against ADV-035 through ADV-045.

Do not expand the attack into source/dependency closure, lineage policy, packet acceptance, claim closure, successor publication, integration, epochs, or replay until repository state opens those gates.

## Root grounding

- **Truth:** two separately demonstrated compatibility surfaces are not relabelled as a packet-level acceptance result; composition exposes facts without inventing closure.
- **Agency / non-domination:** category, evidence, and lane standing come only from exact durable relations, never from actor identity, order, recency, confidence, founder status, or Git permission.
- **Continuity:** a replacement occupant must be able to reconstruct created and modified result compatibility from one exact packet and one exact historical context without hidden chat or current-state guesses.
- **Wisdom before speed:** close the concrete mixed-packet gap before opening evidence precedence, acceptance, immutable integration, epochs, or replay.
