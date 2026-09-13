# CURRENT STATE OVERLAY — Stage 4 exact created-artifact provenance integrated

Status: **no active blocker on Decision 010's bounded packet-created artifact provenance-base precondition**. PR #51 is canonical and Lane 03 ADV-043 regression evidence is canonical through PR #52. The next opened gate is Decision 011: two-sided exact identity for `artifacts_modified[]`. Claim closure, successor-state publication, Stage 5 integration receipts/runtime, epochs/barriers, and replay remain closed.

This file is the narrow current-state overlay on the older `coordination/CURRENT_WAVE.md` chronology.

## Canonical integration points

Created-artifact exact provenance runtime:

`3ced7ee1bb88d7744923fb2cb968af8b3cdb45f9`

PR #51 — `Lane 02: exact created-artifact provenance base preflight` — merged.

ADV-043 evidence/regressions:

`daa36e15456c6ae5879f9884f4093f0ae188462c`

PR #52 — `Lane 03: adversarially verify created-artifact provenance` — retargeted from the stacked Lane 02 branch to canonical `main` after PR #51 merged, then merged without rewriting the specialist branch.

Decision 010:

`coordination/decisions/010_CREATED_ARTIFACT_PROVENANCE_BASE.md`

Decision 011:

`coordination/decisions/011_MODIFIED_ARTIFACT_TWO_SIDED_IDENTITY.md`

canonical Decision 011 commit:

`bf91e735a1fb0dc464974071531b5985cc7fafc4`

A separate public-checkpoint workflow commit (`281df25bc90f335a80680375b2864931e5b91a46`) landed on `main` between the prior lead activation and these integrations. It adds only release-workflow state and explicitly describes the checkpoint as a prerelease/research scaffold rather than production or CANON completion. It does not alter the deterministic kernel contracts or runtime used by Decision 010.

## What is now canonical

Within Decision 009's declared trusted deterministic runtime boundary, the bounded Stage 4 read-only path can now:

1. reconstruct the exact packet -> claim -> claim-base -> lane relation from durable state;
2. reconstruct exact packet-created artifact and evidence identities;
3. bind exact evidence records only to the exact created artifacts they name;
4. apply the bounded created-output compatibility preflight for one unambiguous required evidence state;
5. preserve conflicting/unmatched evidence explicitly rather than treating compatibility success as evidence closure;
6. require a packet-created artifact used by the provenance preflight to use artifact schema v0.2 exact work-base semantics;
7. parse `provenance.base_state_revision_ref` through the shared Stage 2 immutable-reference parser and require kind `state-revision`;
8. exact-load and identity-verify that provenance base;
9. require it to equal the packet's exact claim base;
10. require `provenance.producer_lane_id` to equal the exact claim-base lane logical id;
11. reject historical artifact v0.1 as insufficient for this exact provenance use rather than silently reinterpret its generic `base_state_revision` string;
12. keep `artifacts_modified[]` fail-closed because its current one-string contract still cannot represent both exact prior and exact result identity.

This is still pre-acceptance groundwork. A successful provenance preflight is **not** packet acceptance, evidence closure, dependency/source closure, claim closure, successor-state publication, integration, or replay.

## Evidence

### Lane 02 / PR #51

Exact final PR head:

`2508279a607d47a61cf1da3dbe40ac8a1203601d`

GitHub PR merge-candidate workflow run inspected by Lane 01:

- run `34771329874`;
- job `103761355190`;
- deterministic unittest discovery: **212 tests / 212 passed**;
- 0 failures / 0 errors;
- explicit compile step including the Decision 010 runtime/tests: **success**.

Lane 02's return packet separately records its exact implementation/workflow head `e07e1a311db51d205af1b51f46f5793131421a59` and native evidence. The final branch head adds only the durable Lane 02 return packet beyond the tested implementation head.

The later public-checkpoint workflow commit was disjoint from the kernel change. No post-merge Actions run for merge commit `3ced7ee1...` is asserted here.

### Lane 03 / PR #52

Exact final specialist head:

`d008442a3fa97504534d239123c2a8026533368e`

Native stacked merge-candidate run directly inspected by Lane 01:

- run `34771942649`;
- job `103763008908`;
- **217 tests / 217 passed**;
- ADV-043-A/B/C/D/E all green;
- explicit compile including `tests/test_packet_artifact_provenance_adversarial.py`: **success**.

ADV-043 demonstrated on the bounded surface that:

- a structural exact-lookalike/noncanonical ref cannot bypass the Stage 2 parser;
- corrupt exact provenance targets fail closed during exact-load/identity verification;
- an exact historical ancestor cannot substitute for the exact claim base;
- packet array order cannot hide one stale created artifact among valid ones;
- same-logical-id revisions stored before/after the authoritative base gain no recency/storage-order authority.

That 217-test run was on the specialist's stacked provenance candidate before Lane 01 retargeted PR #52 to canonical `main`. PR #52 changes only workflow compile coverage, ADV-043 tests, and its durable Lane 03 return packet; it does not alter production runtime. No post-merge Actions result for `daa36e15...` is asserted here.

## Decision 011 — next continuity gap

The current return-packet schema v0.3 still represents:

```text
artifacts_modified[] -> one opaque string per entry
```

while the canonical output-identity runtime correctly fails closed because a modification requires two identities:

```text
exact prior artifact observed by the work
exact produced artifact result
```

One opaque value cannot establish both without hidden interpretation. State revisions already bind exact `artifact_refs`, and Decision 010 can ground an exact post-base result's claim-base provenance, so the smallest next repair is now explicit two-sided modification identity.

Decision 011 opens only this bounded chronology for v0:

```text
exact packet P
  -> exact claim C
  -> exact claim base B

modified relation M
  -> exact prior artifact A0
     -> A0 is an exact artifact member of B
  -> exact result artifact A1
     -> A1 exact-loads
     -> A1 satisfies Decision 010 against B and the exact claim-base lane
```

No logical-id equivalence, newest/current object, artifact version, `supersedes_ref`, storage order, packet array order, actor identity, scheduler position, founder status, or Git permission may manufacture the pair.

Historical return-packet v0.3 one-string entries remain historical truth and must not be silently reinterpreted as two exact refs.

## Lane 02 — smallest next implementation

Implement only Decision 011's **read-only modified-artifact two-sided identity precondition**.

Required bounded behavior:

1. preserve historical return-packet v0.3 meaning without reinterpretation;
2. add an explicit newer packet contract only if old/new behavior remains unambiguous;
3. represent each operational modification with one exact prior artifact ref and one exact result artifact ref;
4. parse both through the shared Stage 2 immutable-ref parser and require kind `artifact`;
5. reconstruct the exact claim base through the existing packet lifecycle path;
6. require the exact prior artifact to be an exact member of that base revision and exact-load/identity-verify it;
7. exact-load the result artifact and apply Decision 010's exact work-base / producer-lane checks;
8. preserve all created-output/evidence/provenance and ADV-035 through ADV-043 regressions;
9. remain read-only and stop before same-logical-id lineage rules, `supersedes_ref` authority, evidence closure, packet acceptance, claim closure, successor publication, integration, epochs, or replay.

If the schema migration cannot preserve historical meaning without ambiguous old/new authority, stop with an explicit migration blocker rather than guessing.

## Lane 03 — next adversarial pass

Attack only the exact Lane 02 Decision 011 head:

- same-logical-id/different-exact prior substitution;
- exact prior artifact not present in the exact claim base;
- same-logical-id/different-exact result substitution;
- result provenance bound to another exact revision or producer lane;
- wrong-kind/noncanonical refs on either side;
- missing/corrupt prior or result;
- array-order, newest/current, storage-order, actor, schedule, founder, or Git authority;
- historical v0.3 one-string modifications accidentally acquiring new exact meaning;
- `supersedes_ref`, version, or logical id silently overriding the explicit pair;
- all ADV-035 through ADV-043 regressions remaining green.

Do not expand into lineage policy, evidence conflict/closure, packet acceptance, successor-state publication, Stage 5 integration, epochs, or replay.

## Root grounding

- **Truth:** Decision 010 is integrated only for the exact surface tested; one opaque modification value is not relabelled as two immutable identities.
- **Agency / non-domination:** actor identity, recency, scheduler position, founder status, logical-id equivalence, array/storage order, or Git permission cannot select provenance or modification endpoints.
- **Continuity:** a replacement occupant can reconstruct the created output's exact work base now, and Decision 011 requires the same reconstructability for both sides of a modification.
- **Wisdom before speed:** open one missing identity precondition while keeping lineage, closure, acceptance, integration, epochs, and replay closed.

## Still unresolved

Multiple `required_states` semantics, evidence method/source quality and closure, conflicting/invalidation evidence policy, artifact `source_refs[]` and `dependency_refs[]` exactness/closure, modified-artifact logical lineage and `supersedes_ref` semantics beyond Decision 011's pair identity, occupancy/claim global currentness/supersession/authorization, multiple-packet conflict semantics, broader historical schema reconstruction, durable closure, claim closure, successor revision publication, integration receipts/runtime, epochs/barriers, replay, cross-language reproduction, stronger filesystem durability/concurrency evidence, and hostile same-process code isolation remain explicit obligations.
