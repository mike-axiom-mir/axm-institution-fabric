# CURRENT BLOCKER — Institution Fabric

Status: **Decision 023 remains blocked.** The first exact live source-observation slice is not canonical yet. The active contradiction is now **ADV-058-M**.

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` remains useful historical chronology but is not the current gate. Recency, filename, lane identity, founder identity, CI state, PR mergeability, schedule position, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical base for this sequencing state

Canonical `main` inspected by Lane 01 before this update:

`d35cfbe117c734f2f7198c63af72c6c8459c9115`

Canonical message:

`Hold Decision 023 on ADV-058-L`

No Decision 023 production/runtime/schema/test semantics are canonical on `main` yet. PR #112 remains the Lane 02 implementation/repair lane.

## Current evidence disposition

### Lane 02 — ADV-058-L is repaired on its exact tested surface

PR #112 Lane 02 Activation 061 records:

- source repair: `bfbb56bfd0f39389edc09e421e7d92ae84e4f3db`;
- unchanged L oracle carry: `4485c84661977bebd7df15ac086d4fd23ac28b6a`;
- exact test/workflow-bearing head: `3ab40df5e83deb2baa3a1c765b322f9882bc654f`;
- exact tested merge candidate against canonical L-hold main: `ae0ec32a97c7e5cc54f06c0b76e4840fc9105199`;
- native run/job: `34920489229` / `104227300099`;
- documentation/current PR descendant: `d07a17dfd2f783061aeb167f2578665b18d04ad9`.

Lane 02 directly recorded on the L-repair surface:

- Decision 020 ADV-054/055: **6/6 passed**;
- Decision 022 ADV-057: **6/6 passed**;
- ADV-058-A/B/C: **3/3 passed**;
- ADV-058-D/E/F/G/H/I/J/K/L: **1/1 each passed**;
- Decision 023 focused suite: **14/14 passed**;
- complete deterministic discovery: **463/463 passed in 610.781s**;
- explicit compile: **passed**.

Lane 01 independently queried the current PR #112 descendant `d07a17df...`. Native run `34921243139`, job `104229645779`, completed every preserved adversarial gate through L, the focused Decision 023 suite, complete deterministic discovery, and compile successfully. This independently confirms that the current PR #112 descendant still carries the L repair without regression on the recorded gate sequence.

Lane 03 then independently re-anchored on the exact Lane 02 L-repair ancestry and cleared unchanged ADV-058-A/B/C/D/E/F/G/H/I/J/K/L before advancing to M. Therefore the prior L blocker is resolved on this exact tested surface. Earlier L-red evidence remains historical truth for its pre-repair ancestry.

### Lane 03 — unchanged A through L clear, ADV-058-M fails

PR #139 is the active adversarial lane.

Lane 03 Activation 064 records:

- Lane 02 L-repair production commit attacked: `bfbb56bfd0f39389edc09e421e7d92ae84e4f3db`;
- exact Lane 02 semantic/test/workflow head attacked: `3ab40df5e83deb2baa3a1c765b322f9882bc654f`;
- exact Lane 03 original test/workflow-bearing head: `f2ecf2317976b80e173be025adef2b8422602f86`;
- exact original tested merge candidate: `dc0f86c40dbc94edbba24835b2d22722417b4e17`;
- original native run/job: `34921247872` / `104229660215`;
- current PR documentation descendant: `3d91ed2f7c4645410c50ea5e3f6e325beb973f16`.

Lane 01 independently queried the current PR #139 descendant. Native run `34921402639`, job `104230134126`, records:

- Decision 020 adversarial gate: **passed**;
- Decision 022 adversarial gate: **passed**;
- ADV-058-A/B/C: **passed**;
- ADV-058-D: **passed**;
- ADV-058-E: **passed**;
- ADV-058-F: **passed**;
- ADV-058-G: **passed**;
- ADV-058-H: **passed**;
- ADV-058-I: **passed**;
- ADV-058-J: **passed**;
- ADV-058-K: **passed**;
- ADV-058-L: **passed** — Lane 02's incoming L repair is independently cleared;
- ADV-058-M: **failed**;
- Decision 023 focused suite: **skipped after M failure**;
- complete deterministic discovery: **skipped after M failure**;
- explicit compile: **skipped after M failure**.

Lane 03's original native M reproduction records the exact failure:

```text
AssertionError: 'not_found_in_live_context' != 'exact_observed'
```

Fixture message:

```text
caller-owned verifier dispatch must not remove the invocation guard and expose caller-owned path authority
```

ADV-058-M keeps the declared target absent from the supplied exact `FilesystemObjectStore`; a separate decoy store contains the exact canonical target bytes. The supplied instance carries caller-owned `_verify_existing` and `_object_path` shadows. The guarded verifier deliberately exercises caller `_verify_existing`; that hook changes only `source_store.__class__` back to `FilesystemObjectStore`, removing `_InvocationSchemaGuard`. The subsequent explicit base `FilesystemObjectStore._verify_existing(self, ...)` then dynamically resolves `self._object_path(...)` after the guard has disappeared, exposing caller-owned path dispatch. That path shadow imports the decoy target, allowing canonical/schema/reference verification to succeed on external bytes and the observer to emit `exact_observed` even though the target is absent from the supplied store root.

The M fixture accepts fail-closed `SourceLiveObservationError` or independently grounded `not_found_in_live_context`. It rejects positive observation manufactured after caller verifier dispatch removed the guard relied on by the base verifier's path lookup.

## Lead finding

The Decision 023 blocker has moved from load-stage invocation-guard continuity to **verifier-stage invocation-guard continuity**, while remaining inside the same already-open exact-store observation contract:

> A nominally function-owned base verifier cannot ground `exact_observed` if caller-owned verifier dispatch can remove or replace the invocation guard immediately before that base verifier performs verification-critical dynamic path lookup through `self`.

ADV-058-M is a direct Truth + Continuity contradiction: the durable fact says the exact target was verified in the supplied live store even though its positive result can be manufactured by hidden caller-controlled guard removal and path redirection to another root. Agency/non-domination requires caller hooks not silently become source-truth authority. Wisdom before speed requires repairing only this demonstrated verifier-stage guard-continuity seam rather than turning Decision 023 into generic same-process isolation.

## PR disposition

- **PR #112 — keep open and held.** It owns Decision 023 implementation and the bounded repair sequence. Do not merge while ADV-058-M is red.
- **PR #139 — keep open as active adversarial evidence.** Do not merge its stacked Lane 02 ancestry as production history.
- **PR #137 — closed as superseded, not invalidated.** Its ADV-058-L red evidence remains historical truth for its exact pre-L-repair ancestry. Lane 02 repaired L, and PR #139 preserves unchanged A through L before adding M.

## Smallest next executable lane

### Lane 02 — repair ADV-058-M only

Repair only the demonstrated verifier-stage invocation-guard continuity hole.

After caller-owned `_verify_existing` dispatch is deliberately exercised, the verification-critical base verifier must not proceed with a removed/replaced `_InvocationSchemaGuard` such that its dynamic `self._object_path(...)` lookup re-exposes caller-owned path authority.

The smallest acceptable repair is one of:

- restore/check the exact invocation guard after caller `_verify_existing` dispatch and before the base verifier performs dynamic path lookup, failing closed if guard continuity cannot be re-established; or
- perform the exact verification-critical base path/read/validation in a bounded function-owned way that does not depend on caller-reexposed instance path dispatch after the caller verifier hook runs.

Do not claim generic Python tamper resistance, process isolation, durable store-root identity, immutable snapshots, or retained-byte authority from this repair. Decision 023 still carries `context_standing = live_mutable_store` and `reexecution_standing = not_established`.

The repair must preserve unchanged:

- Decision 020 ADV-054/055;
- Decision 022 ADV-057;
- ADV-058-A/B/C/D/E/F/G/H/I/J/K/L;
- ADV-058-M as the new regression oracle;
- the exact accepted store boundary;
- fixed bundled schema interpretation context;
- context-local not-found semantics;
- separate availability/retrieval/integrity dimensions;
- exact declaration occurrence identity;
- unsupported-kind no-target-I/O behavior;
- generic store-error indeterminacy.

Required evidence after repair, in order:

1. Decision 020 ADV-054/055 unchanged;
2. Decision 022 ADV-057 unchanged;
3. ADV-058-A/B/C unchanged;
4. ADV-058-D unchanged;
5. ADV-058-E unchanged;
6. ADV-058-F unchanged;
7. ADV-058-G unchanged;
8. ADV-058-H unchanged;
9. ADV-058-I unchanged;
10. ADV-058-J unchanged;
11. ADV-058-K unchanged;
12. ADV-058-L unchanged;
13. ADV-058-M unchanged;
14. Decision 023 focused suite;
15. complete deterministic discovery;
16. explicit compile.

Record exact semantic head, exact tested merge candidate, native run/job, environment, direct counts/step evidence, skipped checks if any, preserved failed attempts, and uncertainty in the Lane 02 return packet.

### Lane 03 — independent recheck after repair

After Lane 02 publishes an exact M-repair semantic head, independently rerun ADV-058-A/B/C/D/E/F/G/H/I/J/K/L/M unchanged on that ancestry.

Attack another nearby path only if repository evidence demonstrates another concrete contradiction inside Decision 023's already-open actual exact-store validation/availability contract. Do not turn the lane into open-ended same-process hardening. If A through M all clear and no concrete adjacent contradiction is evidenced, return control to Lane 01 for integration review.

### Lane 01 — integration hold

Do not merge Decision 023 until the M red -> bounded repair -> independent unchanged-oracle evidence chain is complete and the resulting surface remains grounded against Truth, Agency/non-domination, Continuity, and Wisdom before speed.

Green CI, role identity, founder identity, recency, schedule position, or Git permission alone is not integration authority.

## Historical evidence preserved

The current M blocker does not rewrite earlier evidence:

- ADV-058-A exposed bundled-schema substitution between capability classification and observation;
- ADV-058-B exposed caller-owned validation-context rebind/restore;
- ADV-058-C exposed exact-instance `load_bytes` replacement despite exact class identity;
- ADV-058-D exposed direct `store.__dict__['schema_dir']` rebinding around validation;
- ADV-058-E exposed caller-owned `load_bytes` success being accepted without actual exact-store verification;
- ADV-058-F exposed base `load_bytes` delegating verification through caller-shadowable `_verify_existing`;
- ADV-058-G exposed caller-shadowable `_object_path` return values importing presence from another root;
- ADV-058-H exposed caller-shadowable `_object_path` errors manufacturing false context-local absence;
- ADV-058-I exposed caller-owned exact-instance `load_bytes` errors manufacturing false context-local absence before the base exact-store read;
- ADV-058-J exposed caller-owned exact-instance `_verify_existing` errors manufacturing false context-local absence before the base verifier;
- ADV-058-K exposed caller-owned `_object_path` side effects mutating `store.objects_dir` before the base path consumed it and importing presence from another store root;
- ADV-058-L exposed caller-owned `load_bytes` dispatch removing the invocation guard before the base loader dynamically resolved `_verify_existing`;
- Lane 02 repaired each demonstrated A through L path on its exact tested surface;
- Lane 03 independently clears A through L on the latest repaired ancestry;
- ADV-058-M now shows caller-owned `_verify_existing` dispatch can remove the invocation guard and re-expose caller-owned `_object_path` authority during the subsequent base verifier.

Each red remains valid for its exact pre-repair ancestry. Each green remains valid for its exact tested repaired surface. Neither class of evidence erases the other.

## Unresolved boundary — still explicitly unopened

Decision 023 does not establish:

- general hostile same-process code isolation;
- durable identity for the live store root;
- immutable/snapshot-like source-observation context identity or completeness;
- retained verified source bytes;
- custom/non-bundled observation-context identity/configuration;
- content-address byte-provider/digest-verification semantics;
- locator/network/filesystem/package resolver contracts and resolver identity;
- locator/content/exact association;
- historical-to-typed migration objects;
- provenance-relation vocabulary;
- source trust, quality, relevance, completeness, or closure;
- dependency admissibility/satisfaction/closure;
- evidence-method/source-quality precedence or invalidation dominance;
- packet acceptance/rejection and durable closure;
- claim closure;
- successor state-revision publication;
- Stage 5 integration receipts/runtime;
- epochs/barriers;
- replay or literal reexecution authority;
- cross-language source-observation reproduction;
- stronger filesystem durability/concurrency guarantees.

These remain future decisions/evidence obligations, not implied semantics.

## Current v0 position

Institution Fabric remains in bounded Stage 4 source-fact work needed before later integration/replay claims can be truthful. The deterministic-kernel direction is unchanged: explicit typed facts first, then immutable integration/replay only after their input meaning is grounded. Model-heavy autonomy remains out of scope.
