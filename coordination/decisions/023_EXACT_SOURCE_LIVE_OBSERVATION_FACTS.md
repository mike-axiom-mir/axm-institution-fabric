# Decision 023 — Exact Source Live Observation Facts

Date: 2026-09-14
Status: **implementation open for the bounded local/offline slice below; no generic resolver, immutable snapshot, trust policy, closure rule, packet acceptance, Stage 5 integration, epoch, or replay-success semantics are authorized.**

## Why this decision exists

Decision 020 made source identity explicit. Decision 022 then separated runtime interpretation capability from target observation without touching the target path. Decision 021 remained open because the current `FilesystemObjectStore` root is mutable runtime state: recording a path cannot honestly prove that the same live store state can later be reconstructed and re-observed.

The smallest truthful next step is therefore **not** to invent an immutable store snapshot. It is to make the limitation explicit.

Decision 023 authorizes one read-only exact-source observation against a caller-supplied live mutable local store while recording that literal re-execution of that live context is **not established**. Institutional replay of the resulting immutable fact is a different claim from re-running the original filesystem observation.

## Scope

Decision 023 applies only to one Decision 020 `exact_axm_object` declaration occurrence in an exact typed artifact v0.4 or evidence-record v0.2 container.

The projection MUST first derive the Decision 022 runtime capability for that same exact occurrence.

- If `runtime_capability = unsupported_kind`, target-object I/O MUST NOT be attempted.
- If `runtime_capability = supported`, the observation MUST keep the same fixed bundled kernel schema interpretation context used by Decision 022, then MAY use only `FilesystemObjectStore.load_bytes(target_object_ref)` with the ordinary inferred schema for that exact ref.
- A `FilesystemObjectStore` configured with a caller-supplied/custom `schema_dir` is outside this first executable slice and MUST fail closed **before target-object I/O**. Decision 023 does not authorize mixing bundled capability classification with caller-selected target-validation schemas.
- No logical-id, newest-version, recency, locator, search, network, package, adjacent-declaration, branch, actor, CI, or Git fallback is permitted.
- `opaque_label`, `content_address`, and `locator` declarations remain outside this executable slice.

The bundled-schema guard is an interpretation-coherence boundary, not a claim that the bundled schema directory is immutable historical context. The bundled schema files are still live runtime material unless a later snapshot/context decision says otherwise.

## Durable occurrence identity

Every result MUST preserve:

- `containing_object_ref` — exact immutable identity of the typed object containing the declaration;
- `declaration_key` — exact declaration occurrence key;
- `target_object_ref` — exact authored AXM target reference;
- `target_kind` — kind parsed from the target ref;
- `runtime_capability` — `supported | unsupported_kind` from Decision 022.

Equal target refs under different declaration occurrences MUST NOT collapse durable attribution. Implementations may reuse internal work, but the returned institutional facts remain occurrence-bound.

## Explicit live-context standing

The first implementation MUST carry these fixed standing facts:

- `observation_method = filesystem_exact_load_v1`;
- `context_standing = live_mutable_store`;
- `reexecution_standing = not_established`.

These literals deliberately do **not** identify a filesystem path, host, process, actor, timestamp, branch, CI run, or Git state. Those values are not immutable source authority.

`reexecution_standing = not_established` means only that this result does not prove the original live filesystem state can later be reconstructed and observed again. It does not invalidate the observation as historical input to later deterministic institutional replay.

A later decision may introduce an immutable/snapshot-like observation context. Decision 023 does not.

## Observation dimensions

The result MUST keep technical truth dimensions explicit. A single success/failure boolean is not sufficient.

### `observation_outcome`

Exactly one of:

- `exact_observed`
- `not_found_in_live_context`
- `corrupt_material_in_live_context`
- `store_error_in_live_context`
- `not_attempted_unsupported_kind`

### `availability_observation`

Exactly one of:

- `observed_in_live_context`
- `not_found_in_live_context`
- `indeterminate_in_live_context`
- `not_observed`

### `retrieval_observation`

Exactly one of:

- `verified_bytes_obtained`
- `unverified_bytes_obtained`
- `not_obtained`
- `not_attempted`

### `integrity_observation`

Exactly one of:

- `verified_exact_identity`
- `failed_exact_identity`
- `not_evaluated`

The first implementation MUST map existing store results exactly as follows:

| Runtime/store result | outcome | availability | retrieval | integrity |
| --- | --- | --- | --- | --- |
| `unsupported_kind` | `not_attempted_unsupported_kind` | `not_observed` | `not_attempted` | `not_evaluated` |
| exact `load_bytes()` success | `exact_observed` | `observed_in_live_context` | `verified_bytes_obtained` | `verified_exact_identity` |
| `ObjectNotFoundError` | `not_found_in_live_context` | `not_found_in_live_context` | `not_obtained` | `not_evaluated` |
| `ObjectCorruptionError` | `corrupt_material_in_live_context` | `indeterminate_in_live_context` | `unverified_bytes_obtained` | `failed_exact_identity` |
| other `ObjectStoreError` | `store_error_in_live_context` | `indeterminate_in_live_context` | `not_obtained` | `not_evaluated` |

For the current store implementation, `ObjectCorruptionError` is raised only after bytes have been read from the exact path; `unverified_bytes_obtained` therefore describes that bounded implementation fact. Decision 023 does not require returning or retaining those bytes.

A custom/non-bundled schema context is rejected before this mapping is entered. It MUST NOT be relabelled as target absence, target corruption, or a generic target-store failure, because Decision 023 has not authorized observation under that interpretation context.

## What a positive observation proves

`exact_observed` establishes only that, during this invocation against the caller-supplied live mutable store:

1. the runtime supported the target kind under Decision 022;
2. the same fixed bundled schema interpretation context governed the exact target load;
3. the exact target path was read;
4. bytes were obtained;
5. those bytes passed the current exact-store UTF-8/JSON/schema/canonical-byte/reference reproduction checks;
6. the requested exact immutable target was therefore observed in that live context.

It does **not** prove provenance causality, source relevance, trust, quality, completeness, closure, packet acceptance, claim closure, integration, epoch completion, future availability, retained-byte availability, literal re-execution, or replay correctness.

## What negative/error observations prove

`not_found_in_live_context` means only that the exact object was not present in that inspected live store invocation. It is not global nonexistence.

`corrupt_material_in_live_context` means material existed at the exact target path but failed the exact immutable identity contract during that invocation. It is not a trust verdict and does not prove that no correct copy exists elsewhere.

`store_error_in_live_context` leaves target availability indeterminate. An unreadable or otherwise failing live store MUST NOT be relabelled as absence.

`not_attempted_unsupported_kind` means the bundled runtime lacked the Decision 022 interpretation contract and target I/O was deliberately skipped. It is not absence or corruption.

A rejected custom schema context means only that this Decision 023 slice does not have authority to make a live-source observation under that caller-selected interpretation context. It is not a statement about target existence, availability, integrity, or trust.

## Retained bytes and snapshot contexts

Decision 021 compared three ways to strengthen continuity:

1. immutable/snapshot-like observation context;
2. retained verified bytes for positive observations;
3. explicit context-bound/non-reexecution standing.

For the first executable slice, option 3 is selected because it is the smallest truthful universal contract.

- Snapshot/context identity is deferred because proving historical negative observations against a frozen store requires additional state-manifest/snapshot machinery not yet grounded in the v0 kernel.
- Retaining verified bytes is deferred because exact-load success can be recorded without duplicating potentially large source payloads. A later retained-byte evidence contract may strengthen future independent verification without changing the meaning of Decision 023 observations.
- The current result therefore records live-context standing and `reexecution_standing = not_established` explicitly.

## Determinism and transport

The returned fact MUST have one deterministic named representation with no positional semantics. Given the same exact occurrence identity and the same classified store outcome, its canonical representation MUST be byte-identical.

Do not include exception strings, absolute paths, hostnames, process ids, timestamps, object iteration order, actor identity, CI metadata, branch names, Git state, or other ambient values in the canonical fact.

## Required implementation evidence

Lane 02 should implement only this decision and add deterministic tests demonstrating at least:

1. exact successful observation;
2. exact not-found observation remains context-bound;
3. corrupt exact-path material maps to the explicit corruption/integrity facts;
4. generic store read failure maps to indeterminate/store-error rather than absence;
5. unsupported kind performs no target-object I/O;
6. equal target refs under distinct declaration occurrences retain distinct occurrence identity;
7. stale or mismatched containing object identity fails closed before observation;
8. no logical/newest/locator/recency fallback occurs;
9. canonical fact transport excludes path/host/process/time/actor/CI/Git authority;
10. repeated identical classified inputs produce identical canonical fact bytes;
11. changing the contents of the same textual store root may truthfully change a later live observation without implying contradiction, because literal re-execution is explicitly not established;
12. Decision 022 regressions remain unchanged and green;
13. a store configured with a custom `schema_dir` fails closed before target-object I/O, so bundled capability classification cannot be combined with caller-selected target-validation semantics.

Explicit compile evidence is required after the full deterministic suite.

## Lane 03 attack surface

After Lane 02 provides an exact tested head, Lane 03 should attack:

- mutable-path laundering into immutable context identity;
- same textual store root with changed contents;
- negative observation globalization;
- unsupported-kind → absence/corruption laundering;
- bundled-capability/custom-schema-context mixing or schema-context substitution;
- hidden logical-id/newest/locator fallback;
- occurrence collapse for equal target refs;
- stale container/declaration-key rebinding;
- corrupt/store-error outcomes disappearing or becoming booleans;
- exception text/path/host/time entering canonical transport;
- retained-byte or exact-load success being laundered into provenance causality/trust/closure/acceptance;
- live observation being laundered into literal re-execution or replay-success authority.

## Explicit non-goals

Decision 023 does not authorize:

- immutable source-store snapshots or snapshot manifests;
- retained source-byte objects;
- caller-selected/custom schema interpretation contexts for source observation;
- generic filesystem/network/URL/package resolvers;
- `content_address` digest verification;
- locator ↔ exact/content association;
- historical source-ref migration;
- provenance-relation vocabulary;
- trust/relevance/quality scoring;
- source completeness/closure;
- dependency/evidence policy;
- packet acceptance/rejection;
- Stage 5 integration receipts/runtime;
- epochs/barriers;
- replay execution or replay-success claims;
- model/agent judgment over source quality.

## Root grounding

**Truth:** runtime capability, schema interpretation context, live-context availability, retrieval, integrity, re-execution standing, trust, closure, and acceptance remain separate facts.

**Agency / non-domination:** no filesystem path, custom schema injection, host, process, actor, founder, specialist, schedule, CI result, branch, recency, or Git permission becomes source authority.

**Continuity:** exact declaration occurrence and explicit failed/uncertain outcomes survive occupant replacement, while the absence of immutable live-context identity and custom-schema authority are recorded rather than hidden.

**Wisdom before speed:** use the smallest honest context-bound observation slice now; defer custom observation contexts, snapshots, byte retention, generic resolution, trust, closure, integration, epochs, and replay until their own contracts are grounded.

## Ownership

**Lane 02:** implement Decision 023 only, on fresh canonical `main`, with deterministic tests and explicit compile evidence.

**Lane 03:** attack the exact tested Lane 02 head using the surface above; do not invent broader source policy.

**Lane 01:** integrate only after evidence is sufficiently grounded against the four roots and preserve all red/uncertain evidence explicitly.
