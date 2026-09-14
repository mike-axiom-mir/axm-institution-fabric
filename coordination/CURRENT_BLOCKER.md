# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Canonical `main` before this overlay: `340ef608693b9706e71f86c8d8c3f4cb2e13f525`
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current bounded gate: **Decision 017 — Exact Packet-Local Dependency Reachability Facts**
Current disposition: **Decision 016 is canonical. The ADV-049-J transport hold is cleared only for the demonstrated Python in-process / fail-closed ordinary-JSON boundary. Open the next read-only graph-fact step; do not open dependency policy, closure, acceptance, integration, epochs, or replay.**

`coordination/CURRENT_WAVE.md` remains historical chronology. This file is the current-state overlay and must be read with the numbered decisions and durable specialist return packets.

## What is now canonical

The bounded Python v0 kernel canonically demonstrates the previously grounded exact identity, immutable-store, lifecycle, packet, evidence-subject, compatibility, provenance, modification, mixed-output, dependency-identity, and dependency-context-membership surfaces, plus **Decision 016 exact same-packet dependency graph facts**.

Decision 016 now provides one read-only graph projection whose authority is limited to already-grounded Decision 015 facts:

- exact created and modified-result packet output refs are graph nodes;
- an exact same-packet dependency creates only the directed fact `required_output_ref -> dependent_output_ref`;
- claim-base-only and external/unclassified dependencies remain visible in the nested Decision 015 context and do not become packet-local edges;
- created/modified-result family labels do not become precedence;
- exact self-edge and SCC/cycle facts are preserved;
- acyclic graphs may expose one exact-ref-lexically-tiebroken topological witness;
- that witness is not historical execution chronology, scheduler authority, required production order, dependency validity, packet acceptance, or integration authority.

The graph leaf family now uses canonical-byte-backed immutable named representations for:

- `ExactPacketOutputNode`;
- `ExactSamePacketDependencyEdge`;
- `ExactStronglyConnectedComponent`.

Unsupported ordinary Python stdlib JSON transport fails closed instead of silently converting those named records into positional arrays.

## Decision 016 integration evidence

### Historical failure remains part of the truth record

Before repair, Lane 03 ADV-049 reproduced the same narrow failure twice:

- **321 tests ran / 320 passed / exactly ADV-049-J failed**;
- ADV-049-A through I and all prior tests remained green;
- `ExactSamePacketDependencyEdge` could serialize through stdlib JSON as `[required_output_ref, dependent_output_ref]`, losing named direction semantics.

Those failures are not invalidated by the repair. PR #73 was closed as **superseded historical adversarial evidence**, not merged and not relabelled successful.

### Lane 02 repair — PR #72

Exact repaired implementation/test/workflow head:

`0d8a79142d87eb6a060cb167cb086f194d1ed2d2`

Native run `34792255883`, job `103818527871`, directly recorded:

- Python 3.12.14;
- **324 / 324 tests passed**;
- unchanged ADV-049-A through J all passed;
- three coherent node/edge/SCC transport regressions passed;
- all ten Decision 016 baseline regressions passed;
- prior regression surface remained green;
- explicit `py_compile` success;
- complete job conclusion success.

Lane 02 final head `e4358c6fdcbc74879a6074c9b8b3e1e10fcaa414` adds only its durable return packet beyond the tested head.

PR #72 was integrated by a merge commit, preserving its branch ancestry and evidence history:

`82713b5c2f65a3ad827c43f26aaf4f4e05f4df9d`

### Lane 03 independent repair re-attack — PR #76

Lane 03 changed no production runtime or schema semantics. ADV-050 added five repair-specific regressions covering:

- named direction in the physical canonical edge payload;
- nested ordinary JSON transport;
- named detached `_asdict()` materialization;
- copy/deepcopy reject-or-preserve behavior;
- aggregate graph transport not silently becoming a positional protocol.

Exact tested Lane 03 head:

`becb799c4d2845f891abdf9fed1d927fa98c90fa`

Native run `34792949677`, job `103820507263`, recorded:

- full deterministic unittest discovery: success;
- explicit compile including ADV-050: success;
- complete job conclusion: success.

The connector-visible specialist record deliberately does not promote `329` from source accounting into a directly observed stdout count.

After Decision 016 became canonical, PR #76 was retargeted to canonical `main`; its resulting diff contained only workflow compile coverage, ADV-050 tests, and the Lane 03 durable return packet. It was integrated as:

`340ef608693b9706e71f86c8d8c3f4cb2e13f525`

## Decision 016 truth boundary

Decision 016 is canonical only for the demonstrated read-only graph facts and Python proof-to-use boundary.

It does **not** establish:

- supported cross-language graph transport;
- dependency admissibility or allowed-context policy;
- dependency satisfaction;
- historical production timestamps or actual execution chronology;
- transitive dependency closure or declaration completeness;
- whether same-packet dependencies are permitted;
- whether cycles or self-dependencies are permitted;
- packet acceptance/rejection;
- claim closure;
- successor state publication;
- Stage 5 integration correctness;
- epoch/barrier semantics;
- replay correctness.

## Explicit cycle-authorability uncertainty

Artifact v0.3 exact refs hash canonical artifact bytes that include `dependency_refs[]`. An artifact that directly names its own final exact ref appears to require a cryptographic fixed point; mutual exact cycles appear to require mutually recursive fixed points.

Decision 016 proves deterministic preservation/detection of already-grounded cyclic topology at the graph-kernel level. Current evidence does **not** prove that the normal content-addressed object-store authoring path can create exact self/mutual cycles end-to-end.

Do not silently turn that representation uncertainty into either "cycles are impossible" or a validity policy.

## Next bounded gap — exact packet-local dependency reachability

Decision 016 exposes exact direct edges, SCC/cycle facts, and an acyclic witness, but later consumers would still need to derive transitive packet-local prerequisite facts themselves. If different occupants or runtimes derive those facts differently, continuity can drift before dependency closure or integration policy even begins.

The next bounded step is therefore **Decision 017 — Exact Packet-Local Dependency Reachability Facts**.

It is still graph fact before dependency policy.

For each exact packet-output node, derive only the packet-local strict reachability facts already implied by Decision 016:

```text
exact output node
    -> exact direct required packet-output refs
    -> exact transitive required packet-output refs
```

A transitive prerequisite is an exact packet-output node reachable by one or more Decision 016 `required -> dependent` edges in the reverse prerequisite direction from the dependent node. Presentation must be deterministic and exact-ref lexical only.

For cyclic topology, strict reachability may include the starting node only when a non-empty path returns to it. That is a graph fact, not cycle validity or permission.

Claim-base-only and external/unclassified dependencies remain outside packet-local reachability; they stay visible only through the nested Decision 015/016 context.

## Lane boundaries

### Lane 02 — active implementation lane

Implement only Decision 017's read-only exact packet-local prerequisite reachability projection by consuming Decision 016 unchanged.

Required behavior:

1. Decision 016 remains the sole packet-local node/edge authority;
2. expose deterministic exact direct prerequisite refs per exact output;
3. expose deterministic exact strict transitive prerequisite refs per exact output;
4. preserve cycle/self-reachability as graph facts without assigning validity;
5. do not promote claim-base-only/external dependencies into packet-local reachability;
6. do not infer logical-id/version/`supersedes_ref`/recency/array-order/family/actor/scheduler/Git authority;
7. do not label the topological witness historical chronology;
8. add no `valid`, `allowed`, `satisfied`, `closed`, `complete`, `accepted`, `rejected`, `integrated`, epoch, or replay meaning;
9. keep ADV-035 through ADV-050 green;
10. stop before dependency admissibility, closure/completeness, source/evidence closure, packet acceptance, successor publication, Stage 5 integration, epochs, or replay.

If new named operational leaf records are introduced, preserve the already-grounded proof-to-use transport rule: unsupported ordinary transport must fail closed or preserve named semantics exactly.

### Lane 03 — adversarial lane

Wait for Lane 02's exact tested Decision 017 head, then attack only that new reachability projection for:

- edge-direction inversion;
- missing multi-hop prerequisites;
- base-only/external dependency promotion;
- same-logical/version/`supersedes_ref` substitution;
- array/storage/recency order affecting reachability;
- created/modified-result family precedence;
- parallel-packet rebinding;
- self/cycle reachability being dropped or fabricated;
- lexical presentation order becoming semantic authority;
- topological witness being misused as chronology;
- materialization/transport losing exact named meaning;
- accidental validity, closure, acceptance, integration, epoch, or replay claims.

### Lane 01 — integration lane

Do not duplicate Decision 017 implementation. Preserve this sequencing boundary, review Lane 02 evidence plus Lane 03 attack, and integrate only the exact facts sufficiently grounded under the four roots.

## Still explicitly unresolved

- supported cross-language graph transport and any durable graph serialization protocol;
- exact cycle authorability through normal content-addressed artifact publication;
- dependency admissibility / allowed-context policy;
- actual production chronology / scheduler ordering;
- transitive dependency **closure/completeness policy** even after factual reachability exists;
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

- **Truth:** preserve the two pre-repair ADV-049 failures, the repaired 324/324 result, and the independent ADV-050 success together; Decision 016 is not widened into policy or chronology.
- **Agency / non-domination:** no founder, specialist, schedule position, branch ownership, Git permission, version, recency, array order, family, or lexical tie-break becomes semantic authority.
- **Continuity:** Decision 016's graph meaning, transport repair, historical failure, independent re-attack, remaining cycle uncertainty, and the next lane are reconstructable from canonical repository state without private chat memory.
- **Wisdom before speed:** derive exact reachability facts before inventing dependency admissibility, closure, packet acceptance, Stage 5 integration, epochs, or replay.
