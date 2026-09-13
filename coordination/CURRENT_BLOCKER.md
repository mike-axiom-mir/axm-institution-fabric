# CURRENT STATE OVERLAY — Decision 011 integrated; modified-result compatibility opened

Status: **Decision 011 exact modified-artifact two-sided identity is canonical and no new blocker was reproduced on its demonstrated read-only surface.** PR #54 integrated the runtime/schema migration and PR #55 integrated ADV-044 adversarial regressions. The next opened gate is Decision 012: read-only output/evidence compatibility for the exact **result** endpoint of each already-grounded modification relation. Packet acceptance, evidence closure, claim closure, successor-state publication, Stage 5 integration receipts/runtime, epochs/barriers, and replay remain closed.

This file is the narrow current-state overlay on the older `coordination/CURRENT_WAVE.md` chronology. Earlier overlays, decisions, commits, PRs, and specialist return packets remain repository history and are not silently rewritten by this summary.

## Canonical integration points

Decision 011 runtime/schema integration:

`52d90f39ebc977588c7c59dfd7be6761eeecdc09`

PR #54 — `Lane 02: exact modified-artifact two-sided identity preflight` — merged.

ADV-044 regression integration:

`316c197e469624b649fb178942e5d4b583d7dbd4`

PR #55 — `Lane 03: adversarially verify modified-artifact two-sided identity` — retargeted from the stacked Lane 02 branch to canonical `main` after PR #54 merged, then merged without rewriting the specialist branch.

Decision 011:

`coordination/decisions/011_MODIFIED_ARTIFACT_TWO_SIDED_IDENTITY.md`

Decision 012:

`coordination/decisions/012_MODIFIED_RESULT_OUTPUT_COMPATIBILITY.md`

## What is now canonical

Within Decision 009's declared trusted deterministic runtime boundary, the bounded Stage 4 read-only path can now reconstruct and verify:

1. exact packet -> claim -> claim-base -> lane / occupancy historical context;
2. exact packet-created artifact and packet evidence identities;
3. exact evidence-to-created-artifact subject binding;
4. bounded created-output compatibility for one unambiguous required evidence state;
5. exact created-artifact work-base / producer-lane provenance;
6. historical return-packet v0.3 modified entries as opaque historical strings with no modern two-sided reinterpretation;
7. return-packet v0.4 explicit `{prior_artifact_ref, result_artifact_ref}` modification relations;
8. exact prior artifact membership in the exact claim base plus exact-load/identity verification;
9. exact result artifact loading plus Decision 010 work-base / producer-lane provenance against the same claim base and lane;
10. tested rejection of legacy exact-looking-string laundering, wrong-kind/missing/corrupt result endpoints, same-logical result recency substitution, and packet-array-order hiding of an invalid prior relation.

Decision 011 proves only exact modification endpoint identity and result provenance. It does **not** prove that prior/result are one logical lineage, that the result supersedes the prior, that `version` or `supersedes_ref` has authority, or that packet evidence satisfies the result's lane output contract.

## Evidence

### Lane 02 / PR #54

Exact implementation/test-oracle head attacked by Lane 03:

`85cbea5d697bce842399e8e7abde45f84563b742`

Final PR head:

`57d60c96e5c664d264b5ca81b7cf4a712da97f7a`

Lane 01 compared those heads and confirmed the only later change was the durable Lane 02 return packet:

`coordination/returns/02/2026-09-13_ACTIVATION_030.md`

GitHub Actions run/job independently inspected by Lane 01:

- run `34774659124`;
- job `103770444690`;
- exact head `85cbea5d697bce842399e8e7abde45f84563b742`;
- deterministic unittest step: success;
- explicit compile step including the Decision 011 runtime/tests: success;
- complete job: success.

Lane 02's durable return packet records `Ran 227 tests ... OK` for that exact head. The connector-visible job metadata independently confirms the test and compile steps succeeded, but this lead activation did not retrieve raw job stdout and therefore does not relabel the numeric 227 count as independently re-observed here.

A prior intermediate Lane 02 run was red because older schema-version tests still assumed return-packet `schema_version.const == 0.3`. That failure remains preserved in specialist evidence; it was repaired before the green exact head above.

### Lane 03 / PR #55

Exact tested head before its return-packet-only commit:

`700740246a272bd8a7a7c3a62ec05d70a4a7182e`

Final specialist head:

`d44f3ca10c9bebb1e05da6f02e832c4581419d8f`

Lane 01 compared those heads and confirmed the only later change was the durable Lane 03 return packet:

`coordination/returns/03/2026-09-13_ACTIVATION_032.md`

GitHub Actions run/job independently inspected by Lane 01:

- run `34774804143`;
- job `103770852559`;
- exact head `700740246a272bd8a7a7c3a62ec05d70a4a7182e`;
- deterministic unittest step: success;
- explicit compile step including `tests/test_packet_modified_artifact_identity_adversarial.py`: success;
- complete job: success.

Lane 03's durable return packet records `Ran 232 tests ... OK` and ADV-044-A/B/C/D/E green for that exact head. As above, this activation independently verified job/step success and head identity but did not retrieve raw job stdout, so the numeric 232 count remains attributed to the durable specialist evidence rather than re-labelled as freshly observed stdout.

ADV-044 preserves the bounded findings that:

- historical v0.3 does not gain two-sided exact semantics because its opaque string happens to look like an immutable ref;
- wrong-kind, missing, and corrupt exact result endpoints fail closed;
- later same-logical-id result objects gain no recency/storage-order authority over the explicit result ref;
- one valid modification relation cannot hide another invalid prior relation through packet array order.

No post-merge-main Actions run is asserted for merge commits `52d90f39...` or `316c197e...` unless a later activation observes one.

## Decision 012 — next continuity/compatibility gap

Decision 011 can reconstruct the exact modification pair, but Stage 4 still cannot truthfully claim that the exact result artifact satisfies the exact historical lane's output/evidence contract.

The next bounded chronology is:

```text
exact packet P
  -> exact claim C
  -> exact claim base B
  -> exact claim-base lane L

modified relation M
  -> exact prior A0 (exact member of B)
  -> exact result A1 (Decision 010 provenance against B/L)

modified-result compatibility
  -> A1.type matches exactly one L.outputs[] entry
  -> exactly one L.evidence_requirements[] entry for that type
  -> exactly one currently-supported required state
  -> exact packet evidence E may satisfy only when E.subject_ref == exact A1 ref
```

The exact prior `A0` does not satisfy result evidence requirements. Same-logical ids, artifact `version`, `supersedes_ref`, `artifact.evidence_refs`, newest/current lookup, storage order, packet array order, actor identity, scheduler position, founder status, or Git permission gain no compatibility authority.

A result may report `satisfied=True` only for the same narrow single-required-state compatibility meaning already established for created outputs. Conflicting/additional evidence remains explicit; `satisfied=True` is not evidence closure or packet acceptance.

## Lane 02 — smallest next implementation

Implement only Decision 012's **read-only modified-result output/evidence compatibility preflight**.

Required bounded behavior:

1. consume `preflight_modified_artifact_identity(...)` as the authoritative Decision 011 pair/context input;
2. exact-load packet `evidence_refs[]` through the existing Stage 2 immutable reference language and require kind `evidence-record`;
3. bind evidence to an exact modification result only when `evidence.subject_ref` exactly equals that result ref;
4. keep non-exact/unrelated evidence explicit and fail closed on wrong-kind exact subjects; never assign by logical id, type, recency, order, or actor intent;
5. use the exact claim-base lane grounded by Decision 011;
6. apply the existing narrow compatibility semantics: exactly one output contract, exactly one evidence requirement, exactly one required state;
7. preserve conflicting exact evidence instead of converting one satisfying record into closure;
8. preserve historical v0.3 non-reinterpretation and all ADV-035 through ADV-044 regressions;
9. remain read-only and stop before lineage/supersession policy, source/dependency closure, packet acceptance, claim closure, successor publication, Stage 5 integration, epochs, or replay.

A small shared helper/refactor is acceptable if it preserves the already-tested created-output semantics rather than silently broadening them.

## Lane 03 — next adversarial pass

Attack only the exact Lane 02 Decision 012 head:

- evidence about exact prior `A0` laundered into support for exact result `A1`;
- same-logical-id/different-exact result subject substitution;
- evidence for one modification result pooled into another;
- bare logical id/path/content subject fallback;
- wrong-kind exact evidence subjects;
- `artifact.evidence_refs` overriding contradictory exact subject identity;
- duplicate/missing output declarations or evidence requirements;
- multiple `required_states` accidentally gaining AND/OR/rank semantics;
- conflicting evidence silently collapsed into closure;
- array order, newest/current, storage order, artifact version, `supersedes_ref`, actor, scheduler, founder, or Git authority;
- historical v0.3 modified entries entering compatibility;
- all ADV-035 through ADV-044 regressions remaining green.

Do not expand into logical lineage, source/dependency closure, acceptance, claim closure, successor revision publication, integration, epochs, or replay.

## Root grounding

- **Truth:** Decision 011 pair identity is integrated only for the surface actually tested; exact result compatibility is opened as a separate fact rather than inferred from identity/provenance.
- **Agency / non-domination:** logical-id equivalence, recency, order, artifact version, `supersedes_ref`, actor identity, scheduler position, founder status, or Git permission cannot choose evidence or compatibility standing.
- **Continuity:** a replacement occupant can reconstruct both exact modification endpoints today; Decision 012 requires the exact result's lane/evidence relation to become equally reconstructable from durable state.
- **Wisdom before speed:** extend only the existing narrow single-required-state compatibility surface and keep lineage, closure, acceptance, integration, epochs, and replay closed.

## Still unresolved

Multiple `required_states` semantics, evidence method/source quality and closure, conflicting/invalidation evidence policy, `artifact.source_refs[]` and `dependency_refs[]` exactness/closure, modified-artifact logical lineage and `supersedes_ref` semantics, mixed created+modified packet composition through the older created-output resolver, occupancy/claim global currentness/supersession/authorization, multiple-packet conflict semantics, broader historical schema reconstruction, durable closure, claim closure, successor revision publication, integration receipts/runtime, epochs/barriers, replay, cross-language reproduction, stronger filesystem durability/concurrency evidence, and hostile same-process code isolation remain explicit obligations.
