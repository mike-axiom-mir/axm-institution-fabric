# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Canonical `main` reviewed before this Lane 01 branch: **through PR #89 / `4bcfa5fe82d2d50fb043dd3d9dd6efcf854b3c34`**
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current bounded gate: **Decision 020 — Typed Source Declaration Contract**
Current disposition: **HOLD. Lane 02's Decision 020 implementation has strong native baseline evidence, but Lane 03 ADV-054-A reproduced one narrow declaration-key true-end continuity failure. Do not integrate PR #90 until Lane 02 repairs only that boundary and Lane 03 reruns ADV-054 unchanged. Resolver/loading, integrity execution, declaration association, migration mapping, trust, closure, packet acceptance, Stage 5 integration, epochs, and replay remain closed.**

`coordination/CURRENT_WAVE.md` is historical chronology. This file is the current-state overlay and must be read with Decision 020, Decision 019 research, newest commits/PRs/branches, and durable Lane 01/02/03 return packets.

## Canonical kernel boundary before Decision 020

The deterministic Python v0 kernel canonically demonstrates the previously grounded exact identity, immutable store, exact revision membership, lifecycle relationship grounding, bounded occupancy/work-claim/return-packet admission, exact output/evidence identity, exact evidence subject binding, created/modified/mixed output compatibility facts, artifact provenance-base facts, two-sided modification identity, exact dependency identity/context membership, packet-local dependency graph/reachability, Decision 018 reachable dependency-frontier facts, and historical source-ref non-reinterpretation evidence.

Decision 018 remains factual only. Decision 019 established the four source target classes while keeping historical source strings opaque. Neither decision establishes source resolution, trust, closure, acceptance, integration, epochs, or replay.

## Decision 020 implementation evidence — PR #90

Lane 02 PR #90 implements only the versioned typed source-declaration contract on canonical base:

`4bcfa5fe82d2d50fb043dd3d9dd6efcf854b3c34`

Exact test-bearing implementation/workflow head:

`d67fdbcd038b78bf02c8e0d6e1a925183f969f97`

Exact native PR merge candidate:

`dc2c9460f2824be64c2b50d280b57e3c8ea91db2`

Native Actions run `34809276128`, job `103867160232`, Python 3.12.14 directly recorded:

- **410 / 410 tests passed** in 619.485s;
- explicit compile succeeded;
- complete job succeeded.

Lane 02 final branch head `2ac36baedf1dbb4fe46375962c2f19f1adc8ce2e` adds only its durable Activation 041 return packet after the tested head.

The candidate adds:

- one shared four-class typed source declaration contract;
- artifact v0.4 typed `provenance.source_declarations`;
- evidence-record v0.2 typed `source_declarations`;
- declaration occurrence identity as exact containing object identity plus declaration key;
- explicit `opaque_label`, `exact_axm_object`, `content_address`, and `locator` classes;
- Stage 2 canonical immutable-ref parsing for `exact_axm_object` without target loading;
- SHA-256/lowercase-64/`raw_bytes` as the only first content-address form;
- locator context/value as authored facts only;
- historical artifact v0.1/v0.2/v0.3 and evidence v0.1 source semantics unchanged;
- no dual legacy/new source authority in typed versions.

The 410/410 result remains valid evidence for that pre-ADV-054 tested surface. Green CI and mergeability are evidence/execution facts only; they are not canonical authority.

## ADV-054 hold — PR #91

Lane 03 PR #91 independently attacked the exact Decision 020 implementation surface and is intentionally stacked on Lane 02.

Exact adversarial test-bearing head:

`a60b710269022618badfa94368e7bdcb43c26c43`

Exact native PR merge candidate:

`2d389292928dd85adda0f1926d7daf14058a550e`

Native Actions run `34810251086`, job `103869985728`, Python 3.12.14 ran the focused ADV-054 suite first:

- 5 adversarial test methods ran;
- ADV-054-B/C/D/E passed;
- **ADV-054-A failed** for both artifact v0.4 and evidence-record v0.2;
- both failures were `ContractValidationError not raised`;
- full repository suite and explicit compile were skipped after the focused failure;
- therefore Lane 03 makes no new full-suite or compile claim.

### Exact reproduced counterexample

Decision 020 describes declaration ids with the stable spelling language:

```text
^[a-z0-9][a-z0-9._-]*$
```

The current typed artifact/evidence schemas use that expression as JSON-Schema `propertyNames.pattern`. On the demonstrated Python/jsonschema path, `$` accepts a final LF, so this authored key is currently accepted:

```text
"source\n"
```

The repository already has canonical ADV-028 history showing the same `$` false-end producer/parser continuity class and previously repaired it with true-end semantics on identity-bearing boundaries.

This is a narrow contract spelling failure. It does **not** reopen the four-class source taxonomy and is not evidence that resolver, integrity, association, migration, trust, closure, acceptance, or integration semantics should be added.

### ADV-054 findings that held

- duplicate raw JSON declaration keys fail closed through strict parsing;
- ordinary JSON materialization/copy preserves tested declaration key-to-target meaning;
- the same declaration key reused across different exact containing objects remains occurrence-local;
- neighboring exact-looking `content_ref` values do not manufacture source declaration authority.

## Active lane boundaries

### Lane 01 — sequencing / integration

Hold Decision 020 integration while ADV-054-A is reproducible. Do not duplicate Lane 02's implementation repair and do not merge either stacked PR merely because it is mergeable.

After Lane 02 publishes a repaired exact head and native evidence, require Lane 03 to rerun ADV-054-A through E unchanged on that repaired surface before reconsidering integration.

Do not open the next source decision while the current typed declaration contract has a known identity-spelling continuity counterexample.

### Lane 02 — only active implementation repair

Repair **only** the declaration-key true-end boundary so artifact v0.4 and evidence-record v0.2 reject final-LF keys such as `"source\n"` under the repository's already-grounded stable-id convention.

Preserve all other Decision 020 behavior:

1. historical source semantics unchanged;
2. same four explicit source classes;
3. same exact containing object + declaration key occurrence identity;
4. no target loading/resolution;
5. no digest verification;
6. no declaration association;
7. no migration mapping;
8. no trust/relevance/closure/acceptance semantics;
9. no Stage 5 integration, epochs, or replay.

Run ADV-054 unchanged, the full deterministic suite, and explicit compile on the repaired exact head. Preserve any failing attempts rather than rewriting them away.

### Lane 03 — wait for repaired Lane 02 head

Do not change production schemas/runtime. Re-run ADV-054-A through E unchanged against the exact repaired Lane 02 head, then run the full repository suite and explicit compile.

If all pass, clear only the declaration-key true-end hold. Do not infer source resolver/integrity/trust/closure/acceptance semantics from that success.

## Still explicitly unresolved

- source target loading/resolver semantics;
- source bytes retention and retrieval;
- integrity-check execution and retained integrity evidence;
- explicit association between locator/content/exact declarations;
- migration objects mapping exact historical declaration occurrences to future typed declarations;
- general provenance relation vocabulary;
- source quality/trust/relevance;
- source completeness/closure;
- dependency admissibility / satisfaction / closure;
- actual production chronology / scheduler order;
- evidence method/source quality, precedence, invalidation dominance, and closure;
- multiple `required_states` semantics;
- logical lineage and `supersedes_ref` validity;
- global occupancy/claim currentness, supersession, and authorization;
- multiple-packet conflict/selection semantics;
- packet acceptance/rejection and durable closure;
- claim closure;
- successor state-revision publication;
- Stage 5 integration receipts/runtime;
- epochs/barriers and replay;
- cross-language graph/reachability/frontier/source transport and reproduction;
- exact self/mutual-cycle authorability through ordinary content-addressed publication;
- stronger filesystem durability/concurrency evidence;
- hostile same-process code isolation beyond the trusted deterministic runtime boundary.

## Four-root gate

- **Truth:** preserve Lane 02's real 410/410 baseline and Lane 03's real focused failure together; do not convert either into a broader claim than its tested surface supports.
- **Agency / non-domination:** no founder, specialist, CI state, branch, schedule position, or Git permission becomes declaration or merge authority.
- **Continuity:** declaration occurrence identity must not depend on runtime-specific knowledge that `$` accepts a final LF; the known counterexample is now durable current-state evidence.
- **Wisdom before speed:** repair the smallest already-known identity-spelling boundary before integrating Decision 020 or opening resolver/integrity/association/trust/closure work.
