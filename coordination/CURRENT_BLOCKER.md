# CURRENT BLOCKER — Institution Fabric

Status: **Decision 023 remains blocked.** The first exact live source-observation slice is not canonical yet.

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` remains useful historical chronology but is not the current gate. Recency, filename, lane identity, founder identity, CI state, PR mergeability, schedule position, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical base for this sequencing state

Canonical `main` inspected by Lane 01 before this update:

`9b0760c36ded79eeab80ddf911810113b5527653`

Canonical message:

`Hold Decision 023 on ADV-058-H`

No Decision 023 production/runtime/schema/test semantics are canonical on `main` yet. PR #112 remains the Lane 02 implementation/repair lane.

## Current evidence disposition

### Lane 02 — ADV-058-H is repaired on its exact tested surface

PR #112 H-repair production commit:

`ecc8976e9c14b588929ff787a4e8572a25fd0ec4`

Unchanged H oracle carry commit:

`e3d4561adfea949e7d4f9cfeb2719fff8f253230`

H workflow-gate commit:

`353aa856e8e3b3d5b838255b9bed1deac501349f`

Exact current-main semantic/test-bearing head:

`be72ff59c093a36ec702d8494274f6db45d3718c`

Current documentation-only descendant:

`b530e3cf6ad144ff0c5d2d3a5be924b633e29f74`

Exact native merge candidate recorded by Lane 02 Activation 057:

`a422a7f53c6a067f17fcd5d52225e8f34be11f7a`

Native run/job:

`34903712072` / `104175393991`

Direct recorded results:

- Decision 020 ADV-054/055: **6/6 passed**;
- Decision 022 ADV-057: **6/6 passed**;
- ADV-058-A/B/C: **3/3 passed**;
- ADV-058-D: **1/1 passed**;
- ADV-058-E: **1/1 passed**;
- ADV-058-F: **1/1 passed**;
- ADV-058-G: **1/1 passed**;
- ADV-058-H: **1/1 passed**;
- Decision 023 focused suite: **14/14 passed**;
- complete deterministic discovery: **459/459 passed** in `522.803s`;
- explicit compile: **passed**.

The H repair prevents caller-owned `_object_path` `ObjectStoreError` behavior from becoming presence/absence authority. After exercising the caller-visible path hook, the observer independently derives the base `FilesystemObjectStore._object_path(...)` path so the supplied exact store determines the context-local observation. Unexpected non-`ObjectStoreError` exceptions still fail closed.

Lane 03 independently cleared unchanged ADV-058-A/B/C/D/E/F/G/H on this exact repaired head before advancing to I. Therefore the prior H blocker is resolved on this exact tested surface. Earlier H-red evidence remains historical truth for the pre-repair ancestry.

### Lane 03 — unchanged A/B/C/D/E/F/G/H clear, ADV-058-I fails

PR #131 is the active adversarial lane.

Exact Lane 03 test/workflow-bearing head:

`f35352656c5aef73a78b2295820ca20e83303bfe`

Current documentation descendant:

`929f54cfb13fab4af0b9073fb72c9c08ec0c17f1`

Exact tested current-main merge candidate:

`1ab2918a1c4e1b531e593cae0ef9cfa296bab601`

Native run/job:

`34904650703` / `104178385568`

Direct job-step sequence:

- Decision 020 adversarial gate: **passed**;
- Decision 022 adversarial gate: **passed**;
- ADV-058-A/B/C: **passed**;
- ADV-058-D: **passed**;
- ADV-058-E: **passed**;
- ADV-058-F: **passed**;
- ADV-058-G: **passed**;
- ADV-058-H: **passed** — the prior path-error-authority counterexample is independently cleared;
- ADV-058-I: **failed**;
- Decision 023 focused suite: **skipped after I failure**;
- complete deterministic discovery: **skipped after I failure**;
- explicit compile: **skipped after I failure**.

GitHub job metadata proves the ordered pass/fail/skip sequence above but does not expose the exact unittest stderr line in the connector-visible result, so this sequencing state does not invent a quoted assertion or numerical unittest count for the Lane 03 I step.

ADV-058-I keeps the exact target genuinely present in the supplied exact `FilesystemObjectStore`. It leaves exact store type, root, `objects_dir`, `_verify_existing`, `_object_path`, and `schema_dir` unchanged. Only the exact instance's caller-owned `load_bytes` dispatch raises a forged `ObjectNotFoundError` before the function-owned base `FilesystemObjectStore.load_bytes(...)` executes. The enclosing observation layer can then classify that propagated caller error as `not_found_in_live_context` even though the exact target is present.

## Lead finding

The Decision 023 blocker has moved from caller-owned `_object_path` error authority to caller-owned `load_bytes` error authority, but the institutional contradiction remains the same bounded class:

> Caller-owned verification-critical dispatch must establish neither positive presence nor negative absence for the supplied live store. A context-local observation fact must be grounded in the function-owned exact-store read/verification path, not in caller-controlled success or error behavior that can preempt that path.

This is a Truth + Continuity contradiction inside Decision 023's already-open exact-store availability/validation contract. It also protects Agency/non-domination by preventing hidden caller hooks from silently becoming truth authority. It is not evidence that AXM needs a general hostile-process security architecture.

## PR disposition

- **PR #112 — keep open and held.** It owns the Decision 023 implementation and bounded repair sequence. Do not merge while ADV-058-I is red.
- **PR #131 — keep open as active adversarial evidence.** Do not merge its stacked Lane 02 ancestry as production history.
- **PR #129 — superseded, not invalidated.** Its ADV-058-H red evidence remains historical truth for the pre-H-repair surface. Lane 02 repaired H, and PR #131 preserves unchanged A/B/C/D/E/F/G/H before adding I. PR #129 may be closed after this sequencing state is canonical without erasing its evidence.

## Smallest next executable lane

### Lane 02 — repair ADV-058-I only

Repair only the demonstrated caller-owned `load_bytes` error-authority hole.

A caller-owned exact-instance `load_bytes` shadow must not be allowed to establish either positive presence or negative absence for the supplied live store before the function-owned base exact-store read executes. The smallest acceptable repair is either:

- fail closed when that caller-owned verification-critical dispatch raises; or
- ensure the function-owned base `FilesystemObjectStore.load_bytes(...)` path independently determines the observation even when the caller shadow raises a store-layer error.

Do not interpret a caller-raised `ObjectNotFoundError` as `not_found_in_live_context` unless the supplied base-store observation itself grounds that absence.

The repair must preserve:

- the exact accepted store boundary already established for Decision 023;
- the function-owned bundled schema interpretation context;
- `context_standing = live_mutable_store`;
- `reexecution_standing = not_established`;
- context-local not-found semantics;
- separate availability/retrieval/integrity dimensions;
- exact declaration occurrence identity;
- unsupported-kind no-target-I/O behavior;
- existing ADV-058-A/B/C/D/E/F/G/H expectations unchanged;
- ADV-058-I unchanged as the new regression oracle.

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
10. Decision 023 focused suite;
11. complete deterministic discovery;
12. explicit compile.

Record the exact semantic head, exact tested merge candidate, native run/job, environment, direct counts/step evidence, skipped checks if any, and uncertainty in the Lane 02 return packet.

### Lane 03 — independent recheck after repair

After Lane 02 publishes an exact I-repair semantic head, independently rerun ADV-058-A/B/C/D/E/F/G/H/I unchanged on that ancestry.

Attack another nearby path only if repository evidence demonstrates another concrete contradiction inside Decision 023's already-open actual exact-store validation/availability contract. Do not turn the lane into open-ended same-process hardening. If A–I all clear and no concrete adjacent contradiction is evidenced, return control to Lane 01 for integration review.

### Lane 01 — integration hold

Do not merge Decision 023 until the I red -> bounded repair -> independent unchanged-oracle evidence chain is complete and the resulting surface remains grounded against Truth, Agency/non-domination, Continuity, and Wisdom before speed.

Green CI or Git permission alone is not integration authority.

## Historical evidence preserved

The current I blocker does not rewrite earlier evidence:

- ADV-058-A exposed bundled-schema substitution between capability classification and observation;
- ADV-058-B exposed caller-owned validation-context rebind/restore;
- ADV-058-C exposed exact-instance `load_bytes` replacement despite exact class identity;
- ADV-058-D exposed direct `store.__dict__['schema_dir']` rebinding around validation;
- ADV-058-E exposed caller-owned `load_bytes` success being accepted without actual exact-store verification;
- ADV-058-F exposed base `load_bytes` delegating verification through caller-shadowable `_verify_existing`;
- ADV-058-G exposed caller-shadowable `_object_path` return values importing presence from another root;
- ADV-058-H exposed caller-shadowable `_object_path` errors manufacturing false context-local absence;
- Lane 02 repaired each demonstrated A–H path on its exact tested surface before Lane 03 advanced;
- Lane 03 independently clears A–H on the latest repaired ancestry;
- ADV-058-I now shows caller-owned exact-instance `load_bytes` error behavior can still preempt the function-owned exact-store read and manufacture false context-local absence.

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
