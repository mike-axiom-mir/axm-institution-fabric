# Current Stage 4 Sequencing Overlay

Date: 2026-09-14
Current canonical base before this Lane 01 coordination branch: **`fdab2549c93cd6e7ff679ae1f16689acbc3aad69`**
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current bounded gate: **Decision 022 — Exact Source Runtime Capability Facts**
Current disposition: **Decision 020 remains canonical. Decision 021 research found that direct exact-target availability observation is not yet safe because runtime/schema capability and mutable observation context would otherwise be conflated with store outcomes. Lane 02 may now implement only Decision 022's no-target-I/O capability projection. Exact target availability/retrieval observation remains held.**

`coordination/CURRENT_WAVE.md` is historical chronology. This overlay must be read with Decisions 020–022, newest commits/PRs/branches, and durable Lane 01/02/03 return packets.

## Canonical source-declaration boundary

Decision 020 provides exactly four typed source declaration classes for new artifact/evidence versions:

- `opaque_label`;
- `exact_axm_object`;
- `content_address`;
- `locator`.

Historical `source_refs[]` strings retain their authored opaque meaning. Declaration occurrence identity remains:

`exact containing object identity + declaration key`.

A declaration establishes target identity syntax only at its class's bounded strength. It does not establish target existence, retrieval, integrity, causal provenance, trust, relevance, completeness, closure, acceptance, integration, epoch completion, or replay correctness.

## New canonical specialist evidence

### Lane 02 PR #98 — integrated

PR #98 was squash-merged as:

`40ec96a004e264826e4954a94d4d0ea4d8c7f784`

It adds one Decision 020 compatibility regression only: artifact v0.4 and evidence-record v0.2 must continue to accept a canonical `exact_axm_object` reference whose kind is not supported by the current bundled runtime.

Lane 01 directly inspected the final PR merge-candidate run for head `289f0d3f6224adb1dc3f441ac8fd9ab7595134c8`:

- merge candidate: `819e428b02905bae2656ad1f61179037377a92d1`;
- GitHub Actions run/job: `34822965145` / `103908500098`;
- Python 3.12.14 / jsonschema 4.26.0;
- unchanged ADV-054/ADV-055 source oracle: **6/6 passed**;
- full deterministic suite: **417/417 passed** in 613.944s;
- explicit enumerated `py_compile`: **passed**;
- complete job: **success**.

This freezes only the syntax/runtime-support separation. It adds no source observer or resolver.

### Lane 03 PR #99 — integrated

PR #99 was squash-merged as:

`fdab2549c93cd6e7ff679ae1f16689acbc3aad69`

It adds research evidence only: ADV-056-A through L plus Lane 03 Activation 047. No production Python, schema, existing test, workflow, resolver, loader, integrity executor, association mechanism, trust/closure rule, acceptance behavior, Stage 5 integration, epoch, or replay behavior changed.

The strongest constraints are now canonical research state:

1. a mutable store-root/path label is not immutable replay context by itself;
2. exact target work cached/deduplicated by `object_ref` must not erase exact declaration-occurrence attribution;
3. unsupported runtime capability must stay separate from target absence/corruption;
4. corrupt, unreadable, missing, and failed observations must not disappear or become trust verdicts;
5. parallel contradictory context-bound observations gain no newest/actor/CI/branch/Git authority;
6. neighboring exact/content/locator declarations remain unassociated;
7. observation success cannot become trust/closure/acceptance/integration/replay authority.

## Decision 021 research disposition

`coordination/decisions/021_RESEARCH_DISPOSITION.md` records the bounded conclusion.

Existing `FilesystemObjectStore.load()` / `load_bytes()` are exact and deterministic once the runtime has a supported schema for the target kind. They parse the exact ref, derive one exact content-addressed path, strict-parse, validate, reproduce canonical bytes and exact identity, and provide no logical-id/newest/locator fallback.

But `_verify_existing()` reads the exact object path before schema validation. Therefore:

- unsupported kind + absent path can surface `ObjectNotFoundError` before schema support is tested;
- unsupported kind + present bytes can later be mapped through contract failure into `ObjectCorruptionError`.

Those outcomes cannot truthfully be interpreted as plain source absence/corruption until runtime capability is established separately.

The store root is also a mutable filesystem location rather than an immutable snapshot identity. Exact target availability/retrieval observation therefore remains held until Lane 01 later resolves whether the observation context gets a stronger immutable identity or an explicit non-reexecution/replay limitation.

Institutional replay of a durable historical observation record is not the same claim as re-executing the original live source observation. Keep those claims separate.

## Decision 022 — active implementation gate

Decision 022 opens only a deterministic **kernel-bundled runtime capability projection** for one Decision 020 `exact_axm_object` declaration occurrence.

The result must preserve named facts equivalent to:

- exact `containing_object_ref`;
- exact `declaration_key`;
- exact `target_object_ref`;
- parsed `target_kind`;
- `runtime_capability = supported | unsupported_kind`.

The first slice is limited to the bundled kernel schema context. Custom/mutable schema directories remain outside the contract.

The projection must verify the exact containing object and declaration occurrence, parse the target ref through Stage 2, and determine whether the bundled kernel has a valid schema for that target kind.

**It must not read the source target object's content-addressed path.**

`supported` means only that the current bundled deterministic kernel has an interpretation contract for the target kind. `unsupported_kind` means only that this bundled kernel does not. Neither state proves target existence, absence, retrieval, integrity, trust, relevance, closure, acceptance, integration, epoch completion, or replay correctness.

If a bundled schema exists but is itself unreadable/invalid, that is a kernel/runtime configuration failure and must fail closed rather than becoming `unsupported_kind` or source corruption.

## Active lane boundaries

### Lane 01 — sequencing / integration

Decision 021 research disposition is now durable. Do not implement the target observer in parallel with Lane 02. Review and integrate Decision 022 only after exact implementation/test evidence and Lane 03 adversarial evidence are available.

### Lane 02 — active implementation owner

Implement **Decision 022 only** on fresh canonical `main`:

- exact containing-object + declaration-key occurrence binding;
- bundled-kernel schema capability classification;
- no source target object-path read;
- no custom schema context;
- no resolver, availability, retrieval, integrity, trust, closure, acceptance, Stage 5, epoch, or replay semantics;
- deterministic tests and explicit compile.

### Lane 03 — adversarial next after Lane 02 tested head

Attack Decision 022 for target-path leakage, unsupported-kind laundering, same-target occurrence collapse, stale-container rebinding, order/recency authority, non-exact source promotion, ambient/custom schema injection, invalid bundled-schema misclassification, named transport drift, and capability→existence/trust/closure/acceptance laundering.

Do not weaken the oracle after seeing implementation.

## Still explicitly unresolved

- immutable/snapshot-like source observation context identity or explicit observation re-execution limitation;
- exact target availability/existence observation;
- source target loading/retrieval semantics;
- source bytes retention;
- integrity-check execution and retained integrity evidence;
- locator/network/filesystem/package resolvers;
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
- cross-language graph/reachability/frontier/source reproduction;
- exact self/mutual-cycle authorability through ordinary content-addressed publication;
- stronger filesystem durability/concurrency evidence;
- hostile same-process code isolation beyond the trusted deterministic runtime boundary.

## Four-root gate

- **Truth:** runtime capability is now explicitly separated from source availability, corruption, trust, and acceptance; mutable store context is not mislabeled replay identity.
- **Agency / non-domination:** no founder, lane, runtime host, path, actor, CI, branch, schedule, recency, or Git permission becomes source or merge authority.
- **Continuity:** the Decision 020 compatibility guard, ADV-056 counterexamples, research blocker, and next executable boundary are durable outside private chat.
- **Wisdom before speed:** implement the no-target-I/O capability precursor before exact target observation, generic resolvers, integrity execution, trust, closure, Stage 5, epochs, or replay.
