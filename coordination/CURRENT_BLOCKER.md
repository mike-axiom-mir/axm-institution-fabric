# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Canonical `main` before this overlay: `2e8f91f78ebf03b8b7cba58dfe2bdb8f38b485e9`
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current bounded gate: **Decision 018 — Exact Reachable Dependency Frontier Facts**
Current disposition: **Decision 017 is canonical on the demonstrated bounded Python v0 read-only reachability surface. Open only the next factual dependency-boundary projection; do not open admissibility, satisfaction, closure, acceptance, Stage 5 integration, epochs, or replay.**

`coordination/CURRENT_WAVE.md` remains historical chronology. This file is the current-state overlay and must be read with the numbered decisions and durable specialist return packets.

## What is now canonical

The bounded Python v0 kernel canonically demonstrates the previously grounded exact identity, immutable-store, lifecycle, packet, evidence-subject, compatibility, provenance, modification, mixed-output, dependency-identity, dependency-context-membership, and same-packet graph surfaces, plus **Decision 017 exact packet-local dependency reachability facts**.

For every exact packet output, Decision 017 now deterministically exposes:

- exact direct packet-local prerequisite refs from incoming Decision 016 `required -> dependent` edges;
- exact strict-transitive packet-local prerequisite refs for paths of length >= 1;
- self-reachability only when a real non-empty self/cycle path grounds it;
- exact-ref lexical presentation without lexical priority;
- no promotion of claim-base-only or outside/unclassified dependencies into packet-local reachability;
- no authority from logical id, version, `supersedes_ref`, recency, array/storage order, output family, actor identity, scheduler position, topological witness, or Git permission.

The per-output reachability leaf is canonical-byte-backed and named. Unsupported ordinary Python stdlib JSON transport fails closed rather than silently positionalizing named institutional meaning.

## Decision 017 integration evidence

### Lane 02 — PR #78

Exact implementation/workflow head:

`7d9eac88734b397b68bb9bd763839c2af7e28f4b`

Exact pull-request merge candidate:

`b37495633fef8b891df04d633cdc61be1335fd27`

Native run `34795321386`, job `103827160883`, was independently inspected and directly recorded:

- Python 3.12.14;
- **342 / 342 tests passed** in 342.090s;
- Decision 017 baseline regressions passed;
- ADV-035 through ADV-050 remained green;
- explicit compile succeeded;
- complete job succeeded.

Lane 02 final head `d017e51f792d91acc26f8414626b921782186e6b` added only its durable return packet after the exact tested implementation/workflow head.

PR #78 was integrated with merge commit:

`94812d89d6a926361c9c41e7e6a5534f8b333dde`

### Lane 03 — PR #79 / ADV-051

The first Lane 03 attempt is preserved as red evidence: run `34796316580`, job `103830006547`, failed during deterministic unittests and skipped compile. Review found an over-strict adversarial copy oracle; Lane 03 corrected only the oracle to the already-grounded **reject or preserve exact meaning** rule. No production code changed in response.

Exact corrected adversarial head:

`8eeb641218f52dabceff3207f661fdaa9a7415a4`

Exact corrected PR merge candidate:

`189c527a0889b94b2de259bc9af344bea4717009`

Native run `34796704131`, job `103831094736`, was independently inspected and directly recorded:

- Python 3.12.14;
- **352 / 352 tests passed** in 538.405s;
- ADV-051-A through J all passed;
- explicit compile succeeded;
- complete job succeeded.

ADV-051 covers diamond/multi-hop preservation, edge direction under hostile lexical order, cycles with upstream prerequisites, sibling non-laundering, sequential parallel-packet isolation, topological-witness non-authority, duplicate-node fail-closed behavior, named proof-to-use transport, aggregate transport boundary, and absence of accidental policy/lifecycle authority.

After Decision 017 integration, PR #79 was retargeted to `main`; the remaining diff contained only workflow coverage, ADV-051 tests, and the durable Lane 03 return packet. It was integrated as:

`2e8f91f78ebf03b8b7cba58dfe2bdb8f38b485e9`

## Decision 017 truth boundary

Decision 017 is canonical only for exact packet-local direct/transitive reachability on the demonstrated Python in-process boundary.

It does **not** establish:

- dependency admissibility / allowed-context policy;
- dependency satisfaction;
- declaration completeness or dependency closure;
- actual production timestamps or execution chronology;
- scheduler order;
- whether same-packet, claim-base, outside/unclassified, self, or cyclic dependencies are permitted;
- packet acceptance/rejection;
- claim closure;
- successor state publication;
- Stage 5 integration correctness;
- epochs/barriers;
- replay correctness;
- supported cross-language graph/reachability transport.

## Explicit cycle-authorability uncertainty

Artifact v0.3 exact refs hash canonical artifact bytes that include `dependency_refs[]`. A direct artifact reference to its own final exact ref appears to require a cryptographic fixed point; a mutual exact cycle appears to require mutually recursive fixed points.

Decisions 016–017 prove deterministic graph/reachability behavior **if cyclic exact graph facts are supplied**. Current evidence does not prove the ordinary content-addressed publication path can author exact self/mutual cycles end-to-end. Do not silently turn that representation uncertainty into either a prohibition or a permission rule.

## Next bounded gap — exact reachable dependency frontier

Decision 017 now makes the packet-local prerequisite subgraph explicit. Decision 015 separately preserves exact dependency declarations and whether each target is in the exact claim-base artifact membership, packet-created outputs, or packet-modified-result outputs.

A later consumer would still have to combine those layers itself to answer a simpler factual question:

> For an exact output and all of its packet-local prerequisites, which exact declared dependencies leave that reachable packet-output subgraph, who declared them, and were those targets exact members of the claim base?

Leaving that traversal implicit risks omissions, reverse traversal, sibling leakage, anonymous target collapse, or hidden policy before dependency closure is even defined.

The next bounded step is therefore **Decision 018 — Exact Reachable Dependency Frontier Facts**.

It is still **reachable declaration fact before dependency policy or closure**.

For each exact output:

1. scope = that output plus every exact strict-transitive packet-local prerequisite from Decision 017;
2. inspect the exact Decision 015 dependency declarations for every output in scope;
3. frontier relations are only declarations whose target is not an exact output of the same packet;
4. every frontier relation preserves exact `declaring_output_ref`, exact `dependency_ref`, and Decision 015 `in_claim_base`;
5. outside-claim-base / unclassified targets remain explicit facts, not automatic valid or invalid dependencies;
6. same-packet dependency targets remain represented by Decisions 016–017 and are not duplicated into frontier authority merely because they may also exist in the claim base;
7. the same target declared by multiple reachable outputs retains each declaring-output relation.

## Lane boundaries

### Lane 02 — active implementation lane

Implement only Decision 018's read-only reachable dependency frontier projection.

Required behavior:

1. consume `preflight_packet_local_dependency_reachability(...)` as the sole packet-local reachability authority;
2. consume the nested canonical Decision 015 dependency records rather than reclassifying through another lookup path;
3. include declarations from the exact output plus all exact strict-transitive packet-local prerequisites;
4. emit exact named frontier relations with declaring output, dependency target, and `in_claim_base`;
5. exclude exact same-packet dependency targets from the frontier;
6. preserve multi-hop and diamond-branch declarations without sibling/dependent leakage;
7. preserve multiple declaring outputs for the same exact target;
8. add no logical-id/version/`supersedes_ref`/recency/order/family/witness/current-state authority;
9. add no `valid`, `allowed`, `satisfied`, `complete`, `closed`, `accepted`, `rejected`, `integrated`, chronology, scheduler, epoch, or replay meaning;
10. follow the existing reject-or-preserve-named-semantics rule for any new operational named leaves;
11. keep ADV-035 through ADV-051 green;
12. stop before admissibility, satisfaction, closure/completeness policy, source/evidence closure, packet acceptance, claim closure, successor publication, Stage 5 integration, epochs, or replay.

### Lane 03 — adversarial lane

Wait for Lane 02's exact tested Decision 018 head, then attack only that frontier projection for:

- reverse/dependent traversal;
- omitted multi-hop declarations;
- sibling/unrelated branch leakage;
- same-packet target promotion into the frontier;
- loss of declaring-output identity when multiple reachable outputs declare the same target;
- claim-base membership becoming precedence or automatic validity;
- outside/unclassified targets being silently accepted/rejected/relabelled;
- same-logical/high-version/`supersedes_ref`/recency substitution;
- array/storage/lexical/topological-witness order authority;
- created/modified-result family precedence;
- later parallel-packet rebinding;
- materialization/transport losing named relation meaning;
- accidental admissibility, satisfaction, closure, chronology, acceptance, integration, epoch, or replay semantics.

### Lane 01 — integration lane

Do not duplicate Decision 018 implementation. Review exact Lane 02 evidence plus Lane 03 attack and integrate only the factual frontier semantics sufficiently grounded under the four roots.

## Still explicitly unresolved

- supported cross-language graph/reachability/frontier transport and any durable protocol;
- exact self/mutual-cycle authorability through ordinary content-addressed publication;
- dependency admissibility / allowed-context policy;
- dependency satisfaction;
- actual production chronology / scheduler ordering;
- declaration completeness and dependency closure policy;
- exact source provenance / `provenance.source_refs[]` taxonomy and closure;
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
- cross-language reproduction generally;
- stronger filesystem durability/concurrency evidence;
- hostile same-process code isolation beyond Decision 009's trusted deterministic runtime boundary.

## Four-root gate

- **Truth:** Decision 017 is limited to directly observed 342/342 implementation evidence and 352/352 corrected ADV-051 evidence; the first red adversarial oracle run remains preserved separately.
- **Agency / non-domination:** no founder, specialist, schedule position, branch ownership, Git permission, version, recency, family, array order, topological witness, or lexical tie-break becomes hidden semantic authority.
- **Continuity:** current reachability meaning, exact evidence, preserved red history, remaining uncertainty, and the next frontier lane are reconstructable from canonical repository state without private chat memory.
- **Wisdom before speed:** make the reachable dependency boundary explicit before choosing admissibility, closure/completeness, packet acceptance, Stage 5 integration, epochs, or replay.
