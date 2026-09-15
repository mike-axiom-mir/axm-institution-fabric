# CURRENT BLOCKER — Institution Fabric

Status: **Decision 023 remains blocked.** The first exact live source-observation slice is not canonical yet. The active contradiction is now **ADV-058-P**.

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` remains useful historical chronology but is not the current gate. Recency, filename, lane identity, founder identity, CI state, PR mergeability, schedule position, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical base for this sequencing state

Canonical `main` inspected by Lane 01 before this update:

`54ea2c31d899a6af62af9e1a74333662b4727ee9`

Canonical message:

`Hold Decision 023 on ADV-058-O`

No Decision 023 production/runtime/schema/test semantics are canonical on `main` yet. PR #112 remains the Lane 02 implementation/repair lane.

## Current evidence disposition

### Lane 02 — ADV-058-O is repaired on its exact tested surface

PR #112 Lane 02 Activation 064 records:

- exact source repair commit: `d2a214d87b4dfb57d7d2d0718001e566219b92a0`;
- exact semantic/test/workflow-bearing head: `9b33a21874eec89a040c08b333fd1fae4b96366d`;
- exact tested merge candidate against canonical O-hold main: `172f74b6bc89023696d1bbac13a313620fbe6c10`;
- native run/job: `34931852086` / `104261519011`;
- environment: Ubuntu 24.04.5 LTS, CPython 3.12.14, jsonschema 4.26.0;
- documentation-only descendant / current PR #112 head at Lane 01 inspection: `f99763f9db3978e6245dea8e4c8b0df6e7af8316`.

Lane 02 directly recorded on the O-repair surface:

- Decision 020 ADV-054/055: **6/6 passed**;
- Decision 022 ADV-057: **6/6 passed**;
- ADV-058-A/B/C: **3/3 passed**;
- ADV-058-D/E/F/G/H/I/J/K/L/M/N/O: **1/1 each passed**;
- Decision 023 focused suite: **14/14 passed**;
- complete deterministic discovery: **466/466 passed in 612.438s**;
- explicit compile: **passed**;
- no required step skipped.

The bounded O repair keeps caller-owned exact-instance `load_bytes` dispatch from becoming authority for `corrupt_material_in_live_context` / `failed_exact_identity`: caller-raised `ObjectCorruptionError` is no longer sufficient; the function-owned base exact-store load independently determines presence/integrity. Actual function-owned corruption classification remains unchanged.

Lane 01 independently queried current PR #112 descendant `f99763f9...`. Native run `34932658108`, job `104263943279`, completed Decision 020, Decision 022, every preserved adversarial gate through ADV-058-O, the focused Decision 023 suite, complete deterministic discovery, and compile successfully. This confirms that the current PR #112 descendant still carries the O repair without regression on the recorded gate sequence.

Lane 03 then independently re-anchored on exact Lane 02 O-repair semantic/test/workflow head `9b33a218...` and cleared unchanged ADV-058-A/B/C/D/E/F/G/H/I/J/K/L/M/N/O before advancing to P. Therefore the prior O blocker is resolved on this exact tested surface. Earlier O-red evidence remains historical truth for its pre-repair ancestry.

### Lane 03 — unchanged A through O clear, ADV-058-P fails

PR #145 is the active adversarial lane.

Lane 03 Activation 067 records:

- exact Lane 02 O-repair semantic/test/workflow head attacked: `9b33a21874eec89a040c08b333fd1fae4b96366d`;
- exact Lane 03 test/workflow-bearing head: `e8e006e6c4e0317bcb3d5ea72c25d187f00dd7ae`;
- exact tested pull-request merge candidate: `f6f4da9ee8e4bda35bacb8b0f8b3c3a843fd0c82`;
- original native run/job: `34933079361` / `104265183205`;
- documentation descendant / current PR #145 head at Lane 01 inspection: `d0388f6a18d513210853d4b4354f35a846e5b41b`.

Lane 01 independently queried the current PR #145 descendant. Native run `34933255094`, job `104265701464`, records:

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
- ADV-058-L: **passed**;
- ADV-058-M: **passed**;
- ADV-058-N: **passed**;
- ADV-058-O: **passed** — Lane 02's incoming O repair is independently cleared;
- ADV-058-P: **failed**;
- Decision 023 focused suite: **skipped after P failure**;
- complete deterministic discovery: **skipped after P failure**;
- explicit compile: **skipped after P failure**.

The current PR #145 native log records the exact failure:

```text
AssertionError: 'corrupt_material_in_live_context' == 'corrupt_material_in_live_context' : caller-owned verifier dispatch must not forge material corruption
```

ADV-058-P keeps the exact target genuinely present and canonical in the supplied exact `FilesystemObjectStore`. Only caller-owned exact-instance `_verify_existing` dispatch raises a forged `ObjectCorruptionError`; it performs no target I/O and mutates no schema or store-location state. The current verifier guard neutralizes caller-owned not-found but not caller-owned corruption, so the corruption exception can escape before the function-owned `FilesystemObjectStore._verify_existing(...)` independently reads/reproduces exact identity. The outer observer can then emit `corrupt_material_in_live_context` / `failed_exact_identity` solely from caller-owned verifier dispatch.

The P fixture accepts fail-closed `SourceLiveObservationError`, an independently grounded `exact_observed`, or conservative `store_error_in_live_context` / indeterminate handling. It rejects material-corruption or failed-identity facts manufactured solely from caller-owned verifier pre-dispatch.

## Lead finding

The Decision 023 blocker has moved one layer deeper on the same already-open corruption-classification boundary:

> A durable `corrupt_material_in_live_context` / `failed_exact_identity` fact must be grounded in corruption independently observed by the function-owned exact-store verifier, not merely in an exception subtype raised by caller-owned `_verify_existing` pre-dispatch.

ADV-058-P is a direct Truth + Continuity contradiction: the durable fact can say the supplied exact source failed identity verification while the actual exact bytes in that supplied store remain valid. Agency/non-domination requires caller-owned exception choice not silently become source-truth authority. Wisdom before speed requires repairing only this demonstrated verifier corruption-classification seam rather than turning Decision 023 into generic same-process isolation.

## PR disposition

- **PR #112 — keep open and held.** It owns Decision 023 implementation and the bounded repair sequence. Do not merge while ADV-058-P is red.
- **PR #145 — keep open as active adversarial evidence.** Do not merge its stacked Lane 02 ancestry as production history.
- **PR #143 — closed as superseded, not invalidated.** Its ADV-058-O red evidence remains historical truth for its exact pre-O-repair ancestry. Lane 02 repaired O, and PR #145 preserves unchanged A through O before adding P.

## Smallest next executable lane

### Lane 02 — repair ADV-058-P only

Repair only the demonstrated caller-owned verifier corruption-error authority.

The smallest acceptable repair is to ensure caller-owned `_verify_existing` pre-dispatch cannot by itself establish `corrupt_material_in_live_context` / `failed_exact_identity` before the function-owned `FilesystemObjectStore._verify_existing(...)` path observes corruption. A bounded implementation may:

- ignore caller-only verifier corruption and continue through the function-owned base verifier, analogously to the already-grounded caller-only not-found handling; or
- conservatively fail closed / classify caller interference as indeterminate while reserving material-corruption / failed-identity facts for corruption independently produced by the function-owned verifier.

Do not weaken actual base-store corruption detection. Do not claim generic Python tamper resistance, process isolation, durable store-root identity, immutable snapshots, or retained-byte authority from this repair. Decision 023 still carries `context_standing = live_mutable_store` and `reexecution_standing = not_established`.

The repair must preserve unchanged:

- Decision 020 ADV-054/055;
- Decision 022 ADV-057;
- ADV-058-A/B/C/D/E/F/G/H/I/J/K/L/M/N/O;
- ADV-058-P as the new regression oracle;
- the exact accepted store boundary;
- fixed bundled schema interpretation context;
- context-local not-found semantics;
- separate availability/retrieval/integrity dimensions;
- exact declaration occurrence identity;
- unsupported-kind no-target-I/O behavior;
- generic store-error indeterminacy;
- actual function-owned base-store corruption detection.

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
14. ADV-058-N unchanged;
15. ADV-058-O unchanged;
16. ADV-058-P unchanged;
17. Decision 023 focused suite;
18. complete deterministic discovery;
19. explicit compile.

Record exact semantic head, exact tested merge candidate, native run/job, environment, direct counts/step evidence, skipped checks if any, preserved failed attempts, and uncertainty in the Lane 02 return packet.

### Lane 03 — independent recheck after repair

After Lane 02 publishes an exact P-repair semantic/test head, independently rerun ADV-058-A/B/C/D/E/F/G/H/I/J/K/L/M/N/O/P unchanged on that ancestry.

Attack another nearby path only if repository evidence demonstrates another concrete contradiction inside Decision 023's already-open supplied-store observation contract. Do not turn the lane into open-ended same-process hardening. If A through P all clear and no concrete adjacent contradiction is evidenced, return control to Lane 01 for integration review.

### Lane 01 — integration hold

Do not merge Decision 023 until the P red -> bounded repair -> independent unchanged-oracle evidence chain is complete and the resulting surface remains grounded against Truth, Agency/non-domination, Continuity, and Wisdom before speed.

Green CI, role identity, founder identity, recency, schedule position, or Git permission alone is not integration authority.

## Historical evidence preserved

The current P blocker does not rewrite earlier evidence:

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
- ADV-058-M exposed caller-owned `_verify_existing` dispatch removing the invocation guard and re-exposing caller-owned `_object_path` authority during the subsequent base verifier;
- ADV-058-N exposed caller-controlled location equality/path-composition semantics masking `objects_dir` drift and redirecting the subsequent base path into another store root;
- ADV-058-O exposed caller-owned `load_bytes` corruption-error choice manufacturing material-corruption / failed-identity without function-owned corruption evidence;
- Lane 02 repaired each demonstrated A through O path on its exact tested surface;
- Lane 03 independently clears A through O on the latest repaired ancestry;
- ADV-058-P now shows caller-owned `_verify_existing` corruption-error choice can manufacture material-corruption / failed-identity before the function-owned verifier grounds exact identity.

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
