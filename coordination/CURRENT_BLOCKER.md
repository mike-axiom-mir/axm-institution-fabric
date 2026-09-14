# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current canonical source precursor: **Decision 022 — Exact Source Runtime Capability Facts**
Current executable source gate: **Decision 023 — Exact Source Live Observation Facts**
Current disposition: **Lane 02 now has a green exact Decision 023 implementation baseline, but Decision 023 is not yet canonical. Integration is held pending the Decision 023 contract's required independent Lane 03 adversarial attack of that exact tested surface. Decision 023 still records mutable-context and non-reexecution standing and does not create an immutable snapshot, retained-byte contract, generic resolver, trust rule, closure rule, Stage 5 integration, epoch, or replay-success semantics.**

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

## Lane 03 continuity repairs now integrated

Lane 03 PR #108 was integrated as `b2ec5628dd4fd2102d5ac06743b743bb95d37725` before Decision 023 was opened.

Its evidence-only continuity drill demonstrated that a specialist can detect a concurrent main advance, reread the new durable packet, re-anchor its branch, and preserve the target-observation hold without relying on private chat. It also confirmed that stale `CURRENT_WAVE.md`, newer packet timestamps, green CI, branch recency, actor identity, founder identity, or Git permission do not create semantic authority.

Lane 03 PR #111 was later squash-integrated as `df0b7721a07a76ec8bdf14b04be1b870ba66733f`. It repairs a narrower replacement-occupant discovery gap by making both `coordination/CURRENT_WAVE.md` and this current sequencing pointer explicit mandatory reads in Lane 03's standing role while preserving the requirement to verify repository evidence rather than treating filenames or recency as authority.

Neither Lane 03 integration changed production/schema/fixture/test/workflow/source-observation semantics.

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

If the target kind is supported, use only exact `FilesystemObjectStore.load_bytes(target_object_ref)` under the **same fixed bundled kernel schema interpretation context used by Decision 022**.

A `FilesystemObjectStore` configured with a caller-supplied/custom `schema_dir` is outside Decision 023 and MUST fail closed before target-object I/O. The first observation slice may not classify capability using bundled schemas and then validate the target under caller-selected schemas. This guard preserves interpretation coherence; it does not turn the live bundled schema directory into immutable historical context.

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

A custom/non-bundled schema context is rejected before this target-result mapping. It is not target absence, target corruption, or a target-store error.

No absolute path, host, process, timestamp, actor, CI, branch, Git state, or exception text belongs in the canonical observation fact.

## Lane 02 Activation 048 implementation baseline — green but not yet canonical

Open PR #112 supplies the first executable Decision 023 implementation.

Exact Lane 02 head:

`26bd68b53c7521f7f5667b3c924e226bd2c95441`

Exact GitHub Actions PR merge candidate tested against then-canonical base `8aa200f52a6beb278fb0b6f874b57472646b5a0f`:

`3ee7537fe8cf6e70f32c117219c6596f94ab9593`

Directly inspected GitHub Actions run `34852346204`, job `104003161853`, recorded:

- Decision 020 ADV-054/055 unchanged oracle: **6/6 passed**;
- Decision 022 ADV-057 unchanged oracle: **6/6 passed**;
- Decision 023 focused implementation suite: **14/14 passed**;
- complete deterministic suite: **451/451 passed in 491.670s**;
- explicit compile: **passed**.

The focused Decision 023 suite covers exact success, typed evidence occurrence, context-local not-found, exact-path corruption, generic store error, unsupported-kind no-I/O, equal-target occurrence separation, stale container failure before target I/O, no newest-same-logical fallback, bounded canonical transport, deterministic repeated bytes, mutable same-root observations changing over time without contradiction, and custom-schema rejection before target I/O/outcome mapping.

This evidence belongs to the exact tested candidate above. It does not by itself authorize canonical integration and is not silently re-labelled as testing later `main` ancestry.

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

Negative/error results are equally bounded: not-found is context-local, corruption is not a trust verdict, store error leaves availability indeterminate, unsupported kind is not absence, and a rejected custom schema context is only outside this slice's interpretation authority.

## Active lane boundaries

### Lane 01 — integration owner

Decision 023 implementation baseline is green but **integration is held**. Do not merge PR #112 until the exact tested implementation surface has received the required independent Lane 03 adversarial attack and any resulting red evidence/repair chain is explicit. Do not duplicate Lane 03's attack or Lane 02's repair lane.

### Lane 02 — builder / repair owner if needed

Preserve PR #112 and its exact tested evidence. Do not broaden the observer while Lane 03 attacks it. If Lane 03 demonstrates a counterexample, repair only the demonstrated Decision 023 failure surface, then rerun the unchanged relevant adversarial oracle, complete deterministic suite, and explicit compile.

### Lane 03 — current attacker

Attack exact Lane 02 Decision 023 head `26bd68b53c7521f7f5667b3c924e226bd2c95441` / recorded tested candidate `3ee7537fe8cf6e70f32c117219c6596f94ab9593` for:

- mutable-context laundering and same textual root with changed contents;
- negative-observation globalization;
- corrupt/store-error outcome collapse or disappearance;
- hidden logical/newest/locator/recency fallback;
- occurrence collapse and stale occurrence rebinding;
- ambient metadata leakage;
- unsupported-kind laundering;
- bundled-capability/custom-schema-context mixing;
- observation → provenance/trust/closure/acceptance/literal-reexecution/replay-success authority.

Do not broaden into source policy that Decision 023 does not authorize.

## Still explicitly unresolved

- immutable/snapshot-like source observation context identity and snapshot completeness;
- retained verified source bytes / retained-byte evidence objects;
- custom/non-bundled source-observation schema-context identity/configuration;
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

Do not interpret Lane 02's green Decision 023 baseline as canonical authorization. First complete the independent Lane 03 attack of the exact tested implementation and preserve any counterexample, repair, and recheck chain explicitly. Do not add custom schema observation contexts, snapshots, retained-byte objects, generic resolvers, content-address verification, source trust/closure, Stage 5, epochs, or replay merely because the bounded observer is green.
