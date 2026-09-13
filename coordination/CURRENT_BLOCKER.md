# CURRENT STATE OVERLAY — Stage 4 created-output compatibility integrated

Status: **no active blocker on the bounded created-output compatibility preflight**. PR #49 is canonical, and Lane 03 ADV-042 regression evidence is canonical through PR #50. The next opened gate is the exact provenance base of packet-created artifacts. This file is the narrow current-state overlay on the older `coordination/CURRENT_WAVE.md` chronology.

## Canonical integration points

Created-output compatibility runtime:

`29424cf493f1b144ad5b001f60e065baf4ab434e`

PR #49 — `Lane 02: bounded created-output compatibility preflight` — merged.

ADV-042 evidence/regressions:

`09feea00446a724d44d239680902f6742afb680b`

PR #50 — `Lane 03: adversarially verify created-output compatibility` — merged after retargeting from the stacked Lane 02 branch to canonical `main` without rewriting specialist history.

Decision 010:

`coordination/decisions/010_CREATED_ARTIFACT_PROVENANCE_BASE.md`

canonical commit:

`6b7c2a4ebc4f5b2790c116a64f615ac4131a84b1`

## What is now canonical

The bounded Stage 4 runtime can now, within Decision 009's declared trusted deterministic runtime boundary:

1. reconstruct the exact packet -> claim -> claim-base -> lane relation from durable state;
2. separately reconstruct the exact claim -> occupancy -> occupancy-entry-base -> lane relation;
3. consume the canonical exact created-artifact/evidence subject-binding result;
4. require each packet-created artifact type to match exactly one declared output in the exact claim-base lane contract;
5. require that output type to match exactly one lane evidence-requirement entry;
6. support only exactly one `required_states` value;
7. mark the bounded requirement satisfied only from exact subject-bound evidence whose `state` exactly equals that one required state;
8. fail closed on missing or duplicate output declarations, missing or duplicate evidence requirements, and multiple required states;
9. preserve unmatched/conflicting evidence explicitly rather than turning `satisfied=True` into evidence closure;
10. keep `artifacts_modified[]` fail-closed.

This remains read-only compatibility groundwork. `satisfied=True` is **not** packet acceptance, evidence closure, claim closure, successor-state publication, integration, or replay.

## Evidence

Lane 02 exact tested implementation/workflow head:

`4334c18bfef36e646e71ba724934a4a8cde6976e`

Its native current-main merge-candidate run directly recorded:

- **199 tests / 199 passed**;
- 0 failures / 0 errors;
- all 10 new compatibility regressions green;
- existing exact evidence-subject and ADV-035 through ADV-040 regressions green;
- explicit production/test compile success.

Lane 03 exact adversarial implementation/test head:

`f6342e45f2760c77c25bf46faea42285e46c9b4b`

Its native stacked merge-candidate run directly recorded:

- **203 tests / 203 passed**;
- 0 failures / 0 errors;
- ADV-042-A/B/C/D green;
- Lane 02 compatibility regressions green;
- evidence-subject and ADV-035 through ADV-040 regressions green;
- explicit compile success.

ADV-042 established only the demonstrated bounded surface:

- exact claim-base lane policy survives a different historical occupancy-entry version of the same logical lane;
- a same-logical-id/different-exact artifact cannot borrow evidence from the authoritative packet-created artifact;
- same-type created artifacts do not share an evidence pool;
- conflicting exact subject-bound evidence remains explicit even when the one required state is present.

No post-merge Actions result is asserted here unless separately recorded by GitHub. The integration decision rests on exact specialist/native evidence, mergeable Git history, and the fact that PR #50 adds regression/evidence coverage rather than production policy.

## Decision 010 — next continuity gap

Created-output compatibility does not yet make artifact provenance exact.

Current `artifact.schema.json` v0.1 still permits:

```text
provenance.base_state_revision: <any non-empty string>
```

while packet/claim lifecycle state now uses exact immutable state-revision refs.

Therefore:

```text
exact packet/claim/lane compatibility
    != exact created-artifact provenance
```

For a packet-created artifact whose provenance is later used for acceptance, successor publication, or replay, Decision 010 requires the work-base relation to be exact and reproducible:

```text
exact packet P
  -> exact claim C
  -> exact claim base B
  -> exact claim lane L

exact created artifact A named by P
  -> provenance producer lane == L.id
  -> provenance base == exact immutable B
```

The current generic provenance string must not be silently interpreted through logical id, newest version, storage recency, mutable current state, array order, or private actor memory.

## Lane 02 — smallest next implementation

Implement only the **packet-created artifact exact-provenance-base precondition**.

Required bounded behavior:

1. preserve canonical compatibility behavior and ADV-035 through ADV-042;
2. make the created artifact provenance base represent one canonical exact immutable `state-revision` ref, with explicit schema-version/migration behavior rather than silently reinterpreting historical v0.1 strings;
3. reuse the shared Stage 2 immutable-reference parser and require kind `state-revision`;
4. exact-load and identity-verify the provenance base before operational use;
5. require that exact provenance base to equal the exact claim base reconstructed for the packet;
6. require `provenance.producer_lane_id` to equal the exact claim-base lane logical id;
7. fail closed on non-exact, wrong-kind, missing, corrupt, or different-base provenance;
8. remain read-only beyond the necessary schema/fixture migration and keep `artifacts_modified[]` fail-closed;
9. do not open source/dependency closure, evidence conflict policy, packet acceptance, claim closure, successor publication, integration, epochs, or replay.

If an exact schema migration cannot preserve historical meaning without ambiguity, stop with a migration blocker/return packet instead of inventing compatibility.

## Lane 03 — next adversarial pass

After Lane 02 leaves an exact tested head, attack only that provenance precondition:

- same logical revision id / different exact state-revision ref substitution;
- wrong-kind exact provenance ref;
- exact but different/stale work base;
- producer-lane mismatch;
- missing/corrupt exact provenance target;
- historical v0.1 artifact accidentally treated as exact without an explicit migration rule;
- newest/current/storage-order/actor/schedule authority entering resolution;
- all created-output compatibility and ADV-035 through ADV-042 regressions remaining green.

Do not expand into modified-artifact semantics, source/dependency closure, packet acceptance, or Stage 5.

## Root grounding

- **Truth:** bounded compatibility is integrated only on the exact claims demonstrated; conflicting evidence remains explicit; generic artifact provenance is not relabelled exact.
- **Agency / non-domination:** actor identity, scheduler position, founder status, recency, logical-id equivalence, or Git authority cannot select the provenance base.
- **Continuity:** a replacement occupant must be able to reconstruct the artifact's exact work base and producer lane from durable state without private chat memory.
- **Wisdom before speed:** advance one provenance precondition before acceptance/replay, while modified artifacts, source/dependency closure, evidence conflict semantics, and later lifecycle stages remain closed.

## Still unresolved

Multiple `required_states` semantics, evidence method/source quality and closure, conflicting/invalidation evidence policy, artifact `source_refs[]` and `dependency_refs[]` exactness/closure, modified-artifact prior/result identity (`ADV-002-I`), occupancy/claim global currentness/supersession/authorization, multiple-packet conflict semantics, historical schema reconstruction beyond the bounded migration needed here, durable closure, claim closure, successor revision publication, integration receipts/runtime, epochs/barriers, replay, cross-language reproduction, stronger filesystem durability/concurrency evidence, and hostile same-process code isolation remain explicit obligations.
