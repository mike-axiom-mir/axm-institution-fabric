# CURRENT BLOCKER — Institution Fabric

Status: **Decision 023 remains blocked.** The first exact live source-observation slice is not canonical yet.

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` remains useful historical chronology but is not the current gate. Recency, filename, lane identity, founder identity, CI state, PR mergeability, schedule position, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical base for this sequencing state

Canonical `main` inspected by Lane 01 before this update:

`0b07bb1adfff0d7f51271173bd43f5ea07b627e5`

Canonical message:

`Hold Decision 023 on ADV-058-F`

No Decision 023 production/runtime/schema/test semantics are canonical on `main` yet. PR #112 remains the Lane 02 implementation/repair lane.

## Current evidence disposition

### Lane 02 — ADV-058-F is repaired on its exact tested surface

PR #112 exact ADV-058-F semantic/test-bearing head:

`7fcc0c1e36bb17d7c5801df50b3ccaccd595c9d8`

Current PR #112 descendant inspected by Lane 03:

`0a08d2b0d5e45f6b06eec42bc2efec6d784dc834`

Lane 02 Activation 055 records exact current-main merge candidate:

`68e656ba36856b4e54c2c6e265b17188a5ea1ca6`

Native run/job:

`34891755343` / `104135918905`

Direct recorded results:

- Decision 020 ADV-054/055: **6/6 passed**;
- Decision 022 ADV-057-A–F: **6/6 passed**;
- ADV-058-A/B/C: **3/3 passed**;
- ADV-058-D: **1/1 passed**;
- ADV-058-E: **1/1 passed**;
- ADV-058-F: **1/1 passed**;
- Decision 023 focused suite: **14/14 passed**;
- complete deterministic discovery: **457/457 passed**;
- explicit compile: **passed**.

The F repair binds the verification-critical call away from caller-owned exact-instance `_verify_existing` success and makes successful base verification necessary on the demonstrated path. This evidence remains valid. It is not erased by the newer G counterexample.

### Lane 03 — unchanged A/B/C/D/E/F clear, ADV-058-G fails

PR #127 is the active adversarial lane.

Exact Lane 03 test/workflow-bearing head recorded by Activation 058:

`b9af0b41052cb32e1b9acd1e1bdf16cea6c9a684`

Current PR #127 descendant:

`5080e931714560aa02c31e8a3ba95801ec1f5594`

Activation 058 native candidate/run/job:

- merge candidate: `47638dc3220b8316aefaddf51cce05c2aa87800d`;
- run/job: `34893294831` / `104140989703`.

Observed adversarial sequence on the repaired F ancestry:

- Decision 020 ADV-054/055: **6/6 passed**;
- Decision 022 ADV-057-A–F: **6/6 passed**;
- ADV-058-A/B/C: **3/3 passed**;
- ADV-058-D: **1/1 passed**;
- ADV-058-E: **1/1 passed**;
- ADV-058-F: **1/1 passed**;
- ADV-058-G: **1 run, 1 failure**;
- Decision 023 focused suite: **skipped after G failure**;
- complete deterministic suite: **skipped after G failure**;
- explicit compile: **skipped after G failure**.

Exact G failure:

`AssertionError: 'not_found_in_live_context' != 'exact_observed'`

Fixture message:

`caller-shadowed _object_path must not import exact presence from another root`

The current PR #127 descendant also remains red at the ADV-058-G workflow step on run/job `34893511071` / `104141697127`, while the earlier Decision 020/022 and ADV-058-A/B/C/D/E/F gates pass before that failure.

ADV-058-G keeps the accepted exact `FilesystemObjectStore` type and leaves `load_bytes`, `_verify_existing`, and `schema_dir` untouched. The supplied live store root A deliberately lacks the declared exact target. A different root B contains the exact canonical target bytes. Caller-owned instance `_object_path` dispatch redirects only path location from the supplied store to root B. Base schema validation, canonical-byte comparison, and immutable-reference reproduction can then succeed on exact bytes reached outside the supplied store root, allowing the observer to emit `exact_observed` even though the target is absent from the supplied live context.

## Lead finding

The Decision 023 blocker has moved from verifier dispatch to object-location dispatch, but the institutional contradiction remains bounded:

> A positive `exact_observed` fact must ground both availability and exact identity in the supplied live store context. Exact bytes verified after caller-owned path redirection from another root are not evidence that the target was observed in the supplied store.

This is a Truth + Continuity contradiction inside Decision 023's already-open exact-store validation/availability contract. It is not evidence that AXM needs a general hostile-process security architecture.

## PR disposition

- **PR #112 — keep open and held.** It owns the Decision 023 implementation and bounded repair sequence. Do not merge while ADV-058-G is red.
- **PR #127 — keep open as active adversarial evidence.** Do not merge its stacked Lane 02 ancestry as production history.
- **PR #125 — superseded, not invalidated.** Its ADV-058-F red evidence remains historical truth for the pre-F-repair surface. Lane 02 repaired F and PR #127 preserves unchanged A/B/C/D/E/F before adding G; PR #125 can therefore be closed after this sequencing state is canonical without erasing its evidence.

## Smallest next executable lane

### Lane 02 — repair ADV-058-G only

Repair only the demonstrated object-path dispatch hole.

A normal positive observation must not depend on caller-owned exact-instance `_object_path` dispatch. Bind the actual verification-critical path location to non-caller-owned base exact-store behavior for the supplied store, or fail closed on the demonstrated override path.

The repair must preserve:

- the exact accepted store boundary already established for Decision 023;
- the function-owned bundled schema interpretation context;
- `context_standing = live_mutable_store`;
- `reexecution_standing = not_established`;
- context-local not-found semantics;
- separate availability/retrieval/integrity dimensions;
- exact declaration occurrence identity;
- unsupported-kind no-target-I/O behavior;
- existing ADV-058-A/B/C/D/E/F expectations unchanged;
- ADV-058-G unchanged as the new regression oracle.

Do **not** widen the repair into generic Python hardening, immutable source snapshots, retained-byte authority, durable store-root identity, custom schema-context identity, generic resolvers, trust/closure, Stage 5 integration, epochs/barriers, replay, or model-heavy autonomy.

Required evidence after repair, in order:

1. Decision 020 ADV-054/055 unchanged;
2. Decision 022 ADV-057 unchanged;
3. ADV-058-A/B/C unchanged;
4. ADV-058-D unchanged;
5. ADV-058-E unchanged;
6. ADV-058-F unchanged;
7. ADV-058-G unchanged;
8. Decision 023 focused suite;
9. complete deterministic discovery;
10. explicit compile.

Record the exact semantic head, exact tested merge candidate, native run/job, environment, direct counts, skipped checks if any, and uncertainty in the Lane 02 return packet.

### Lane 03 — independent recheck after repair

After Lane 02 publishes an exact G-repair semantic head, independently rerun ADV-058-A/B/C/D/E/F/G unchanged on that ancestry.

Attack another nearby path only if repository evidence demonstrates another contradiction inside Decision 023's already-open actual exact-store validation/availability contract. Do not turn the lane into open-ended same-process hardening.

### Lane 01 — integration hold

Do not merge Decision 023 until the G red → bounded repair → independent unchanged-oracle evidence chain is complete and the resulting surface remains grounded against Truth, Agency/non-domination, Continuity, and Wisdom before speed.

Green CI or Git permission alone is not integration authority.

## Historical evidence preserved

The current G blocker does not rewrite earlier evidence:

- ADV-058-A exposed bundled-schema substitution between capability classification and observation;
- ADV-058-B exposed caller-owned validation-context rebind/restore;
- ADV-058-C exposed exact-instance `load_bytes` replacement despite exact class identity;
- ADV-058-D exposed direct `store.__dict__['schema_dir']` rebinding around validation;
- ADV-058-E exposed caller-owned `load_bytes` success being accepted without actual exact-store verification;
- ADV-058-F exposed base `load_bytes` delegating verification through caller-shadowable `_verify_existing`;
- Lane 02 repaired each demonstrated path on its exact tested surface before Lane 03 advanced;
- ADV-058-G now shows base verification still locates material through caller-shadowable `_object_path`, allowing exact presence from another root to be imported into the supplied live-context fact.

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
