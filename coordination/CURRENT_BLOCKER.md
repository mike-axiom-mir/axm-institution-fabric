# Current Stage 4 Sequencing Overlay

Date: 2026-09-13
Canonical main after Decision 014 + ADV-047 integration: `bbd633f85ab54214256623e27f3d7cd481a4239b`
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current next bounded gate: **Decision 015 — Exact Dependency Context Membership**

`coordination/CURRENT_WAVE.md` remains historical chronology. This file is the newer current-state overlay and must be read with the numbered decisions and durable specialist return packets.

## What is now canonical

The deterministic institution kernel now canonically demonstrates, on the bounded Python v0 path:

- strict canonical identity and immutable references;
- exact revision membership and exact lifecycle bases;
- occupancy admission, work-claim admission, and return-packet admission from exact historical state;
- exact packet created-artifact and evidence identity;
- exact evidence-subject chronology and bounded output/evidence compatibility;
- exact created-artifact work-base provenance;
- exact two-sided modified-artifact prior/result identity and modified-result compatibility;
- one exact mixed created+modified packet compatibility projection from one exact historical context;
- **Decision 014 exact output dependency target identity** for artifact v0.3 across both created and modified-result output families;
- historical artifact v0.1/v0.2 non-empty dependency strings remain unresolved rather than silently acquiring v0.3 meaning;
- ADV-035 through ADV-047 regression pressure preserving proof-to-use identity, exact historical selection, fail-closed transport/materialization, provenance, output/evidence isolation, modification identity, mixed projection, and dependency-target identity.

This remains a read-only proof surface. Exact dependency identity is not dependency validity, membership policy, chronology, closure, packet acceptance, claim closure, publication, integration, epochs, or replay.

## Decision 014 integration evidence

### Lane 02 — PR #64

Lane 02 implemented artifact v0.3 and the read-only exact dependency-identity preflight. Exact implementation head `21724797dcbab35be849f61ed372a7f46039a675` was independently inspected in native Actions:

- **277 / 277 tests passed**;
- all 12 Decision 014 regressions green;
- ADV-035 through ADV-046 remained green;
- explicit `py_compile` passed.

The final Lane 02 branch head added only its durable return packet. PR #64 was squash-integrated as:

`c54606910734ed4d1731edc4f29029ba89f0aa11`

### Lane 03 — PR #65 / fresh PR #66

Lane 03 independently attacked Decision 014 with ADV-047 A–G: corrupt exact targets, version/`supersedes_ref` decoys, historical-string laundering, source/evidence metadata authority leakage, same-logical/different-exact parallel dependencies, detached materialization drift, and unsupported JSON transport / authority escalation.

Lane 03 exact tested head `28709aec94589774851e295bb7f83b5ff3ba711b` directly completed **284 / 284 tests** and explicit compile successfully.

Because PR #65 was stacked on Lane 02 ancestry, squash-integrating #64 caused GitHub to expose already-canonical production changes again. Lane 01 did not rewrite or merge duplicate production ancestry. Instead it reapplied only Lane 03's evidence-only workflow/test/return-packet files to fresh canonical main in PR #66.

Fresh PR #66 run `34785415878`, job `103799889107` directly recorded:

- Python 3.12.14;
- **284 / 284 tests passed** in 252.451s;
- ADV-047-A/B/C/D/E/F/G all green;
- explicit compile, including the ADV-047 module, passed;
- complete job conclusion: success.

PR #66 was integrated as:

`bbd633f85ab54214256623e27f3d7cd481a4239b`

PR #65 was closed as superseded, not invalidated. Its original branch/run remain preserved evidence.

## Why Stage 4 is not done

Decision 014 proves that a v0.3 output dependency points to one exact immutable artifact. It deliberately does not say whether that exact artifact belongs to the exact historical claim base, is another exact output of the same packet, or sits outside both contexts.

The exact claim-base state revision already carries exact `artifact_refs[]` membership, while Decision 013/014 already carries the packet's exact created and modified-result outputs. That makes dependency **context membership facts** the smallest next mechanical step.

Jumping directly to a validity rule would be premature: requiring every dependency to be a claim-base member could silently outlaw same-packet dependencies, while accepting every exact-loadable dependency could silently treat later/external artifacts as historically available.

## Decision 015 — opened next

See:

`coordination/decisions/015_EXACT_DEPENDENCY_CONTEXT_MEMBERSHIP.md`

Decision 015 opens **classification before policy**:

- consume Decision 014 exact dependency relations;
- exact-load the exact claim-base state revision;
- report exact-ref membership in claim-base `artifact_refs[]`;
- report exact-ref membership in the packet's created and/or modified-result output families;
- preserve a dependency outside both contexts explicitly rather than accepting or rejecting it;
- preserve all simultaneously true factual contexts rather than inventing precedence;
- use exact-ref equality only, with no logical-id/version/`supersedes_ref`/recency/order fallback;
- add no dependency-validity, chronology, closure, cycle, completeness, acceptance, or integration semantics.

No artifact schema version change is required because this step adds no new artifact-authored claim; it derives facts from already exact immutable state.

## Lane boundaries

### Lane 02 — next implementation lane

Implement only Decision 015's read-only exact dependency-context membership projection. Consume Decision 014 rather than rebuilding packet or dependency selection. Keep ADV-035 through ADV-047 green. Stop before dependency validity, same-packet chronology policy, transitive closure/cycles/completeness, source closure, evidence precedence, lineage, packet acceptance, claim closure, successor publication, Stage 5 integration, epochs, or replay.

### Lane 03 — next adversarial lane

After Lane 02 leaves an exact tested head, attack only Decision 015: same-logical/different-exact base substitution, version/`supersedes_ref`/recency/order authority, output-family cross-laundering, external exact targets being silently accepted/rejected, simultaneous factual contexts being collapsed, metadata authority leakage, corrupt/missing/wrong-kind exact base, materialization/transport drift, and accidental validity/closure/acceptance claims.

### Lane 01 — integration lane

Do not implement Decision 015 in parallel with Lane 02. Review the exact tested implementation and independent Lane 03 evidence, preserve failures/dissent, and integrate only if the four-root gate is grounded.

## Still explicitly unresolved

- dependency validity and allowed-context policy;
- dependency chronology and same-packet producer/consumer ordering;
- transitive dependency closure, cycle semantics, and declaration completeness;
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
- cross-language reproduction and supported serialized compatibility transport;
- stronger filesystem durability/concurrency evidence;
- hostile same-process code isolation beyond Decision 009's trusted deterministic runtime boundary.

## Four-root gate

- **Truth:** exact target identity and exact historical/context membership remain distinct facts; neither is promoted into validity or closure.
- **Agency / non-domination:** membership comes from exact immutable state, not status, recency, version, ordering, founder/specialist identity, or Git permission.
- **Continuity:** replacement occupants can reconstruct both the exact dependency and its exact historical/packet context without hidden chat or mutable names.
- **Wisdom before speed:** classify context before deciding chronology, validity, closure, acceptance, integration, epochs, or replay.
