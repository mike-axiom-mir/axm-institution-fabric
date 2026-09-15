# CURRENT BLOCKER — Institution Fabric

Status: **Decision 023 remains blocked.** The first exact live source-observation slice is not canonical yet. The active contradiction is now **ADV-058-J**.

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` remains useful historical chronology but is not the current gate. Recency, filename, lane identity, founder identity, CI state, PR mergeability, schedule position, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical base for this sequencing state

Canonical `main` inspected by Lane 01 before this update:

`e394cadaa95de95fdf027943d09d89265f3e2c8c`

Canonical message:

`Hold Decision 023 on ADV-058-I`

No Decision 023 production/runtime/schema/test semantics are canonical on `main` yet. PR #112 remains the Lane 02 implementation/repair lane.

## Current evidence disposition

### Lane 02 — ADV-058-I is repaired on its exact tested surface

PR #112 final bounded I-repair semantic/test-bearing head:

`6c07a773c9d1c6cf200e46a3d27442b8c7d8c235`

Current documentation-only descendant:

`38d13a3ec50f6c3223b5236d910040a6daa90a6a`

Exact native merge candidate:

`788337f89c1231c113aff50f7a5c8e91a2e5d9d7`

Native run/job:

`34908100733` / `104189291523`

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
- Decision 023 focused suite: **14/14 passed**;
- complete deterministic discovery: **460/460 passed** in `398.990s`;
- explicit compile: **passed**.

Lane 01 independently checked the native workflow metadata for semantic head `6c07a773...`: run `34908100733` completed successfully, and its job records every preserved adversarial gate through I, the focused Decision 023 suite, full deterministic discovery, and compile as successful.

The final I repair is intentionally narrower than Lane 02's first attempt. The first attempt at `7fe6b600...` made ADV-058-I green but broke `test_generic_store_failure_remains_indeterminate_not_absence`; that red focused regression remains preserved. Final head `6c07a773...` suppresses only caller-raised `ObjectNotFoundError` on the exact-instance `load_bytes` shadow before independently allowing the function-owned base `FilesystemObjectStore.load_bytes(...)` path to determine the supplied-store observation. Generic caller-raised `ObjectStoreError` remains an indeterminate store error.

Lane 03 independently cleared unchanged ADV-058-A/B/C/D/E/F/G/H/I on this repaired ancestry before advancing to J. Therefore the prior I blocker is resolved on this exact tested surface. Earlier I-red evidence remains historical truth for its pre-repair ancestry.

### Lane 03 — unchanged A through I clear, ADV-058-J fails

PR #133 is the active adversarial lane.

Exact Lane 03 test/workflow-bearing head:

`2d6c64bc384d5082dd841214f85ba17cad2de67c`

Current documentation descendant:

`c8cf921e82e5517b6f0b7611cc92e62dfc158593`

PR-generated merge candidate observed after PR creation:

`271a786985e129dc29c080abb287e95e017ac2a8`

Native run/job:

`34909066307` / `104192271729`

Lane 01 independently checked the native job-step sequence:

- Decision 020 adversarial gate: **passed**;
- Decision 022 adversarial gate: **passed**;
- ADV-058-A/B/C: **passed**;
- ADV-058-D: **passed**;
- ADV-058-E: **passed**;
- ADV-058-F: **passed**;
- ADV-058-G: **passed**;
- ADV-058-H: **passed**;
- ADV-058-I: **passed** — the incoming Lane 02 I repair is independently cleared;
- ADV-058-J: **failed**;
- Decision 023 focused suite: **skipped after J failure**;
- complete deterministic discovery: **skipped after J failure**;
- explicit compile: **skipped after J failure**.

The connector-visible job metadata establishes the ordered pass/fail/skip sequence above but does not expose the exact unittest stderr/assertion text. This sequencing state does not invent one.

ADV-058-J keeps the exact target genuinely present in the supplied exact `FilesystemObjectStore`. It leaves the exact store type, root, `objects_dir`, `load_bytes`, `_object_path`, and `schema_dir` unchanged. Only the exact instance's caller-owned `_verify_existing` dispatch is shadowed to raise a forged `ObjectNotFoundError` before the function-owned base verifier can read the exact path and reproduce immutable identity.

The current guard invokes that caller-owned verifier dispatch first. If the caller shadow raises, `FilesystemObjectStore._verify_existing(self, ...)` does not execute before the store-layer error escapes into the enclosing observation classification. The result can therefore be treated as `not_found_in_live_context` even though the supplied exact store genuinely contains the target.

The J fixture accepts either a fail-closed `SourceLiveObservationError` or an independently grounded `exact_observed`. It rejects a false context-local absence fact.

## Lead finding

The Decision 023 blocker has moved from caller-owned `load_bytes` error authority to caller-owned `_verify_existing` error authority, while staying inside the same already-open exact-store observation contract:

> Caller-owned verification-critical dispatch must establish neither positive presence nor negative absence for the supplied live store. A context-local observation fact must be grounded in the function-owned exact-store path/verification operation, or the operation must fail closed.

Decision 023 says `not_found_in_live_context` means the exact object was not present in the inspected live-store invocation. A caller-owned verifier exception cannot ground that affirmative absence fact when the base store still contains the object. This is a direct Truth + Continuity contradiction. It also protects Agency/non-domination by preventing hidden caller hooks from silently becoming source truth authority. Wisdom before speed requires repairing only the demonstrated J seam rather than turning Decision 023 into a general hostile-process isolation project.

## PR disposition

- **PR #112 — keep open and held.** It owns Decision 023 implementation and the bounded repair sequence. Do not merge while ADV-058-J is red.
- **PR #133 — keep open as active adversarial evidence.** Do not merge its stacked Lane 02 ancestry as production history.
- **PR #131 — closed as superseded, not invalidated.** Its ADV-058-I red evidence remains historical truth for the exact pre-I-repair surface. Lane 02 repaired I, and PR #133 preserves unchanged A through I before adding J.

## Smallest next executable lane

### Lane 02 — repair ADV-058-J only

Repair only the demonstrated caller-owned `_verify_existing` error-authority hole.

At the verification-critical `_verify_existing` layer, caller-owned exact-instance dispatch must not be allowed to establish either positive presence or negative absence for the supplied live store before the function-owned base verifier grounds the observation. The smallest acceptable repair is either:

- fail closed on the demonstrated caller-owned verifier error path; or
- preserve any required caller-visible dispatch while independently allowing `FilesystemObjectStore._verify_existing(self, ...)` to determine presence/absence/identity when the caller shadow raises the demonstrated store-layer error.

Do not interpret a caller-raised `_verify_existing` `ObjectNotFoundError` as `not_found_in_live_context` unless the supplied base-store observation itself grounds that absence.

The repair must preserve:

- the exact accepted store boundary already established for Decision 023;
- the function-owned bundled schema interpretation context;
- `context_standing = live_mutable_store`;
- `reexecution_standing = not_established`;
- context-local not-found semantics;
- separate availability/retrieval/integrity dimensions;
- exact declaration occurrence identity;
- unsupported-kind no-target-I/O behavior;
- generic store-error indeterminacy;
- existing ADV-058-A/B/C/D/E/F/G/H/I expectations unchanged;
- ADV-058-J unchanged as the new regression oracle.

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
11. Decision 023 focused suite;
12. complete deterministic discovery;
13. explicit compile.

Record exact semantic head, exact tested merge candidate, native run/job, environment, direct counts/step evidence, skipped checks if any, preserved failed attempts, and uncertainty in the Lane 02 return packet.

### Lane 03 — independent recheck after repair

After Lane 02 publishes an exact J-repair semantic head, independently rerun ADV-058-A/B/C/D/E/F/G/H/I/J unchanged on that ancestry.

Attack another nearby path only if repository evidence demonstrates another concrete contradiction inside Decision 023's already-open actual exact-store validation/availability contract. Do not turn the lane into open-ended same-process hardening. If A through J all clear and no concrete adjacent contradiction is evidenced, return control to Lane 01 for integration review.

### Lane 01 — integration hold

Do not merge Decision 023 until the J red -> bounded repair -> independent unchanged-oracle evidence chain is complete and the resulting surface remains grounded against Truth, Agency/non-domination, Continuity, and Wisdom before speed.

Green CI, role identity, founder identity, or Git permission alone is not integration authority.

## Historical evidence preserved

The current J blocker does not rewrite earlier evidence:

- ADV-058-A exposed bundled-schema substitution between capability classification and observation;
- ADV-058-B exposed caller-owned validation-context rebind/restore;
- ADV-058-C exposed exact-instance `load_bytes` replacement despite exact class identity;
- ADV-058-D exposed direct `store.__dict__['schema_dir']` rebinding around validation;
- ADV-058-E exposed caller-owned `load_bytes` success being accepted without actual exact-store verification;
- ADV-058-F exposed base `load_bytes` delegating verification through caller-shadowable `_verify_existing`;
- ADV-058-G exposed caller-shadowable `_object_path` return values importing presence from another root;
- ADV-058-H exposed caller-shadowable `_object_path` errors manufacturing false context-local absence;
- ADV-058-I exposed caller-owned exact-instance `load_bytes` errors manufacturing false context-local absence before the base exact-store read;
- Lane 02 repaired each demonstrated A through I path on its exact tested surface;
- Lane 03 independently clears A through I on the latest repaired ancestry;
- ADV-058-J now shows caller-owned exact-instance `_verify_existing` error behavior can still preempt the function-owned base verifier and manufacture false context-local absence.

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
