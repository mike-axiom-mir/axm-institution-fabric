# CURRENT STATE OVERLAY — Decision 012 integrated; mixed packet compatibility opened

Status: **Decision 012 exact modified-result output/evidence compatibility is canonical on its demonstrated read-only surface, and ADV-045 reproduced no blocker after Lane 02's bounded representation repair.** PR #57 integrated the runtime/tests and PR #58 integrated Lane 03's evidence-only adversarial regressions. The next opened gate is Decision 013: a read-only mixed created+modified packet compatibility projection. Packet acceptance, evidence closure, lineage/supersession policy, source/dependency closure, claim closure, successor-state publication, Stage 5 integration receipts/runtime, epochs/barriers, and replay remain closed.

This file is the narrow current-state overlay on the older `coordination/CURRENT_WAVE.md` chronology. Earlier overlays, decisions, commits, PRs, failed runs, and specialist return packets remain repository history and are not silently rewritten by this summary.

## Canonical integration points

Decision 012 runtime/test integration:

`3d34cc043b99eccf8eb9c3db319dca431c6dcff4`

PR #57 — `Lane 02: modified-result output compatibility preflight` — merged.

ADV-045 regression integration:

`d4e9080d379236169225db322ec06d1b3b1c1b5b`

PR #58 — `Lane 03: adversarially verify modified-result compatibility` — retargeted from the stacked Lane 02 branch to canonical `main` after PR #57 merged, then merged without rewriting the specialist branch.

Decision 012:

`coordination/decisions/012_MODIFIED_RESULT_OUTPUT_COMPATIBILITY.md`

Decision 013:

`coordination/decisions/013_MIXED_PACKET_COMPATIBILITY_PROJECTION.md`

## What is now canonical

Within Decision 009's declared trusted deterministic runtime boundary, the bounded Stage 4 read-only path can reconstruct and verify:

1. exact packet -> claim -> claim-base -> lane / occupancy historical context;
2. exact packet-created artifact and packet evidence identities for the created-only surface;
3. exact evidence-to-created-artifact subject binding;
4. bounded created-output compatibility for one unambiguous required evidence state;
5. exact created-artifact work-base / producer-lane provenance;
6. return-packet v0.4 explicit `{prior_artifact_ref, result_artifact_ref}` modification relations while historical v0.3 modified entries remain opaque;
7. exact prior membership in the exact claim base and exact result identity/provenance against the same base/lane;
8. bounded modified-result compatibility for exactly one output declaration, one evidence requirement, and one currently-supported required evidence state;
9. exact evidence may satisfy a modification result only when `evidence.subject_ref` exactly equals that exact result ref;
10. prior evidence, same-logical decoys, version / `supersedes_ref`, later same-logical lane contracts, recency, storage order, and evidence array order gain no compatibility authority;
11. conflicting/additional exact result evidence remains explicit and `satisfied=True` remains narrower than evidence closure or packet acceptance.

Decision 012 does **not** prove logical lineage, valid supersession, source/dependency closure, evidence closure, packet acceptance, claim closure, successor publication, integration, epochs, or replay.

## Decision 012 evidence

### Preserved failed implementation evidence

Lane 02's first Decision 012 implementation head `fe7232957cbb1e7978fd6e8465067c071b3a1e0e` reached the new evaluator but exposed a real proof-to-use representation mismatch: its native run recorded 243 tests with 9 errors at `lane.outputs[] must expose a mapping`, and compile was skipped after the failing unittest gate.

That failure remains evidence. It was not relabelled flaky or erased.

### Lane 02 repaired baseline

Exact repaired implementation/workflow head:

`0d235f10766e4d8eed58ff73ef39f6fa1558cb56`

Final PR #57 head:

`dfa446056489d4ffde276935c95137bca5a18662`

The only change after the tested repaired head was the durable Lane 02 return packet:

`coordination/returns/02/2026-09-13_ACTIVATION_031.md`

GitHub Actions run/job inspected by Lane 01:

- run `34777655519`;
- job `103778601150`;
- exact head `0d235f10766e4d8eed58ff73ef39f6fa1558cb56`;
- deterministic unittest step: success;
- explicit compile step: success;
- complete job: success.

Lane 02's durable packet records **243/243 passed** plus explicit compile success, including all eleven Decision 012 tests and prior ADV-035 through ADV-044 regressions. Lane 01 independently confirmed exact head identity and successful test/compile job steps but did not retrieve raw stdout, so the numeric count remains attributed to specialist evidence.

The repair preserved the exact `lane_ref` already grounded by Decision 011 and loaded that same exact immutable ref through `FilesystemObjectStore.load(...)` for the ordinary mapping representation expected by the compatibility evaluator. It did not add logical-id/current/newest fallback authority.

### Lane 03 / ADV-045

Exact tested adversarial head:

`55ec072591c007c43573c3f9bd77e598ebde4fcd`

Final PR #58 head:

`fc361e4466cf2115d67abb14b2d6dedf5e2ffc2e`

The only change after that tested head was the durable Lane 03 return packet:

`coordination/returns/03/2026-09-13_ACTIVATION_033.md`

GitHub Actions run/job inspected by Lane 01:

- run `34777866613`;
- job `103779182656`;
- exact head `55ec072591c007c43573c3f9bd77e598ebde4fcd`;
- deterministic unittest step: success;
- explicit compile step: success;
- complete job: success.

Lane 03's durable packet records **248/248 passed** plus explicit compile success. ADV-045-A/B/C/D/E preserve that evidence order does not choose standing, later same-logical/high-version/superseding decoys gain no authority, `supersedes_ref` cannot launder prior evidence into result evidence, passing prior evidence cannot mask invalidated exact-result evidence, and a later same-logical lane contract cannot replace the exact claim-base contract. Lane 01 independently confirmed exact head identity and successful test/compile job steps but did not retrieve raw stdout, so the numeric count remains attributed to specialist evidence.

No post-merge-main Actions run is asserted for merge commits `3d34cc043...` or `d4e9080d...` unless a later activation observes one.

## Decision 013 — next composition gap

Created-output and modified-result compatibility are now individually grounded, but a packet containing **both** output families still lacks one truthful read-only projection.

The older created-output path intentionally consumes a resolver that fails closed whenever `artifacts_modified[]` is non-empty. Decision 011/012, meanwhile, understands v0.4 modifications but does not expose created-output compatibility. Treating modification results as created artifacts would erase the explicit prior/result relation, while independently reconstructing context could let the two paths disagree about authoritative lane or evidence state.

Decision 013 therefore opens only this chronology:

```text
one exact packet P
  -> one exact claim / base / occupancy / historical lane context

created outputs
  -> exact artifacts_created[] refs
  -> existing exact subject binding
  -> existing narrow created-output compatibility

modified outputs
  -> Decision 011 exact prior/result pairs
  -> Decision 012 narrow result compatibility

mixed projection
  -> prove both families use the same exact historical context
  -> preserve per-output compatibility and unmatched/conflicting evidence
  -> no aggregate packet acceptance/closure boolean
```

If the same exact artifact ref is classified simultaneously as a created artifact and a modification result, the mixed projection must fail closed rather than silently pick or deduplicate a category. This is a composition ambiguity only; Decision 013 does not declare the packet globally invalid.

## Lane 02 — smallest next implementation

Implement only Decision 013's **read-only mixed created+modified compatibility projection**.

Required bounded behavior:

1. use one exact packet and grounded historical claim/base/occupancy/lane context;
2. exact-load created refs and evidence refs through the existing Stage 2 exact-reference language without weakening the older resolver's historical proof boundary;
3. preserve existing created-output subject-binding and one-state compatibility semantics unchanged;
4. consume Decision 012 unchanged for exact modification results;
5. prove exact context agreement before composing component results;
6. fail closed on exact-ref collision between created and modified-result categories rather than using array order, logical id, type, version, recency, or `supersedes_ref`;
7. preserve unmatched, conflicting, and invalidated evidence explicitly;
8. expose per-output facts only — no packet-level `accepted`, `closed`, `complete`, or aggregate `satisfied` boolean;
9. preserve ADV-035 through ADV-045 and historical v0.3 non-reinterpretation;
10. stop before conflict precedence, evidence/source/dependency closure, lineage/supersession policy, packet acceptance, claim closure, successor publication, integration, epochs, or replay.

A small shared exact-context / compatibility helper refactor is acceptable only if tests prove created-only and modified-only behavior remain unchanged.

## Lane 03 — next adversarial pass

Attack only the exact Lane 02 Decision 013 head:

- created and modified components reconstructing different exact lane/context authority;
- the same exact artifact classified as both created and modification result;
- same-logical/different-exact outputs across families being collapsed;
- created evidence pooled into modified results or modified-result evidence pooled into created outputs;
- evidence/category selection by array order, storage order, recency, version, `supersedes_ref`, actor, scheduler, founder, or Git authority;
- conflicting / `invalidated` evidence disappearing during composition;
- component compatibility accidentally becoming packet acceptance/rejection;
- multiple `required_states` gaining semantics through the wrapper;
- historical v0.3 modified entries leaking into the mixed path;
- all ADV-035 through ADV-045 regressions staying green.

Do not expand into source/dependency closure, lineage policy, packet acceptance, claim closure, successor publication, integration, epochs, or replay.

## Root grounding

- **Truth:** Decision 012 is integrated only for the exact surface actually tested; two component compatibility surfaces are not relabelled as acceptance.
- **Agency / non-domination:** exact durable relations, not actor identity, order, recency, confidence, founder status, or Git permission, determine context and evidence standing.
- **Continuity:** a replacement occupant can reconstruct the demonstrated modified-result decision today; Decision 013 requires a mixed packet to become equally reconstructable from one exact historical context.
- **Wisdom before speed:** close the concrete composition gap before evidence precedence, packet acceptance, immutable integration, epochs, or replay.

## Still unresolved

Multiple `required_states` semantics, evidence method/source quality and closure, conflicting/invalidation evidence precedence, `artifact.source_refs[]` and `dependency_refs[]` exactness/closure, modified-artifact logical lineage and `supersedes_ref` semantics, occupancy/claim global currentness/supersession/authorization, multiple-packet conflict semantics, broader historical schema reconstruction, durable closure, packet acceptance, claim closure, successor revision publication, integration receipts/runtime, epochs/barriers, replay, cross-language reproduction, stronger filesystem durability/concurrency evidence, and hostile same-process code isolation remain explicit obligations.
