# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current canonical source precursor: **Decision 022 — Exact Source Runtime Capability Facts**
Current executable source gate: **Decision 023 — Exact Source Live Observation Facts**
Current disposition: **Decision 021 observation-context research is sufficiently bounded to open one local/offline live-store observation slice. Decision 023 explicitly records mutable-context and non-reexecution standing; it does not create an immutable snapshot, retained-byte contract, generic resolver, trust rule, closure rule, Stage 5 integration, epoch, or replay-success semantics.**

This file is the current sequencing pointer. Earlier overlays, red and green specialist runs, Decisions 020–022, and return packets remain historical evidence and are not invalidated or rewritten. `coordination/CURRENT_WAVE.md` remains historical chronology and must not override newer repository state.

## Preserved Decision 022 standing

Decision 022 production integration remains commit `ae2a4171dac0c6bb56b86ac11fc4b987924b4a94`.

It provides one deterministic no-target-I/O runtime capability fact for an exact Decision 020 `exact_axm_object` occurrence:

- exact containing-object identity;
- declaration key;
- exact authored target ref;
- parsed target kind;
- `runtime_capability = supported | unsupported_kind` for the fixed bundled kernel schema context.

Its preserved evidence chain remains green baseline → ADV-057-A red counterexample → bounded repair → independent unchanged-oracle green recheck. The repaired and independent candidates both completed **437/437 deterministic tests plus explicit compile**. Lane 02 Activation 047 later repeated **437/437 plus compile** as a verification-only contribution without opening target observation.

Runtime capability is still not target existence, availability, retrieval, integrity, provenance causality, trust, closure, acceptance, integration, epoch completion, or replay correctness.

## Lane 03 Activation 050 now integrated

Lane 03 PR #108 was integrated as `b2ec5628dd4fd2102d5ac06743b743bb95d37725` before Decision 023 was opened.

Its evidence-only continuity drill demonstrated that a specialist can detect a concurrent main advance, reread the new durable packet, re-anchor its branch, and preserve the target-observation hold without relying on private chat. It also confirmed that stale `CURRENT_WAVE.md`, newer packet timestamps, green CI, branch recency, actor identity, founder identity, or Git permission do not create semantic authority.

No production/schema/fixture/test/workflow semantics changed in that integration.

## Decision 021 final research conclusion

The remaining observation-context question compared:

1. immutable/snapshot-like observation context;
2. retained verified bytes for positive exact observations;
3. explicit context-bound/non-reexecution standing for live observations.

The first executable slice selects **3** as the smallest truthful contract.

The current `FilesystemObjectStore` root is mutable runtime state. A path label therefore MUST NOT be treated as immutable observation-context identity. Instead, Decision 023 explicitly records:

- `observation_method = filesystem_exact_load_v1`;
- `context_standing = live_mutable_store`;
- `reexecution_standing = not_established`.

This keeps two claims separate:

- an immutable recorded observation fact may later be replayed as historical institutional input;
- literal re-execution of the original live filesystem observation is not established.

Immutable snapshots/manifests and retained-byte evidence remain possible later strengthening mechanisms, not hidden assumptions of the first slice.

## Decision 023 bounded implementation contract

Decision 023 applies only to one exact typed `exact_axm_object` declaration occurrence in artifact v0.4 or evidence-record v0.2.

The implementation MUST first preserve/derive the Decision 022 runtime capability for the same exact occurrence.

### Unsupported runtime

If the target kind is `unsupported_kind`:

- perform **no target-object I/O**;
- return explicit `not_attempted_unsupported_kind` / `not_observed` / `not_attempted` / `not_evaluated` standing.

### Supported runtime

If the target kind is supported, use only exact `FilesystemObjectStore.load_bytes(target_object_ref)`.

No logical-id, newest-version, recency, locator, search, network, package, adjacent-source, actor, CI, branch, or Git fallback is allowed.

The durable result must preserve exact occurrence identity and explicit technical dimensions:

- `observation_outcome`;
- `availability_observation`;
- `retrieval_observation`;
- `integrity_observation`.

The authorized outcome classes are:

- exact success → `exact_observed`, observed in this live context, verified bytes obtained, exact identity verified;
- `ObjectNotFoundError` → `not_found_in_live_context`, bytes not obtained, integrity not evaluated;
- `ObjectCorruptionError` → `corrupt_material_in_live_context`, availability indeterminate, unverified bytes obtained, exact identity failed;
- other `ObjectStoreError` → `store_error_in_live_context`, availability indeterminate, bytes not obtained, integrity not evaluated;
- unsupported kind → no observation attempted.

No absolute path, host, process, timestamp, actor, CI, branch, Git state, or exception text belongs in the canonical observation fact.

## What Decision 023 does not prove

Even `exact_observed` does not establish:

- provenance causality;
- source relevance, trust, or quality;
- completeness or closure;
- packet acceptance/rejection;
- claim closure;
- Stage 5 integration;
- epoch completion;
- retained-byte availability;
- future source availability;
- literal observation re-execution;
- replay correctness.

Negative/error results are equally bounded: not-found is context-local, corruption is not a trust verdict, store error leaves availability indeterminate, and unsupported kind is not absence.

## Active lane boundaries

### Lane 01 — integration owner

Decision 023 research/contract is now durable. Do not duplicate Lane 02 implementation work. Integrate only after exact implementation and adversarial evidence are sufficiently grounded against the four roots.

### Lane 02 — current builder

Implement **Decision 023 only** on fresh canonical `main`.

Required evidence includes deterministic tests for:

- exact success;
- context-bound not-found;
- corrupt exact-path material;
- generic store failure remaining indeterminate;
- unsupported kind performing no target I/O;
- equal target refs preserving distinct declaration occurrences;
- stale/mismatched container identity failing closed;
- no logical/newest/locator/recency fallback;
- canonical transport excluding ambient authority;
- repeated identical classified inputs producing identical bytes;
- same textual mutable store root truthfully producing a different later observation after contents change;
- unchanged Decision 022 regressions.

Run the complete deterministic suite and explicit compile.

### Lane 03 — next attacker after Lane 02

Attack the exact tested Decision 023 head for mutable-context laundering, negative-observation globalization, hidden fallback, occurrence collapse, stale rebinding, failure disappearance, ambient metadata leakage, unsupported-kind laundering, and observation→trust/closure/acceptance/reexecution authority.

Do not broaden into source policy that Decision 023 does not authorize.

## Still explicitly unresolved

- immutable/snapshot-like source observation context identity and snapshot completeness;
- retained verified source bytes / retained-byte evidence objects;
- content-address byte-provider and digest verification semantics;
- locator/network/filesystem/package resolver contracts and resolver identity/configuration;
- explicit locator/content/exact association;
- historical-to-typed migration objects;
- provenance-relation vocabulary;
- source trust/quality/relevance/completeness/closure;
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
- cross-language graph/reachability/frontier/source-observation reproduction;
- exact self/mutual-cycle authorability through ordinary content-addressed publication;
- stronger filesystem durability/concurrency evidence;
- hostile same-process code isolation beyond the trusted deterministic runtime boundary.

## Stop rule for the next activation

Do not interpret opening Decision 023 as permission to add snapshots, retained-byte objects, generic resolvers, content-address verification, source trust/closure, Stage 5, epochs, or replay. First prove the bounded live-store exact-source observation contract and preserve its explicit `reexecution_standing = not_established` limitation.
