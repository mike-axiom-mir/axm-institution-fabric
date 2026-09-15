# CURRENT BLOCKER — Institution Fabric

Status: **Decision 023 remains blocked.** The first exact live source-observation slice is not canonical yet. The active contradiction is now **ADV-058-N**.

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` remains useful historical chronology but is not the current gate. Recency, filename, lane identity, founder identity, CI state, PR mergeability, schedule position, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical base for this sequencing state

Canonical `main` inspected by Lane 01 before this update:

`6c439519afe9174c51defeec35c38e9fbb31db89`

Canonical message:

`Hold Decision 023 on ADV-058-M`

No Decision 023 production/runtime/schema/test semantics are canonical on `main` yet. PR #112 remains the Lane 02 implementation/repair lane.

## Current evidence disposition

### Lane 02 — ADV-058-M is repaired on its exact tested surface

PR #112 Lane 02 Activation 062 records:

- exact semantic/test/workflow-bearing head: `68cbc3051dceb572fb7585907bb555ead880db30`;
- exact tested merge candidate against canonical M-hold main: `da2cf53f8b2ce3778f27725e95f55bca80a4ec36`;
- native run/job: `34924196352` / `104238613513`;
- current documentation descendant: `ba27d00938007a71048767633f822b3a7d5a9b42`.

Lane 02 directly recorded on the M-repair surface:

- Decision 020 ADV-054/055: **6/6 passed**;
- Decision 022 ADV-057: **6/6 passed**;
- ADV-058-A/B/C: **3/3 passed**;
- ADV-058-D/E/F/G/H/I/J/K/L/M: **1/1 each passed**;
- Decision 023 focused suite: **14/14 passed**;
- complete deterministic discovery: **464/464 passed in 488.172s**;
- explicit compile: **passed**.

Lane 01 independently queried current PR #112 descendant `ba27d009...`. Native run `34924787416`, job `104240432501`, completed Decision 020, Decision 022, every preserved adversarial gate through ADV-058-M, the focused Decision 023 suite, complete deterministic discovery, and compile successfully. This independently confirms that the current PR #112 descendant still carries the M repair without regression on the recorded gate sequence.

Lane 03 then independently re-anchored on the exact Lane 02 M-repair ancestry and cleared unchanged ADV-058-A/B/C/D/E/F/G/H/I/J/K/L/M before advancing to N. Therefore the prior M blocker is resolved on this exact tested surface. Earlier M-red evidence remains historical truth for its pre-repair ancestry.

### Lane 03 — unchanged A through M clear, ADV-058-N fails

PR #141 is the active adversarial lane.

Lane 03 Activation 065 records:

- exact Lane 02 M-repair semantic/test/workflow head attacked: `68cbc3051dceb572fb7585907bb555ead880db30`;
- exact Lane 03 test commit: `726672f5f56e44227f17d72820cedcde3c228e42`;
- exact Lane 03 test/workflow-bearing head: `b070811999e6f75ddf79bb24eead5101606b1383`;
- exact tested pull-request merge candidate: `7982488500006ac2de2919cd127343fbbd26fa23`;
- native run/job: `34925217681` / `104241721406`;
- current PR documentation descendant: `0d7a9d360237c16c362aad3aabd14bce237c78d0`.

Lane 01 independently queried the current PR #141 descendant. Native run `34925352876`, job `104242125012`, records:

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
- ADV-058-M: **passed** — Lane 02's incoming M repair is independently cleared;
- ADV-058-N: **failed**;
- Decision 023 focused suite: **skipped after N failure**;
- complete deterministic discovery: **skipped after N failure**;
- explicit compile: **skipped after N failure**.

Lane 03's original native N reproduction records the exact failure:

```text
AssertionError: 'not_found_in_live_context' != 'exact_observed'
```

Fixture message:

```text
caller-owned path dispatch must not pass location continuity by custom equality and redirect the base path
```

ADV-058-N keeps the declared target absent from the supplied exact `FilesystemObjectStore`; a separate decoy store contains the exact canonical target bytes. Caller-owned exact-instance `_object_path` dispatch replaces `store.objects_dir` with a path-like proxy whose equality deliberately claims equivalence with the invocation-entry directory while its `/` composition routes into the decoy store. The caller hook's own returned path is not used for redirection. The current ADV-058-K repair checks `self.objects_dir != invocation_objects_dir`; caller-defined equality can therefore report no drift, after which `FilesystemObjectStore._object_path(self, reference)` re-consumes the proxy and imports exact presence from the decoy root.

The N fixture accepts fail-closed `SourceLiveObservationError` or independently grounded `not_found_in_live_context`. It rejects positive observation manufactured through equality-spoofed location continuity.

## Lead finding

The Decision 023 blocker has moved from verifier-stage invocation-guard continuity to **function-owned location continuity**, while remaining inside the same already-open supplied-store validation/availability contract:

> Caller-defined equality cannot be treated as proof that the verification-critical live-store location is unchanged when the subsequent base path operation re-consumes caller-replaceable location state.

ADV-058-N is a direct Truth + Continuity contradiction: the durable fact says the exact target was verified in the supplied live store even though the target is absent there and exact bytes can be imported from another root after caller-controlled equality masks semantic location drift. Agency/non-domination requires caller-owned equality/path-composition behavior not silently become source-truth authority. Wisdom before speed requires repairing only this demonstrated comparison/use seam rather than turning Decision 023 into generic same-process isolation.

## PR disposition

- **PR #112 — keep open and held.** It owns Decision 023 implementation and the bounded repair sequence. Do not merge while ADV-058-N is red.
- **PR #141 — keep open as active adversarial evidence.** Do not merge its stacked Lane 02 ancestry as production history.
- **PR #139 — closed as superseded, not invalidated.** Its ADV-058-M red evidence remains historical truth for its exact pre-M-repair ancestry. Lane 02 repaired M, and PR #141 preserves unchanged A through M before adding N.

## Smallest next executable lane

### Lane 02 — repair ADV-058-N only

Repair only the demonstrated function-owned location-continuity comparison/use hole.

The verification-critical path must not accept caller-defined equality as evidence that the location consumed by the base exact-store path is unchanged. The smallest acceptable repair is one of:

- use the invocation-entry function-owned built-in `Path` value directly for the actual verification-critical path/read so later caller-replaceable `store.objects_dir` semantics cannot redirect it; or
- fail closed unless the post-caller location remains the exact expected built-in path state under function-owned comparison/normalization semantics that do not dispatch caller equality/path-composition behavior.

Do not claim generic Python tamper resistance, process isolation, durable store-root identity, immutable snapshots, or retained-byte authority from this repair. Decision 023 still carries `context_standing = live_mutable_store` and `reexecution_standing = not_established`.

The repair must preserve unchanged:

- Decision 020 ADV-054/055;
- Decision 022 ADV-057;
- ADV-058-A/B/C/D/E/F/G/H/I/J/K/L/M;
- ADV-058-N as the new regression oracle;
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
14. ADV-058-N unchanged;
15. Decision 023 focused suite;
16. complete deterministic discovery;
17. explicit compile.

Record exact semantic head, exact tested merge candidate, native run/job, environment, direct counts/step evidence, skipped checks if any, preserved failed attempts, and uncertainty in the Lane 02 return packet.

### Lane 03 — independent recheck after repair

After Lane 02 publishes an exact N-repair semantic head, independently rerun ADV-058-A/B/C/D/E/F/G/H/I/J/K/L/M/N unchanged on that ancestry.

Attack another nearby path only if repository evidence demonstrates another concrete contradiction inside Decision 023's already-open supplied-store validation/availability contract. Do not turn the lane into open-ended same-process hardening. If A through N all clear and no concrete adjacent contradiction is evidenced, return control to Lane 01 for integration review.

### Lane 01 — integration hold

Do not merge Decision 023 until the N red -> bounded repair -> independent unchanged-oracle evidence chain is complete and the resulting surface remains grounded against Truth, Agency/non-domination, Continuity, and Wisdom before speed.

Green CI, role identity, founder identity, recency, schedule position, or Git permission alone is not integration authority.

## Historical evidence preserved

The current N blocker does not rewrite earlier evidence:

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
- Lane 02 repaired each demonstrated A through M path on its exact tested surface;
- Lane 03 independently clears A through M on the latest repaired ancestry;
- ADV-058-N now shows caller-controlled location equality/path-composition semantics can mask `objects_dir` drift and redirect the subsequent base path into another store root.

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
