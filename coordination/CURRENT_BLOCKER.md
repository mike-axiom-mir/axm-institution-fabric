# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Canonical `main` reviewed before this Lane 01 branch: **through PR #92 / `65e5b1a9e16fb2662558d198f35df4c79a367520`**
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current bounded gate: **Decision 020 — Typed Source Declaration Contract**
Current disposition: **HOLD. Lane 02 repaired the ADV-054 declaration-key true-end bug and Lane 03 independently cleared that exact hold unchanged, but Lane 01 integration review reproduced a second narrow true-end ambiguity in Decision 020's `content_address.digest`: the shared schema's `^[0-9a-f]{64}$` accepts 64 lowercase hex characters followed by a final LF on the demonstrated Python/jsonschema path. PR #94 preserves ADV-055-A as red evidence. Do not integrate PR #90 until only this digest spelling boundary is repaired and independently rerun. Resolver/loading, integrity execution, declaration association, migration mapping, trust, closure, packet acceptance, Stage 5 integration, epochs, and replay remain closed.**

`coordination/CURRENT_WAVE.md` is historical chronology. This file is the current-state overlay and must be read with Decision 020, newest commits/PRs/branches, and durable Lane 01/02/03 return packets.

## Canonical kernel boundary before Decision 020

The deterministic Python v0 kernel canonically demonstrates the previously grounded exact identity, immutable store, exact revision membership, lifecycle relationship grounding, bounded occupancy/work-claim/return-packet admission, exact output/evidence identity, exact evidence subject binding, created/modified/mixed output compatibility facts, artifact provenance-base facts, two-sided modification identity, exact dependency identity/context membership, packet-local dependency graph/reachability, Decision 018 reachable dependency-frontier facts, and historical source-ref non-reinterpretation evidence.

Decision 019 established the four source target classes while keeping historical source strings opaque. Neither Decision 019 nor Decision 020 establishes source resolution, integrity success, trust, closure, acceptance, integration, epochs, or replay.

## Decision 020 baseline and first repair — PR #90

Lane 02 PR #90 implements only the versioned typed source-declaration contract. The first exact tested Decision 020 surface recorded **410/410 tests passed plus explicit compile**, but Lane 03 ADV-054-A then reproduced the already-known `$` false-end ambiguity on declaration keys.

Lane 02 repaired only that declaration-key boundary.

Exact repaired Lane 02 test-bearing head:

`9aeb6eea36defc0b9ee14bb2931b9873fc0c093b`

Exact repaired merge candidate against canonical main:

`a05744b5fe80730e8cfb5722eb8df8390aebd2dd`

Native run/job:

`34813097716` / `103878151574`

Direct evidence:

- unchanged ADV-054-A through E: **5/5 passed**;
- full deterministic suite: **415/415 passed**;
- explicit compile: **passed**.

Lane 02 final branch head `b97746c585c8c50a379060766076be5dd9072015` adds its durable return packet after the repaired test-bearing head.

The repaired schema uses true-end semantics for typed declaration keys:

```text
^[a-z0-9][a-z0-9._-]*(?![\s\S])
```

The prior red ADV-054 run remains valid historical evidence and is not erased by the repair.

## Independent ADV-054 clearance — PR #93

Lane 03 reran the byte-identical ADV-054 oracle against the repaired Lane 02 surface.

Exact Lane 03 tested head:

`3053e8da75f46ef1caf1879f90c89c5c5c6492a8`

Exact PR merge candidate:

`525c4770b1515decb245fe718246f76a652e1954`

Native run/job:

`34814179663` / `103881294495`

Direct evidence:

- unchanged ADV-054-A through E: **5/5 passed**;
- full deterministic suite: **415/415 passed**;
- explicit compile: **passed**;
- complete job: **success**.

This clears only the declaration-key true-end hold on the demonstrated Python/jsonschema surface. It does not authorize broader source semantics or Decision 020 integration by itself.

## ADV-055 hold — PR #94

During Lane 01's four-root integration review, the same producer/parser continuity class was found on the new `content_address.digest` spelling boundary.

Decision 020 requires:

```text
algorithm = sha256
digest = exactly 64 lowercase hexadecimal characters
byte_scope = raw_bytes
```

The current shared declaration schema uses:

```text
^[0-9a-f]{64}$
```

On the demonstrated Python/jsonschema path, `$` accepts a final LF. Therefore a digest containing 64 lowercase hex characters plus `"\n"` can pass the schema even though it is not the exact 64-character identity spelling Decision 020 claims.

Lane 01 opened PR #94 stacked on the repaired Lane 02 branch and added only one adversarial regression:

`ADV-055-A — trailing LF content digest must fail exact 64-hex spelling`

Exact PR #94 head:

`c705d558e8bd881c1f44fd0887a9b037953b16a1`

Native run:

`34816432992`

Native job:

`103887966260`

Observed workflow facts:

- checkout/setup/install succeeded;
- the focused typed-source adversarial step **failed**;
- full deterministic suite was skipped after that failure;
- explicit compile was skipped after that failure;
- complete workflow conclusion: **failure**.

PR #94 changes only the adversarial test file. The same repaired Decision 020 surface had just passed ADV-054 5/5 on Lane 03's independent run. Combined with the known JSON-Schema `$` end behavior and the exact one-test delta, this is sufficient to preserve ADV-055 as a current blocker pending Lane 02's narrow repair. Do not overclaim a new full-suite result from this red run.

This finding does **not** reopen the four-class source taxonomy and does not authorize resolver, integrity verification, association, migration, trust, closure, acceptance, Stage 5 integration, epoch, or replay work.

## Active lane boundaries

### Lane 01 — sequencing / integration

Hold Decision 020 integration. Preserve both the cleared ADV-054 evidence and the new ADV-055 red evidence. Do not merge PR #90 or open the next source semantic decision while the content-address spelling boundary remains ambiguous.

PR #94 is adversarial evidence stacked on PR #90, not a production repair lane.

### Lane 02 — only active implementation repair

Repair **only** the `content_address.digest` true-end boundary so a typed source digest accepts exactly 64 lowercase hex characters and rejects a final LF or any trailing character.

Prefer the repository's already-grounded true-end convention rather than introducing a second spelling mechanism.

Preserve every other Decision 020 behavior:

1. historical source semantics unchanged;
2. the same four explicit source classes;
3. exact containing object + declaration key occurrence identity;
4. no target loading/resolution;
5. no digest verification or integrity-success claim;
6. no declaration association;
7. no migration mapping;
8. no trust/relevance/closure/acceptance semantics;
9. no Stage 5 integration, epochs, or replay.

Run ADV-054-A through E plus ADV-055-A unchanged, then the full deterministic suite and explicit compile on the repaired exact head. Preserve any failing attempt rather than rewriting it away.

### Lane 03 — after repaired Lane 02 head

Do not change production schemas/runtime. Independently rerun the unchanged ADV-054 + ADV-055 oracle against the exact repaired Lane 02 head, followed by the full repository suite and explicit compile.

If green, clear only the demonstrated true-end source spelling holds and hand back to Lane 01. Do not infer source resolver/integrity/trust/closure/acceptance semantics from success.

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

- **Truth:** preserve the first red ADV-054 result, the repaired and independently green ADV-054 result, and the new red ADV-055 result together. Do not let 415/415 on the earlier oracle erase a contract case it never tested.
- **Agency / non-domination:** no founder, lane, CI state, branch, schedule position, or Git permission becomes source or merge authority.
- **Continuity:** a replacement occupant must not need runtime-specific knowledge that `$` may accept a final LF to reconstruct the exact spelling of an immutable content address.
- **Wisdom before speed:** repair one demonstrated identity-spelling boundary before integrating Decision 020 or opening resolver/integrity/association/trust/closure work.
