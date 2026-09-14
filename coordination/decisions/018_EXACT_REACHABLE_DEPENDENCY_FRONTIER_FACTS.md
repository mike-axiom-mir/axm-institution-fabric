# Decision 018 — Exact Reachable Dependency Frontier Facts

Status: **accepted as the next bounded Stage 4 preflight after canonical Decision 017, subject to implementation and adversarial evidence before integration.**

Decision 017 now canonically reconstructs, for every exact packet output, its direct and strict-transitive packet-local prerequisites from the already-grounded Decision 016 graph. Decision 015 still preserves every exact dependency declaration together with independent exact-context membership facts.

The next missing fact remains narrower than dependency policy or closure: **when an output depends on packet-local prerequisite outputs, which exact declared dependencies leave that reachable packet-local subgraph and point to the exact claim base or to an outside/unclassified target?**

## Problem

Today a later consumer can combine Decision 017 reachability with the nested Decision 015 dependency records itself. Leaving that combination implicit creates another continuity gap. Different occupants could accidentally:

- inspect only the final output's own non-packet dependencies and omit those declared by transitive packet-local prerequisites;
- walk dependents instead of prerequisites and inherit the wrong branch's declarations;
- collapse declarations from different prerequisite outputs into one relation and lose who declared what;
- promote a same-packet dependency into an external/base frontier relation;
- choose by logical id, version, `supersedes_ref`, recency, array order, family, or topological witness;
- treat a reachable declaration as proof that the dependency is allowed, satisfied, complete, historically prior, or sufficient for acceptance.

Those would add hidden authority or hidden traversal conventions before dependency policy is grounded.

## Decision

Open one **read-only exact reachable dependency frontier projection** over canonical Decisions 015–017.

For each exact packet output `O`:

1. Let `reachable_output_scope(O)` be `O` plus every exact packet-output ref in Decision 017's `strict_transitive_prerequisite_refs` for `O`.
2. For every exact output in that scope, consume its exact Decision 015 dependency declarations unchanged.
3. A declaration becomes a **frontier relation** only when its exact target is not another exact packet output of the same packet — that is, both `in_packet_created` and `in_packet_modified_result` are false in Decision 015.
4. Every frontier relation must retain at least:
   - the exact `declaring_output_ref`;
   - the exact `dependency_ref`;
   - the exact Decision 015 `in_claim_base` fact.
5. A frontier target with `in_claim_base == false` remains **outside-claim-base / unclassified on this projection**. Do not silently rename it valid external state, invalid state, missing state, or an integration blocker.
6. If the same exact dependency target is declared by multiple reachable outputs, preserve the declaring-output relation rather than collapsing those declarations into one anonymous target.
7. Packet-local dependencies remain represented by Decisions 016–017 and do not also become frontier relations merely because they are present in the exact claim base. Their independent historical membership facts remain inspectable through the nested Decision 015 context.
8. Presentation may be deterministically sorted by exact refs, but lexical order is presentation only and carries no priority, chronology, or scheduler meaning.

The result must preserve the nested Decision 017 projection so the exact packet, claim, base, occupancy, lane, graph, reachability, and upstream membership evidence remain reconstructable.

## Exact non-authorities

Frontier selection or meaning must not be changed by:

- logical artifact id;
- artifact `version`;
- `supersedes_ref`;
- `provenance.source_refs[]`;
- artifact-local `evidence_refs[]`;
- packet/output/dependency array order;
- store insertion order or recency;
- newest/current lookup;
- output family;
- actor/founder/specialist identity;
- Decision 016 topological-witness position;
- scheduler position;
- Git permission;
- lexical position except deterministic presentation.

Exact Decision 015 dependency records and Decision 017 prerequisite reachability are the only authorities for this projection.

## Bounded runtime meaning

A successful Decision 018 projection establishes only that a replacement occupant can deterministically reconstruct, for each exact packet output, the exact non-packet dependency declarations reachable through that output's packet-local prerequisite subgraph, while retaining which exact reachable output declared each dependency and whether Decision 015 found the dependency in the exact claim-base artifact membership.

It does **not** establish:

- dependency admissibility or allowed-context policy;
- that a claim-base dependency is usable, current, sufficient, or historically available at execution time;
- that an outside/unclassified dependency is allowed or disallowed;
- dependency satisfaction;
- declaration completeness or dependency closure;
- source-provenance closure;
- actual production timestamps or execution chronology;
- scheduler order;
- cycle permission or exact cyclic-artifact authorability;
- packet acceptance/rejection;
- claim closure;
- successor state-revision publication;
- Stage 5 integration;
- epoch/barrier completion;
- replay correctness.

This remains **reachable declaration fact before dependency policy or closure**.

## Lane 02 — smallest implementation

Implement only a read-only Decision 018 projection that:

1. consumes `preflight_packet_local_dependency_reachability(...)` as the sole packet-local reachability authority;
2. reuses the nested canonical Decision 015 dependency-context facts rather than reloading or reclassifying dependencies through a second authority path;
3. builds each output's reachable output scope from the exact output itself plus its Decision 017 strict-transitive prerequisite refs;
4. emits named deterministic frontier relations carrying exact declaring-output ref, exact dependency ref, and `in_claim_base`;
5. excludes exact same-packet dependency targets from the frontier while leaving their nested Decision 015 membership facts intact;
6. preserves declarations from all reachable prerequisite outputs, including multi-hop and diamond branches, without sibling/dependent leakage;
7. introduces no logical-id/version/`supersedes_ref`/recency/order/family/witness/current-state authority;
8. exposes no `valid`, `allowed`, `satisfied`, `closed`, `complete`, `accepted`, `rejected`, `integrated`, execution-time, scheduler, epoch, or replay field;
9. if new named operational leaf records are introduced, follows the established reject-or-preserve-named-semantics transport rule;
10. keeps ADV-035 through ADV-051 green;
11. stops before admissibility, satisfaction, closure/completeness policy, source/evidence closure, packet acceptance, claim closure, successor publication, Stage 5 integration, epochs, or replay.

No authored schema migration is required for this bounded step because it derives read-only facts from already exact immutable relations and adds no artifact-authored or packet-authored assertion.

## Minimum implementation regressions

At minimum, prove:

- an output with one direct claim-base dependency produces one frontier relation naming that output as declarer;
- an outside/unclassified exact dependency remains explicit with `in_claim_base == false` and gains no validity meaning;
- a final output inherits a non-packet declaration from a direct packet-local prerequisite;
- a three-node chain carries a root prerequisite's non-packet declaration to the final output;
- a diamond carries frontier declarations from both prerequisite branches without cross-inventing declarations;
- a sibling output outside the prerequisite subgraph contributes nothing;
- exact same-packet dependency targets do not become frontier relations;
- a packet-output target that is also a claim-base member remains a packet-local path rather than being duplicated as frontier authority;
- the same exact dependency declared by two reachable outputs preserves both declaring-output relations;
- packet/output/dependency order and lexical position do not change frontier facts;
- same-logical/high-version/`supersedes_ref` decoys do not substitute;
- no validity, satisfaction, completeness, closure, chronology, acceptance, integration, epoch, or replay authority appears.

Cycle-focused tests may remain direct projection/kernel tests where exact content-addressed cyclic artifact authorability is still unproven. Do not relabel them end-to-end publication evidence.

## Lane 03 — adversarial surface

Attack the exact Lane 02 head for at least:

- traversal in the dependent direction instead of the prerequisite direction;
- omission of multi-hop prerequisite declarations;
- sibling or unrelated branch declaration leakage;
- same-packet targets being promoted to frontier relations;
- loss of the exact declaring-output identity when the same dependency is declared more than once;
- claim-base membership becoming precedence or automatic validity;
- outside/unclassified dependencies being silently rejected or relabelled valid external state;
- same-logical-id / high-version / `supersedes_ref` / recency substitutions;
- array/storage/lexical/topological-witness ordering changing frontier facts;
- created/modified-result family precedence;
- later parallel-packet rebinding;
- materialization/transport changing named declaring-output/dependency meaning;
- accidental admissibility, satisfaction, closure, chronology, acceptance, integration, epoch, or replay semantics.

Do not expand the attack into choosing the actual dependency policy.

## Preserved uncertainty

Decision 018 deliberately does not resolve:

- whether claim-base, same-packet, or outside/unclassified dependency contexts are allowed;
- whether a declaration is complete or sufficient;
- exact self/mutual-cycle authorability under the current content-addressed artifact representation;
- supported cross-language graph/reachability/frontier transport;
- source/evidence provenance quality and closure;
- multiple-packet conflict/selection semantics;
- actual execution chronology or scheduler semantics.

## Root grounding

- **Truth:** derive only exact reachable declaration facts already implied by canonical Decisions 015–017; do not relabel them validity, satisfaction, closure, chronology, or acceptance.
- **Agency / non-domination:** no founder, specialist, scheduler, Git permission, recency, version, family, logical id, witness, or ordering convention chooses the dependency frontier.
- **Continuity:** another occupant can reconstruct the same reachable non-packet dependency boundary, including who declared each exact dependency, without private traversal assumptions.
- **Wisdom before speed:** make the reachable dependency boundary explicit before deciding admissibility, closure/completeness, packet acceptance, Stage 5 integration, epochs, or replay.
