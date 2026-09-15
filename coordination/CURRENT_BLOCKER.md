# CURRENT BLOCKER — Institution Fabric

Status: **Decision 023 remains blocked.** The first exact live source-observation slice is not canonical yet. The active contradiction is now **ADV-058-K**.

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` remains useful historical chronology but is not the current gate. Recency, filename, lane identity, founder identity, CI state, PR mergeability, schedule position, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical base for this sequencing state

Canonical `main` inspected by Lane 01 before this update:

`193dacae0135b2581261ee1706549b65cc245636`

Canonical message:

`Hold Decision 023 on ADV-058-J`

No Decision 023 production/runtime/schema/test semantics are canonical on `main` yet. PR #112 remains the Lane 02 implementation/repair lane.

## Current evidence disposition

### Lane 02 — ADV-058-J is repaired on its exact tested surface

PR #112 source repair commit:

`93f4841c61c3df98fbb1ce23892fd34f7afeb0f9`

Exact workflow/test-bearing head:

`4e4f9e6c681b0932386c0dfc576a323c4d071037`

Documentation-only descendant:

`8e83cfbcc6e5bb0ec68de2acad8d0b9a0d596391`

Exact native merge candidate:

`c5b81acaaf731fef6af555ed27d29aa6c2b0f3b4`

Native run/job:

`34912412206` / `104202599061`

Direct recorded results:

- Decision 020 ADV-054/055: **6/6 passed**;
- Decision 022 ADV-057: **6/6 passed**;
- ADV-058-A/B/C: **3/3 passed**;
- ADV-058-D: **1/1 passed**;
- ADV-058-E: **1/1 passed**;
- ADV-058-F: **1/1 passed**;
- ADV-058-G: **1/1 passed**;
- ADV-058-H: **1/1 passed**;
- ADV-058-I: **1/1 passed**;
- ADV-058-J unchanged oracle: **1/1 passed**;
- Decision 023 focused suite: **14/14 passed**;
- complete deterministic discovery: **461/461 passed** in `615.104s`;
- explicit compile: **passed**.

Lane 01 independently queried native workflow run `34912412206`. GitHub reports the run completed successfully and job `104202599061` records each preserved adversarial gate through J, the focused Decision 023 suite, full deterministic discovery, and compile as successful.

Lane 03 then independently re-anchored on exact Lane 02 head `4e4f9e6...` and cleared unchanged ADV-058-A/B/C/D/E/F/G/H/I/J before advancing to K. Therefore the prior J blocker is resolved on this exact tested surface. Earlier J-red evidence remains historical truth for its pre-repair ancestry.

### Lane 03 — unchanged A through J clear, ADV-058-K fails

PR #135 is the active adversarial lane.

Exact Lane 03 test/workflow-bearing head:

`03c47ac8126f97e9b6b709c09a48352afe32d62a`

Current documentation descendant:

`d553f36f9766e628cfde3e36f0832c542dd34f7a`

PR-generated merge candidate observed after PR creation:

`420aacf072a6700a2f1d5066bd5bd8e9c0b54d3a`

Native run/job:

`34913459258` / `104205846955`

Lane 01 independently queried the native job-step sequence:

- Decision 020 adversarial gate: **passed**;
- Decision 022 adversarial gate: **passed**;
- ADV-058-A/B/C: **passed**;
- ADV-058-D: **passed**;
- ADV-058-E: **passed**;
- ADV-058-F: **passed**;
- ADV-058-G: **passed**;
- ADV-058-H: **passed**;
- ADV-058-I: **passed**;
- ADV-058-J: **passed** — the incoming Lane 02 J repair is independently cleared;
- ADV-058-K: **failed**;
- Decision 023 focused suite: **skipped after K failure**;
- complete deterministic discovery: **skipped after K failure**;
- explicit compile: **skipped after K failure**.

The connector-visible job metadata establishes the ordered pass/fail/skip sequence above but does not expose the exact unittest stderr/assertion text. This sequencing state does not invent one.

ADV-058-K keeps the supplied exact `FilesystemObjectStore` target absent at its original object tree and places the exact canonical target only in a separate decoy store. The caller-owned exact-instance `_object_path` shadow does **not** import presence through its return value. Instead, when the current guard invokes that shadow, the shadow mutates only `store.objects_dir` to the decoy location. The subsequent function-owned `FilesystemObjectStore._object_path(self, ...)` then consumes that caller-mutated instance state and can reach/verify the decoy bytes.

The K fixture accepts fail-closed `SourceLiveObservationError` or context-local `not_found_in_live_context`. It rejects `exact_observed` sourced through hidden location-state mutation.

## Lead finding

The Decision 023 blocker has moved from caller-owned verifier-error authority to **caller-owned path-state side-effect authority**, while remaining inside the same already-open exact-store observation contract:

> A function-owned exact-store path/read cannot ground context-local presence if the location state it consumes was silently changed by caller-owned dispatch earlier in the same invocation. Caller-visible `_object_path` behavior may establish neither positive presence nor negative absence through hidden mutation of the state later relied on as independent grounding.

ADV-058-G already established that caller-owned `_object_path` return values may not import presence from another root. ADV-058-K demonstrates the adjacent unresolved form: ignoring the caller return value is insufficient if the subsequent base path still trusts mutable instance location state changed by that caller hook.

This is a direct Truth + Continuity contradiction because `exact_observed` would describe the supplied live context while exact presence actually came from a different object tree introduced by hidden mutation. It also protects Agency/non-domination by preventing caller hooks from silently becoming source-truth authority. Wisdom before speed requires repairing only this demonstrated invocation-local location-state seam rather than turning Decision 023 into durable store-root identity or general hostile-process isolation.

## PR disposition

- **PR #112 — keep open and held.** It owns Decision 023 implementation and the bounded repair sequence. Do not merge while ADV-058-K is red.
- **PR #135 — keep open as active adversarial evidence.** Do not merge its stacked Lane 02 ancestry as production history.
- **PR #133 — closed as superseded, not invalidated.** Its ADV-058-J red evidence remains historical truth for the exact pre-J-repair surface. Lane 02 repaired J, and PR #135 preserves unchanged A through J before adding K.

## Smallest next executable lane

### Lane 02 — repair ADV-058-K only

Repair only the demonstrated `_object_path` location-state side-effect hole.

At the verification-critical path/read layer, caller-visible exact-instance `_object_path` dispatch must not be able to change the location state consumed by the subsequent function-owned exact-store operation and thereby import exact presence from another root.

The smallest acceptable repair is either:

- fail closed when the demonstrated location state changes during caller dispatch; or
- preserve invocation-entry function-owned location state for the actual base path/read so caller dispatch cannot silently redirect the grounding context through side effects.

Do not describe an invocation-local preserved location value as durable historical store-root identity. Decision 023 still carries `context_standing = live_mutable_store` and `reexecution_standing = not_established`.

The repair must preserve:

- the exact accepted store boundary already established for Decision 023;
- the fixed bundled schema interpretation context;
- context-local not-found semantics;
- separate availability/retrieval/integrity dimensions;
- exact declaration occurrence identity;
- unsupported-kind no-target-I/O behavior;
- generic store-error indeterminacy;
- existing ADV-058-A/B/C/D/E/F/G/H/I/J expectations unchanged;
- ADV-058-K unchanged as the new regression oracle.

Do **not** widen the repair into generic Python tamper resistance, immutable source snapshots, retained-byte authority, durable store-root identity, custom schema-context identity, generic resolvers, trust/closure, Stage 5 integration, epochs/barriers, replay, or model-heavy autonomy.

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
12. Decision 023 focused suite;
13. complete deterministic discovery;
14. explicit compile.

Record exact semantic head, exact tested merge candidate, native run/job, environment, direct counts/step evidence, skipped checks if any, preserved failed attempts, and uncertainty in the Lane 02 return packet.

### Lane 03 — independent recheck after repair

After Lane 02 publishes an exact K-repair semantic head, independently rerun ADV-058-A/B/C/D/E/F/G/H/I/J/K unchanged on that ancestry.

Attack another nearby path only if repository evidence demonstrates another concrete contradiction inside Decision 023's already-open actual exact-store validation/availability contract. Do not turn the lane into open-ended same-process hardening. If A through K all clear and no concrete adjacent contradiction is evidenced, return control to Lane 01 for integration review.

### Lane 01 — integration hold

Do not merge Decision 023 until the K red -> bounded repair -> independent unchanged-oracle evidence chain is complete and the resulting surface remains grounded against Truth, Agency/non-domination, Continuity, and Wisdom before speed.

Green CI, role identity, founder identity, recency, schedule position, or Git permission alone is not integration authority.

## Historical evidence preserved

The current K blocker does not rewrite earlier evidence:

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
- Lane 02 repaired each demonstrated A through J path on its exact tested surface;
- Lane 03 independently clears A through J on the latest repaired ancestry;
- ADV-058-K now shows caller-owned `_object_path` side effects can mutate `store.objects_dir` before the base path consumes it and import exact presence from another store root.

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
