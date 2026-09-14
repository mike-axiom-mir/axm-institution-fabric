# Decision 021 — Research Disposition

Date: 2026-09-14
Status: **bounded research conclusion recorded; exact target-availability observation remains blocked, while one smaller deterministic precursor is grounded enough to open as Decision 022.**

Decision 021 asked for the smallest universal source-observation boundary that could follow Decision 020 without collapsing declaration identity, availability, retrieval, integrity, association, trust, closure, or acceptance.

## Evidence integrated during the research gate

Lane 02 PR #98 is canonical as commit `40ec96a004e264826e4954a94d4d0ea4d8c7f784`. It adds one Decision 020 compatibility regression proving that a canonical `exact_axm_object` declaration remains valid even when its target kind is not supported by the current runtime. Its final PR merge candidate ran the existing ADV-054/ADV-055 oracle 6/6 green, the full deterministic suite 417/417 green, and explicit compile successfully. No production semantics changed.

Lane 03 PR #99 is canonical as commit `fdab2549c93cd6e7ff679ae1f16689acbc3aad69`. It adds ADV-056-A through L as research counterexamples only. In particular it preserves two constraints that must be addressed before an exact target observer can truthfully claim more:

1. a mutable filesystem store-root/path label is not an immutable replay context by itself;
2. implementation-level work deduplicated by `object_ref` must not erase Decision 020 declaration-occurrence identity (`exact containing object identity + declaration key`).

## Existing exact-load primitives actually available

`FilesystemObjectStore.load()` / `load_bytes()` already provide a strong exact path once runtime support is available:

- parse the exact `axmref:v1` identity;
- derive the exact content-addressed path;
- read only that path;
- strict-parse JSON;
- validate with the inferred `<kind>.schema.json` contract;
- reproduce canonical bytes;
- reproduce the exact requested immutable reference;
- never fall back by logical id, newest version, locator, recency, actor, branch, or store order.

The store also distinguishes exact-path absence (`ObjectNotFoundError`), stored-byte/identity corruption (`ObjectCorruptionError`), reference/schema mismatch (`ObjectReferenceMismatchError`), and other store I/O failure (`ObjectStoreError`).

## What Decision 020 can expose without reinterpretation

Artifact v0.4 and evidence-record v0.2 can expose typed source declarations while retaining declaration occurrence identity as:

`exact containing object identity + declaration key`.

For `exact_axm_object`, the declared target is a canonical immutable AXM reference only. Declaration validation deliberately does not load the target. Historical source strings remain opaque and do not enter this boundary.

## Research blocker 1 — runtime capability is a separate truth dimension

The current store infers `<kind>.schema.json` only after parsing the exact ref. Inside `_verify_existing()`, the exact object path is read before schema validation. This creates an important ordering fact:

- unsupported kind + absent exact path can surface `ObjectNotFoundError` before runtime schema support is examined;
- unsupported kind + present bytes can later be mapped through contract failure into `ObjectCorruptionError`.

Neither outcome is sufficient to say that the target is simply absent or corrupt as a source fact, because the runtime first lacks a supported interpretation contract for that kind.

Therefore **runtime/schema capability standing must be explicit before target availability is classified**.

## Research blocker 2 — live store path is not immutable observation context

`FilesystemObjectStore` is configured by a mutable filesystem root. The same root text can truthfully produce different exact-target observations at different times as objects are published or external state changes.

Therefore the first exact target-availability observer must not call a root path an immutable replay context. One of two later contracts is required:

- a stronger immutable/snapshot-like observation context identity; or
- an explicit result standing that says observation re-execution from the recorded context is **not established**.

This is separate from deterministic institutional replay. A later immutable observation record may be replayed as historical input to downstream state transitions without implying that the original live filesystem state can be reconstructed and re-observed. **Institution replay and observation re-execution are distinct claims.**

## Missing/corrupt/unreadable/unsupported preservation

ADV-056 establishes the minimum future truth boundary:

- unsupported runtime/schema context cannot be collapsed into target absence;
- exact-path absence is context-bound, not global nonexistence;
- corrupt bytes are storage/integrity observations, not trust verdicts;
- unreadable store state remains unknown/error, not absence;
- failed observation attempts cannot disappear from durable results;
- successful exact load may establish several bounded technical facts but does not imply provenance causality, trust, relevance, closure, acceptance, integration, epoch completion, or replay correctness.

## Context/occurrence identity conclusion

A later exact target observer must preserve, at minimum:

- exact containing object identity;
- declaration key;
- exact authored target ref;
- explicit observation method/context standing;
- explicit per-occurrence outcome, including failed outcomes;
- explicit runtime capability standing separate from availability.

Operational caching may reuse work by exact target ref, but durable results must remain attributable to each authored declaration occurrence.

## Offline boundary

The first source-observation path remains local/offline. No network, URL, package, filesystem-locator, search, or model resolver is authorized. `opaque_label`, `content_address`, and `locator` remain declaration facts only.

## Research conclusion

The originally proposed direct exact-target availability projection is **not yet grounded enough to implement** because runtime capability and replay-context standing would otherwise be silently entangled with store outcomes.

One smaller deterministic precursor is grounded: expose **kernel-bundled runtime capability facts for exact AXM source declaration occurrences without reading the target object path**. That precursor is opened separately as Decision 022.

Decision 022 does not close the broader Decision 021 problem. After the capability boundary is tested adversarially, Lane 01 must return to the remaining observation-context question before authorizing exact target availability/retrieval observations.

## Rejected shortcuts

- classify bare `ObjectNotFoundError` as global source absence;
- classify contract failure for an unsupported kind as source corruption/trust failure;
- record only a mutable store root and call the observation replayable;
- key durable observations only by `object_ref`;
- omit failed observations;
- infer source associations from adjacency, key similarity, order, recency, actor, CI, branch, or Git state;
- treat successful exact load as trust, closure, acceptance, integration, epoch completion, or replay correctness;
- open generic resolver/network behavior before the deterministic local boundary is proven.

## Root grounding

- **Truth:** runtime support, context-bound availability, retrieval, integrity, provenance relation, trust, closure, and acceptance remain separate facts.
- **Agency / non-domination:** no host, path, resolver, actor, founder, lane, schedule, CI result, branch, recency, or Git permission becomes source authority.
- **Continuity:** exact declaration occurrence and failed/uncertain states remain recoverable; the repository now records why a mutable path cannot silently stand in for replay context.
- **Wisdom before speed:** open the smaller capability precursor first and keep target observation, generic resolution, trust, closure, Stage 5, epochs, and replay unopened until their truth boundaries are grounded.
