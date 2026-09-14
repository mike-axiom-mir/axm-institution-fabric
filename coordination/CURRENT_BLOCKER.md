# CURRENT BLOCKER — Institution Fabric

Status: **Decision 023 remains blocked.** The first exact live source-observation slice is not canonical yet.

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` remains useful historical chronology but is not the current gate. Recency, filename, lane identity, founder identity, CI state, PR mergeability, schedule position, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical base for this sequencing state

Canonical `main` inspected by Lane 01 before this update:

`49f39edc3c74a5d2914911c5007d716e65b64335`

Canonical message:

`Hold Decision 023 on ADV-058-E`

No production/runtime/schema/test semantics from Decision 023 are canonical on `main` yet. PR #112 remains the Lane 02 implementation/repair lane.

## Current evidence disposition

### Lane 02 — ADV-058-E is repaired on its exact tested surface

PR #112 exact Decision 023 semantic/test-bearing head:

`9da6cf68cdd15b7da1108d7900b5740ba4de3d8c`

Current documentation descendant:

`35341b9f9c1f0b050febbbf121e701d6288343da`

Lane 02's durable Activation 054 packet records native candidate `34dec338b51201fcff26b3303f9ee862a874bc9c`, run/job `34885839817` / `104116159398`, with:

- Decision 020 ADV-054/055: **6/6 passed**;
- Decision 022 ADV-057-A–F: **6/6 passed**;
- ADV-058-A/B/C: **3/3 passed**;
- ADV-058-D: **1/1 passed**;
- ADV-058-E: **1/1 passed**;
- Decision 023 focused suite: **14/14 passed**;
- complete deterministic discovery: **456/456 passed**;
- explicit compile: **passed**.

A later native run on current PR #112 head `35341b9f...` also checked out exact current-main merge candidate `783a6825249e2bbcaaf14e2072e624685e2e28a6` and again passed the same Decision 020/022/A–E/focused gates, **456/456** full deterministic tests, and explicit compile. This newer run confirms the documentation descendant remains green; it does not widen the bounded claim.

The E repair correctly prevents caller-owned exact-instance `load_bytes` return success from being accepted as validation proof. The guarded path invokes the base `FilesystemObjectStore.load_bytes(...)` operation before a normal positive observation can be emitted.

That evidence remains valid. It is not erased by the newer F counterexample.

### Lane 03 — unchanged A/B/C/D/E clear, ADV-058-F fails

PR #125 is the active adversarial lane.

Exact Lane 03 test/workflow-bearing head recorded by Activation 057:

`14c1d1eb8d358488d14a81131d51c57ffc5b4e7c`

Documentation/current PR descendant:

`93a79742d67e3c1844e2a2fbb132734f84418220`

Activation 057 native candidate/run/job:

- merge candidate: `4c4c27c431dcd0ca3917f734584c45d8c4a214c4`;
- run/job: `34887362531` / `104121200005`.

Current PR-head verification also remained red on candidate `30bb6084dc9d60833b75e25f31dde28c1663ba9f`, run/job `34887506605` / `104121679903`.

Observed adversarial sequence on the current repaired ancestry:

- Decision 020 ADV-054/055: **passed**;
- Decision 022 ADV-057-A–F: **passed**;
- ADV-058-A/B/C: **passed**;
- ADV-058-D: **passed**;
- ADV-058-E: **passed**;
- ADV-058-F: **failed**;
- Decision 023 focused suite: **skipped after F failure**;
- complete deterministic suite: **skipped after F failure**;
- explicit compile: **skipped after F failure**.

Exact F failure:

`AssertionError: 'not_found_in_live_context' != 'exact_observed'`

Fixture message:

`caller-shadowed _verify_existing must not forge exact_observed`

ADV-058-F keeps the accepted exact `FilesystemObjectStore` type and does not replace `load_bytes` or mutate `schema_dir`. It shadows only the exact instance's `_verify_existing` method. The declared target is absent. Because base `FilesystemObjectStore.load_bytes(self, ...)` still delegates verification through `self._verify_existing(...)`, caller-owned instance dispatch can return arbitrary bytes without exact-path I/O, schema/canonical validation, or immutable-reference reproduction. The observer can then emit `exact_observed` even though the verification event claimed by the fact never occurred.

## Lead finding

The Decision 023 blocker has moved one layer deeper, but it remains the same bounded institutional contract:

> A positive `exact_observed` fact must be grounded in the actual exact-store read and immutable identity verification under the same function-owned interpretation context. Binding the outer `load_bytes` call to base-class behavior is insufficient if that base operation still delegates its verification-critical step through caller-owned instance dispatch.

This is a validation-provenance contradiction, not evidence that AXM needs a general hostile-process security architecture.

## PR disposition

- **PR #112 — keep open and held.** It owns the Decision 023 implementation and bounded repair sequence. Do not merge while ADV-058-F is red.
- **PR #125 — keep open as active adversarial evidence.** Do not merge its stacked Lane 02 ancestry as production history.
- **PR #123 — superseded, not invalidated.** Its ADV-058-E red evidence remains historical truth for the pre-E-repair surface. Lane 02 repaired E and PR #125 preserves unchanged A/B/C/D/E before adding F; PR #123 can therefore be closed after this sequencing state is canonical without erasing its evidence.

## Smallest next executable lane

### Lane 02 — repair ADV-058-F only

Repair only the demonstrated verifier-dispatch hole.

A normal positive observation must not depend on caller-owned exact-instance `_verify_existing` dispatch. Bind the actual verification-critical operation to non-caller-owned exact-store behavior, or fail closed on the demonstrated override path.

The repair must preserve:

- the exact accepted store boundary already established for Decision 023;
- the function-owned bundled schema interpretation context;
- `context_standing = live_mutable_store`;
- `reexecution_standing = not_established`;
- context-local not-found semantics;
- separate availability/retrieval/integrity dimensions;
- exact declaration occurrence identity;
- unsupported-kind no-target-I/O behavior;
- existing A/B/C/D/E adversarial expectations unchanged.

Do **not** widen the repair into generic Python hardening, immutable source snapshots, retained-byte authority, custom schema-context identity, generic resolvers, trust/closure, Stage 5 integration, epochs/barriers, replay, or model-heavy autonomy.

Required evidence after repair, in order:

1. Decision 020 ADV-054/055 unchanged;
2. Decision 022 ADV-057 unchanged;
3. ADV-058-A/B/C unchanged;
4. ADV-058-D unchanged;
5. ADV-058-E unchanged;
6. ADV-058-F unchanged;
7. Decision 023 focused suite;
8. complete deterministic discovery;
9. explicit compile.

Record the exact semantic head, exact tested merge candidate, native run/job, environment, direct counts, skipped checks if any, and uncertainty in the Lane 02 return packet.

### Lane 03 — independent recheck after repair

After Lane 02 publishes an exact F-repair semantic head, independently rerun ADV-058-A/B/C/D/E/F unchanged on that ancestry.

Attack another nearby path only if repository evidence demonstrates another contradiction inside Decision 023's already-open actual exact-store validation contract. Do not turn the lane into open-ended same-process hardening.

### Lane 01 — integration hold

Do not merge Decision 023 until the F red → bounded repair → independent unchanged-oracle evidence chain is complete and the resulting surface remains grounded against Truth, Agency/non-domination, Continuity, and Wisdom before speed.

Green CI or Git permission alone is not integration authority.

## Historical evidence preserved

The current F blocker does not rewrite earlier evidence:

- ADV-058-A exposed bundled-schema substitution between capability classification and observation;
- ADV-058-B exposed caller-owned validation-context rebind/restore;
- ADV-058-C exposed exact-instance `load_bytes` replacement despite exact class identity;
- ADV-058-D exposed direct `store.__dict__['schema_dir']` rebinding around validation;
- ADV-058-E exposed caller-owned `load_bytes` success being accepted without actual exact-store verification;
- Lane 02 repaired each demonstrated path on its exact tested surface before Lane 03 advanced to the next counterexample;
- ADV-058-F now shows base `load_bytes` still reaches caller-shadowable `_verify_existing` dispatch.

Each red remains valid for its exact pre-repair ancestry. Each green remains valid for its exact tested repaired surface. Neither class of evidence erases the other.

## Unresolved boundary — still explicitly unopened

Decision 023 does not establish:

- general hostile same-process code isolation;
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

Institution Fabric remains in the bounded Stage 4 source-fact work needed before later integration/replay claims can be truthful. The deterministic kernel direction is unchanged: explicit typed facts first, then immutable integration/replay only after their input meaning is grounded. Model-heavy autonomy remains out of scope.
