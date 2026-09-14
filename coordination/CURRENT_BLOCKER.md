# CURRENT BLOCKER — Institution Fabric

Status: **Decision 023 remains blocked.** The first exact live source-observation slice is not canonical yet.

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` remains useful historical chronology but is not the current gate. Recency, filename, lane identity, founder identity, CI state, PR mergeability, schedule position, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical base for this sequencing state

Canonical `main` inspected by Lane 01 before this update:

`2f2a869cc8aba919713100b49e4e061d0334f5eb`

Canonical message:

`Hold Decision 023 on ADV-058-G`

No Decision 023 production/runtime/schema/test semantics are canonical on `main` yet. PR #112 remains the Lane 02 implementation/repair lane.

## Current evidence disposition

### Lane 02 — ADV-058-G is repaired on its exact tested surface

PR #112 production G-repair commit:

`1503f344d4f93a6157af3cb3b7fa5cf0d5a60fab`

Exact Lane 02 semantic/test-bearing head:

`211c0b9104780170cbb148127543d081b420297b`

Return-packet/documentation descendant:

`24d90175fbe34bedeef701ed6fa9e81342ed542c`

Exact native current-main merge candidate recorded by Lane 02 Activation 056:

`782f99291e63954df5cf255955545284943d2721`

Native run/job:

`34897991303` / `104156775112`

Direct recorded results:

- Decision 020 ADV-054/055: **6/6 passed**;
- Decision 022 ADV-057-A–F: **6/6 passed**;
- ADV-058-A/B/C: **3/3 passed**;
- ADV-058-D: **1/1 passed**;
- ADV-058-E: **1/1 passed**;
- ADV-058-F: **1/1 passed**;
- ADV-058-G: **1/1 passed**;
- Decision 023 focused suite: **14/14 passed**;
- complete deterministic discovery: **458/458 passed**;
- explicit compile: **passed**.

Lane 02's bounded G repair prevents a successful caller-owned exact-instance `_object_path` return value from becoming location authority for the verification-critical read. The actual path used by base verification is derived through `FilesystemObjectStore._object_path(self, reference)` for the supplied exact store. This evidence remains valid for the exact surface tested. It is not erased by the newer H counterexample.

The current PR #112 documentation descendant also reran natively as run/job `34898972037` / `104160019637` and completed all then-present Decision 020/022, ADV-058-A/B/C/D/E/F/G, focused Decision 023, full deterministic discovery, and explicit compile steps successfully. This later run is supporting continuity evidence; the direct numerical counts above remain those recorded by the exact Activation 056 candidate.

### Lane 03 — unchanged A/B/C/D/E/F/G clear, ADV-058-H fails

PR #129 is the active adversarial lane.

Exact Lane 03 test/workflow-bearing head recorded by Activation 059:

`231c80784ee630f1da9b961bf2d25c21dd67bd97`

Current PR #129 documentation descendant:

`df0dfc95d724732d9ce1d5c9d908ada82291b824`

Activation 059 native candidate/run/job:

- merge candidate: `df49051a0126e6dc4832bfd46199a4e184ca944b`;
- run/job: `34898955784` / `104159961753`.

Observed adversarial sequence on the repaired G ancestry:

- Decision 020 adversarial gate: **passed**;
- Decision 022 adversarial gate: **passed**;
- ADV-058-A/B/C: **passed**;
- ADV-058-D: **passed**;
- ADV-058-E: **passed**;
- ADV-058-F: **passed**;
- ADV-058-G: **passed** — the prior object-path return-value counterexample is independently cleared;
- ADV-058-H: **failed**;
- Decision 023 focused suite: **skipped after H failure**;
- complete deterministic suite: **skipped after H failure**;
- explicit compile: **skipped after H failure**.

GitHub job metadata for this adversarial run exposes step conclusions but not unittest stdout counts, so this sequencing state does not invent per-step numerical counts for Lane 03 where they were not directly available.

The current PR #129 documentation descendant reran natively as run/job `34899135347` / `104160568471` and reproduced the same ordered result: all preserved gates through ADV-058-G passed, ADV-058-H failed, and the focused/full/compile stages were skipped. Its current GitHub merge candidate is `0ae0ddca983557c263afeea4be27f9c51a42a23f`.

ADV-058-H keeps the accepted exact `FilesystemObjectStore` type and stores the exact declared target in the supplied live store. The actual base-store path exists. The fixture leaves the store root, `objects_dir`, `load_bytes`, `_verify_existing`, and `schema_dir` unchanged, but shadows only the exact instance's `_object_path` so it raises `ObjectNotFoundError` for the target. Lane 02's G repair still invokes that caller-owned shadow before deriving the non-caller-owned base path. The exception therefore escapes before the grounded base-store read and is mapped by the observation layer to `not_found_in_live_context` even though the exact target is present.

## Lead finding

The Decision 023 blocker has moved from caller-owned path **return value** authority to caller-owned path **error** authority, but the institutional contradiction remains bounded:

> A caller-owned verification-critical `_object_path` dispatch must not establish either positive presence or negative absence for the supplied live store. A context-local absence fact requires grounding in the supplied base-store observation, not merely an exception raised by caller-controlled dispatch that contradicts the actual store state.

This is a Truth + Continuity contradiction inside Decision 023's already-open exact-store availability/validation contract. It also protects Agency/non-domination by preventing a hidden caller hook from silently becoming truth authority. It is not evidence that AXM needs a general hostile-process security architecture.

## PR disposition

- **PR #112 — keep open and held.** It owns the Decision 023 implementation and bounded repair sequence. Do not merge while ADV-058-H is red.
- **PR #129 — keep open as active adversarial evidence.** Do not merge its stacked Lane 02 ancestry as production history.
- **PR #127 — superseded, not invalidated.** Its ADV-058-G red evidence remains historical truth for the pre-G-repair surface. Lane 02 repaired G, and PR #129 preserves unchanged A/B/C/D/E/F/G before adding H. PR #127 may be closed after this sequencing state is canonical without erasing its evidence.

## Smallest next executable lane

### Lane 02 — repair ADV-058-H only

Repair only the demonstrated `_object_path` error-dispatch hole.

A caller-owned exact-instance `_object_path` shadow must not be allowed to establish either positive presence or negative absence for the supplied live store. The smallest acceptable repair is either:

- fail closed when that caller-owned verification-critical dispatch is present/raises; or
- ensure the non-caller-owned base-store path/read independently determines the observation even when the shadow raises.

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
- existing ADV-058-A/B/C/D/E/F/G expectations unchanged;
- ADV-058-H unchanged as the new regression oracle.

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
9. Decision 023 focused suite;
10. complete deterministic discovery;
11. explicit compile.

Record the exact semantic head, exact tested merge candidate, native run/job, environment, direct counts/step evidence, skipped checks if any, and uncertainty in the Lane 02 return packet.

### Lane 03 — independent recheck after repair

After Lane 02 publishes an exact H-repair semantic head, independently rerun ADV-058-A/B/C/D/E/F/G/H unchanged on that ancestry.

Attack another nearby path only if repository evidence demonstrates another contradiction inside Decision 023's already-open actual exact-store validation/availability contract. Do not turn the lane into open-ended same-process hardening.

### Lane 01 — integration hold

Do not merge Decision 023 until the H red -> bounded repair -> independent unchanged-oracle evidence chain is complete and the resulting surface remains grounded against Truth, Agency/non-domination, Continuity, and Wisdom before speed.

Green CI or Git permission alone is not integration authority.

## Historical evidence preserved

The current H blocker does not rewrite earlier evidence:

- ADV-058-A exposed bundled-schema substitution between capability classification and observation;
- ADV-058-B exposed caller-owned validation-context rebind/restore;
- ADV-058-C exposed exact-instance `load_bytes` replacement despite exact class identity;
- ADV-058-D exposed direct `store.__dict__['schema_dir']` rebinding around validation;
- ADV-058-E exposed caller-owned `load_bytes` success being accepted without actual exact-store verification;
- ADV-058-F exposed base `load_bytes` delegating verification through caller-shadowable `_verify_existing`;
- ADV-058-G exposed base verification locating material through caller-shadowable `_object_path`, allowing exact presence from another root to be imported into the supplied live-context fact;
- Lane 02 repaired each demonstrated A–G path on its exact tested surface before Lane 03 advanced;
- Lane 03 independently clears A–G on the latest repaired ancestry;
- ADV-058-H now shows that the G repair still invokes caller-owned `_object_path` error behavior before the grounded base path, allowing false context-local absence to be manufactured for a present target.

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
