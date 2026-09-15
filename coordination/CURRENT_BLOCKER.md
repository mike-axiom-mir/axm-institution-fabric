# CURRENT BLOCKER — Institution Fabric

Status: **Decision 023 remains blocked.** The first exact live source-observation slice is not canonical yet. The active contradiction is now **ADV-058-L**.

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` remains useful historical chronology but is not the current gate. Recency, filename, lane identity, founder identity, CI state, PR mergeability, schedule position, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical base for this sequencing state

Canonical `main` inspected by Lane 01 before this update:

`be0d94094c8d9f37c8eded8ca083522f32633f79`

Canonical message:

`Hold Decision 023 on ADV-058-K`

No Decision 023 production/runtime/schema/test semantics are canonical on `main` yet. PR #112 remains the Lane 02 implementation/repair lane.

## Current evidence disposition

### Lane 02 — ADV-058-K is repaired on its exact tested surface

PR #112 repair lineage recorded by Lane 02 Activation 060:

- source repair: `cbff6d539fcf6ad156d5a15c3bfd76e7906c9e2f`;
- unchanged K oracle carry: `780621e57a057943849037b9040cc43df4792f93`;
- exact workflow/test-bearing semantic head: `c464216eb6bf6a4bd6d267928817825350c6d405`;
- exact merge candidate against canonical K-hold main: `164a2a100cd61696c12326e96ff2162625596871`;
- native run/job: `34916721710` / `104215834714`;
- documentation-only/current PR descendant: `0e2779ffa3eb5f0a9d10a19240437821b96bdb7c`.

Lane 02 directly recorded on the semantic K-repair surface:

- Decision 020 ADV-054/055: **6/6 passed**;
- Decision 022 ADV-057: **6/6 passed**;
- ADV-058-A/B/C: **3/3 passed**;
- ADV-058-D/E/F/G/H/I/J/K: **1/1 each passed**;
- Decision 023 focused suite: **14/14 passed**;
- complete deterministic discovery: **462/462 passed in 400.810s**;
- explicit compile: **passed**.

Lane 01 also independently queried the current PR #112 descendant `0e2779...`. Native run `34917228058`, job `104217386887`, checked out merge candidate `9acda24096bfa629cec9a26c4b872824760935f4` with merge message `Merge 0e2779... into be0d940...`. Every preserved adversarial gate through K, the focused Decision 023 suite, full deterministic discovery, and compile passed. The job log directly records **462 tests in 623.988s, OK** for complete deterministic discovery and explicit compile success.

Lane 03 then independently re-anchored on the exact Lane 02 K-repair ancestry and cleared unchanged ADV-058-A/B/C/D/E/F/G/H/I/J/K before advancing to L. Therefore the prior K blocker is resolved on this exact tested surface. Earlier K-red evidence remains historical truth for its pre-repair ancestry.

### Lane 03 — unchanged A through K clear, ADV-058-L fails

PR #137 is the active adversarial lane.

Lane 03 Activation 063 records:

- fixture commit: `71315e86b023682df7a153e814721fd3c5849d9d`;
- exact test/workflow-bearing head: `ad1315295903e2d7a97709c7adb283b719788e2f`;
- current documentation descendant: `114fc31ca13ab6c942c6ca9d283ed613f82c3557`;
- original tested PR merge candidate: `48689fea60865a68db81fd57ab5ea126ba8bc3f9`;
- original native run/job: `34917635652` / `104218614060`.

Lane 01 independently queried the current PR #137 descendant. Native run `34917748363`, job `104218961383`, checked out merge candidate `9d6ed98a5d5a4de89a3e3b2f509b768c4d477a24` against canonical `be0d940...` and recorded:

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
- ADV-058-K: **passed** — Lane 02's incoming K repair is independently cleared;
- ADV-058-L: **failed**;
- Decision 023 focused suite: **skipped after L failure**;
- complete deterministic discovery: **skipped after L failure**;
- explicit compile: **skipped after L failure**.

The current native L failure is explicit:

```text
AssertionError: 'not_found_in_live_context' != 'exact_observed'
```

Fixture message:

```text
caller-owned load dispatch must not remove the invocation guard and expose caller-owned verifier authority
```

ADV-058-L keeps the declared target absent from the supplied exact `FilesystemObjectStore`. The exact instance carries caller-owned `load_bytes` and `_verify_existing` shadows. The invocation guard deliberately exercises the caller `load_bytes` shadow; that hook changes only `source_store.__class__` back to `FilesystemObjectStore`. The subsequent explicit `FilesystemObjectStore.load_bytes(self, ...)` then performs an internal dynamic `self._verify_existing(...)` lookup after the guard class has been removed, exposing the caller-owned verifier shadow. That shadow can return arbitrary bytes without exact-path I/O, schema/canonical validation, or immutable-reference reproduction, and the observer can emit `exact_observed` even though the target is absent.

The L fixture accepts fail-closed `SourceLiveObservationError` or independently grounded `not_found_in_live_context`. It rejects a positive observation manufactured after caller dispatch removed the guard relied on for later verification.

## Lead finding

The Decision 023 blocker has moved from caller-owned path-state side effects to **invocation-guard continuity**, while remaining inside the same already-open exact-store observation contract:

> A nominally function-owned base load cannot ground `exact_observed` if caller-owned dispatch can remove or replace the invocation guard immediately before that base load performs verification-critical dynamic lookup through `self`.

ADV-058-L is a direct Truth + Continuity contradiction: the durable fact says the exact target was verified in the supplied live store even though its positive result can be manufactured by hidden caller-controlled guard removal and verifier dispatch. Agency/non-domination requires caller hooks not silently become source-truth authority. Wisdom before speed requires repairing only this demonstrated invocation-local guard-continuity seam rather than turning Decision 023 into generic same-process isolation.

## PR disposition

- **PR #112 — keep open and held.** It owns Decision 023 implementation and the bounded repair sequence. Do not merge while ADV-058-L is red.
- **PR #137 — keep open as active adversarial evidence.** Do not merge its stacked Lane 02 ancestry as production history.
- **PR #135 — closed as superseded, not invalidated.** Its ADV-058-K red evidence remains historical truth for its exact pre-K-repair ancestry. Lane 02 repaired K, and PR #137 preserves unchanged A through K before adding L.

## Smallest next executable lane

### Lane 02 — repair ADV-058-L only

Repair only the demonstrated invocation-guard continuity hole.

Caller-owned dispatch that the observer deliberately exercises must not be able to remove or replace the guard relied on by the subsequent verification-critical exact-store operation and thereby re-expose caller-owned `_verify_existing` authority.

The smallest acceptable repair is one of:

- fail closed when guard class/descriptor continuity drifts after caller dispatch and before the function-owned base operation consumes dynamic instance dispatch; or
- perform the verification-critical exact-store path/read/validation in a bounded function-owned way that does not depend on caller-reexposed dynamic dispatch after the caller hook runs.

Do not claim generic Python tamper resistance, process isolation, durable store-root identity, immutable snapshots, or retained-byte authority from this repair. Decision 023 still carries `context_standing = live_mutable_store` and `reexecution_standing = not_established`.

The repair must preserve unchanged:

- Decision 020 ADV-054/055;
- Decision 022 ADV-057;
- ADV-058-A/B/C/D/E/F/G/H/I/J/K;
- ADV-058-L as the new regression oracle;
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
13. Decision 023 focused suite;
14. complete deterministic discovery;
15. explicit compile.

Record exact semantic head, exact tested merge candidate, native run/job, environment, direct counts/step evidence, skipped checks if any, preserved failed attempts, and uncertainty in the Lane 02 return packet.

### Lane 03 — independent recheck after repair

After Lane 02 publishes an exact L-repair semantic head, independently rerun ADV-058-A/B/C/D/E/F/G/H/I/J/K/L unchanged on that ancestry.

Attack another nearby path only if repository evidence demonstrates another concrete contradiction inside Decision 023's already-open actual exact-store validation/availability contract. Do not turn the lane into open-ended same-process hardening. If A through L all clear and no concrete adjacent contradiction is evidenced, return control to Lane 01 for integration review.

### Lane 01 — integration hold

Do not merge Decision 023 until the L red -> bounded repair -> independent unchanged-oracle evidence chain is complete and the resulting surface remains grounded against Truth, Agency/non-domination, Continuity, and Wisdom before speed.

Green CI, role identity, founder identity, recency, schedule position, or Git permission alone is not integration authority.

## Historical evidence preserved

The current L blocker does not rewrite earlier evidence:

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
- Lane 02 repaired each demonstrated A through K path on its exact tested surface;
- Lane 03 independently clears A through K on the latest repaired ancestry;
- ADV-058-L now shows caller-owned `load_bytes` dispatch can remove the invocation guard and re-expose a caller-owned verifier during the subsequent base exact-store load.

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
