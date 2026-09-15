# CURRENT BLOCKER — Institution Fabric

Status: **Decision 023 remains blocked.** The first exact live source-observation slice is not canonical yet. The active contradiction is now **ADV-058-Q**.

This file is the current sequencing pointer. `coordination/CURRENT_WAVE.md` remains useful historical chronology but is not the current gate. Recency, filename, lane identity, founder identity, CI state, PR mergeability, schedule position, or Git permission are evidence/execution facts only; AXM's four roots remain the internal constitutional merge gate.

## Canonical base for this sequencing state

Canonical `main` inspected by Lane 01 before this update:

`c0edaadda0415841c2dcbc2bb2754e35345e20fd`

Canonical message:

`Hold Decision 023 on ADV-058-P`

No Decision 023 production/runtime/schema/test semantics are canonical on `main` yet. PR #112 remains the Lane 02 implementation/repair lane.

## Current evidence disposition

### Lane 02 — ADV-058-P is repaired on its exact tested surface

PR #112 Lane 02 Activation 065 records:

- source repair commit: `c8e77ee37a076d07a872dbf6a5ce9d6ecfe39941`;
- exact semantic/test/workflow-bearing head: `440a1861b7f1adf6c96a0f4db5ef85cac0a340d0`;
- exact tested merge candidate against canonical P-hold main: `25100c69b9d3c03d16f5e90b1dd11c9b63ba4075`;
- native run/job: `34936117362` / `104274274572`;
- environment: Ubuntu 24.04.5 LTS, CPython 3.12.14, jsonschema 4.26.0;
- documentation-only descendant / current PR #112 head at Lane 01 inspection: `14610250e9c2ab3b7c00146bed45a8ea36aab164`.

Lane 02 directly recorded on the P-repair surface:

- Decision 020 ADV-054/055: **6/6 passed**;
- Decision 022 ADV-057: **6/6 passed**;
- ADV-058-A/B/C: **3/3 passed**;
- ADV-058-D/E/F/G/H/I/J/K/L/M/N/O/P: **1/1 each passed**;
- Decision 023 focused suite: **14/14 passed**;
- complete deterministic discovery: **467/467 passed in 616.178s**;
- explicit compile: **passed**;
- no required step skipped.

The bounded P repair treats caller-owned `_verify_existing` `ObjectCorruptionError` like caller-owned not-found: that pre-dispatch exception is not sufficient to author `corrupt_material_in_live_context` / `failed_exact_identity`. The function-owned `FilesystemObjectStore._verify_existing(...)` path must independently determine actual presence and immutable identity. Actual corruption produced by the function-owned base verifier remains classified as corruption; other caller-raised store-layer failures retain conservative store-error handling.

Lane 01 also queried current PR #112 descendant `14610250...`. Native run `34937036349` completes successfully, confirming the documentation descendant still carries the P repair and its preserved workflow surface without an observed regression.

Lane 03 then independently re-anchored on exact Lane 02 P-repair semantic/test/workflow head `440a1861...` and cleared unchanged ADV-058-A/B/C/D/E/F/G/H/I/J/K/L/M/N/O/P before advancing to Q. Therefore the prior P blocker is resolved on this exact tested surface. Earlier P-red evidence remains historical truth for its pre-repair ancestry.

### Lane 03 — unchanged A through P clear, ADV-058-Q fails

PR #147 is the active adversarial lane.

Lane 03 Activation 068 records:

- exact Lane 02 P-repair semantic/test/workflow head attacked: `440a1861b7f1adf6c96a0f4db5ef85cac0a340d0`;
- exact corrected Lane 03 test/workflow-bearing head: `18d666d419bcc539057cedb66e2c639764c9fb1c`;
- exact tested pull-request merge candidate: `4aa69ff119a340a4a27d1bb4245072dd7aa5f4e3`;
- corrected native run/job: `34937496621` / `104278503500`;
- environment: Ubuntu 24.04.5 LTS, CPython 3.12.14, jsonschema 4.26.0;
- documentation descendant / current PR #147 head at Lane 01 inspection: `6558fda24f96ec4846a87d917c52172ba4bbf010`.

The corrected Lane 03 native run records:

- Decision 020 ADV-054/055: **6/6 passed**;
- Decision 022 ADV-057: **6/6 passed**;
- ADV-058-A/B/C: **3/3 passed**;
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
- ADV-058-O: **passed**;
- ADV-058-P: **passed** — Lane 02's incoming P repair is independently cleared;
- ADV-058-Q: **failed**;
- Decision 023 focused suite: **skipped after Q failure**;
- complete deterministic discovery: **skipped after Q failure**;
- explicit compile: **skipped after Q failure**.

The corrected Q run records the exact semantic failure:

```text
AssertionError: 'corrupt_material_in_live_context' == 'corrupt_material_in_live_context' : caller mutation of the observer-owned schema snapshot must not forge material corruption
```

ADV-058-Q keeps the exact target genuinely present and canonical in the supplied exact `FilesystemObjectStore`. The caller-owned exact-instance `_verify_existing` shadow does not alter target bytes/path, the store root, `objects_dir`, the ambient bundled schema set, or the `schema_dir` binding. Instead, while the observer's invocation guard exposes the function-owned temporary schema directory through `store.schema_dir`, the caller hook mutates that temporary snapshot's `artifact.schema.json` in place to another valid schema that rejects the target, then returns normally. The later function-owned base verifier consumes those caller-mutated interpretation bytes and can emit `corrupt_material_in_live_context` / `failed_exact_identity` even though the supplied target remains valid under the interpretation captured for capability classification.

Binding continuity (`schema_dir` still names the same temporary directory) is therefore insufficient to establish interpretation-content continuity.

Lane 01 independently queried the current PR #147 documentation descendant. Native run `34937597207`, job `104278807521`, again passes Decision 020, Decision 022, every preserved adversarial gate through P, fails Q, and skips focused Decision 023, full discovery, and compile after the targeted red. This confirms the active branch still carries the corrected Q contradiction.

Lane 03 also preserves an earlier invalid fixture attempt instead of rewriting it away: preliminary head `de9197be1487ac6fc5f1c4c5aac80976329aff56`, run/job `34937368343` / `104278113536`, failed because the test incorrectly asserted `type(PosixPath) is Path`. That preliminary failure is **not** semantic evidence for Q. The corrected test-only assertion at `18d666d...` is the evidence-bearing reproduction above.

## Lead finding

The Decision 023 blocker has moved from caller exception authority to interpretation-content continuity inside the same already-open function-owned invocation schema context:

> A durable `corrupt_material_in_live_context` / `failed_exact_identity` fact cannot be grounded by a function-owned base verifier if the interpretation bytes that verifier consumes were made caller-mutable after capability classification without an independent continuity check or fail-closed boundary.

ADV-058-Q is a direct Truth + Continuity contradiction: the durable fact can say the supplied exact source failed identity verification while the actual target remains valid under the interpretation captured for the same observation's capability classification. Agency/non-domination requires caller-visible dispatch not silently gain authority to rewrite the observer's interpretation context and thereby author institutional source truth. Wisdom before speed requires repairing only this demonstrated invocation-local snapshot-content seam rather than expanding Decision 023 into generic process isolation or historical snapshot authority.

## PR disposition

- **PR #112 — keep open and held.** It owns Decision 023 implementation and the bounded repair sequence. Do not merge while ADV-058-Q is red.
- **PR #147 — keep open as active adversarial evidence.** Do not merge its stacked Lane 02 ancestry as production history.
- **PR #145 — close as superseded, not invalidated.** Its ADV-058-P red evidence remains historical truth for its exact pre-P-repair ancestry. Lane 02 repaired P, and PR #147 preserves unchanged A through P before adding Q.

## Smallest next executable lane

### Lane 02 — repair ADV-058-Q only

Repair only the demonstrated invocation-local schema snapshot **content continuity** seam.

The smallest acceptable repair is to ensure caller-visible dispatch cannot alter the interpretation bytes later consumed by the function-owned base verifier without detection/fail-closed behavior. A bounded implementation may:

- re-establish the exact function-owned schema snapshot contents against a function-owned token after caller dispatch and before the base verifier consumes them; or
- feed the base validation path interpretation material whose invocation-local bytes cannot be changed through the demonstrated caller-visible path.

Do not weaken actual base-store corruption detection. Do not claim generic Python tamper resistance, process isolation, durable schema/store-root identity, retained-byte authority, historical snapshots, trust/closure, Stage 5 integration, epochs/barriers, or replay from this repair. Decision 023 still carries `context_standing = live_mutable_store` and `reexecution_standing = not_established`.

The repair must preserve unchanged:

- Decision 020 ADV-054/055;
- Decision 022 ADV-057;
- ADV-058-A/B/C/D/E/F/G/H/I/J/K/L/M/N/O/P;
- ADV-058-Q as the new regression oracle;
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
17. ADV-058-Q unchanged;
18. Decision 023 focused suite;
19. complete deterministic discovery;
20. explicit compile.

Record exact semantic head, exact tested merge candidate, native run/job, environment, direct counts/step evidence, skipped checks if any, preserved failed attempts, and uncertainty in the Lane 02 return packet.

### Lane 03 — independent recheck after repair

After Lane 02 publishes an exact Q-repair semantic/test head, independently rerun ADV-058-A/B/C/D/E/F/G/H/I/J/K/L/M/N/O/P/Q unchanged on that ancestry.

Attack another nearby path only if repository evidence demonstrates another concrete contradiction inside Decision 023's already-open supplied-store observation / same-invocation interpretation-coherence contract. Do not turn the lane into open-ended same-process hardening. If A through Q all clear and no concrete adjacent contradiction is evidenced, return control to Lane 01 for integration review.

### Lane 01 — integration hold

Do not merge Decision 023 until the Q red -> bounded repair -> independent unchanged-oracle evidence chain is complete and the resulting surface remains grounded against Truth, Agency/non-domination, Continuity, and Wisdom before speed.

Green CI, role identity, founder identity, recency, schedule position, or Git permission alone is not integration authority.

## Historical evidence preserved

The current Q blocker does not rewrite earlier evidence:

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
- ADV-058-P exposed caller-owned `_verify_existing` corruption-error choice manufacturing material-corruption / failed-identity before the function-owned verifier grounded exact identity;
- Lane 02 repaired each demonstrated A through P path on its exact tested surface;
- Lane 03 independently clears A through P on the latest repaired ancestry;
- ADV-058-Q now shows caller mutation of the observer-owned invocation schema snapshot can alter the interpretation bytes later consumed by the function-owned base verifier and manufacture material-corruption / failed-identity.

Each red remains valid for its exact pre-repair ancestry. Each green remains valid for its exact tested repaired surface. Neither class of evidence erases the other.

## Unresolved boundary — still explicitly unopened

Decision 023 does not establish:

- general hostile same-process code isolation;
- durable identity for the live store root;
- durable identity for the bundled/schema interpretation root;
- immutable/historical source-observation context identity or completeness;
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
