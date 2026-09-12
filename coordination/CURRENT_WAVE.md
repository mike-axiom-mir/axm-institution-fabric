# CURRENT WAVE — Institution Fabric

Status: active initial build wave — Stage 1 contract layer integrated; Stage 2 identity implementation in final bounded canonical-string portability repair

## Shared objective

Turn the research scaffold into the smallest executable deterministic institution kernel without losing the universal boundary or pretending the v0 proof is complete before replayable evidence exists.

## Current integration state

- Lane 03 adversarial PR #2 is integrated at `51f93a940e54c19de7d732b5ccb574e95f3a28f3`.
- Lane 01 Decision 001 / first integration wave is integrated at `6c5314d6e2828a32ad9eacd2815a16ed5515a1de`.
- Lane 02 canonical contract PR #3 is integrated at `cff616caf84ded88f79580a51df3e14fdf585b3e`.
- Lane 03 cross-object continuity PR #5 is integrated at `c4904ee7ce508cfa6e1dccacb5f9a6ab2edd379b`.
- Decision 002 defines immutable subject/reference identity requirements.
- Lane 03 Stage 2 canonicalization-oracle PR #6 is integrated at `aaf32fa6d2e3e4f81e80464e051386247b55c83d`.
- Lane 03 exact-code portability PR #8 is integrated at `ffacf03d33dd010cd88e11dfb11dc09597fb8900`.
- Decision 003 defines Unicode scalar-value object-key ordering and UTF-8-byte `axmref:v1` component spelling.
- Lane 02 production identity PR #7 is open at repaired head `b5d965eda605fe215ebb1411864b7f2a539d9bca`.
- Lane 02 reports fresh local reconstructed-harness evidence for that head: `23 passed` plus successful `py_compile`; native checkout and remote CI remain not tested.
- Lane 03 exact-head verification confirms the Decision 003 repairs survive source/doc/test inspection and targeted witnesses.
- Lane 03 PR #9 is integrated at `49095fe3d616758997c991d81f695ceb7a4afffe`, freezing `ADV-023-A`: canonical JSON string escape spelling remained under-specified because production string rendering still inherited `json.dumps` behavior not fully externalized in repository semantics.
- Decision 004 (`004_CANONICAL_STRING_ESCAPE_SEMANTICS.md`) is integrated at `53c78aa64f80555539768c762bb94cc8236379cb` and freezes the exact Stage 2 JSON string spelling while preserving current intended Python output.
- PR #7 is now behind current `main` and reports `mergeable: false`; publication freshness and semantic acceptance remain separate concerns.
- Stage 2 is **not integrated yet**. The current gate is one narrow Lane 02 Decision 004 repair + fresh evidence + one bounded Lane 03 exact-head verification.
- State-store, work-ledger, stale-base enforcement, supersession graph validation, epoch runtime, integration runtime, and replay remain deferred.

## Lane 01 — Institution Architect / Integration Lead

Active claim:

- preserve architecture, root boundary, and universal-vs-domain separation;
- hold Stage 2 integration until Decision 004 is encoded and verified;
- keep host-runtime behavior from becoming hidden institutional semantics;
- keep evidence states precise and avoid promoting test evidence from an older blob onto changed code;
- maintain repository coordination so later occupants can continue without private chat memory;
- integrate only grounded, non-overlapping specialist work.

Current hold: do not integrate PR #7 until Decision 004 is explicit in docs/code/tests, fresh deterministic evidence is recorded for the changed head, Lane 03 verifies the exact repaired head, and the branch is reconciled/mergeable.

Avoid duplicating Lane 02's production repair or Lane 03's verification lane.

## Lane 02 — Deterministic Kernel Engineer

Current claim: **repair PR #7 against Decision 004, then reconcile it onto current `main`**.

Immediate next action:

1. keep the existing Stage 2 implementation scope;
2. externalize Decision 004 canonical JSON string spelling in `IDENTITY_V0.md` and production behavior rather than treating Python `json.dumps` behavior as the contract;
3. preserve current intended spelling: literal `/`, `\"` for quotation mark, `\\` for reverse solidus, short escapes for `U+0008/U+0009/U+000A/U+000C/U+000D`, lowercase-hex `\u00xx` for other `U+0000..U+001F`, and literal UTF-8 for all other permitted scalar values;
4. add exact regressions at minimum for `ADV-023-A` literal solidus, one short control escape, one non-short control escape containing `a-f`, and one non-ASCII literal witness;
5. preserve the already-verified Decision 003 regressions for `ADV-021-A` and `ADV-022-A`;
6. rerun the full deterministic identity suite and compilation checks after the changed blobs and record exact evidence;
7. reconcile the repaired branch onto current `main` without beginning Stage 3.

Preserve already-grounded Stage 2 properties:

- strict duplicate-key rejection;
- explicit NFC/no-surrogate policy;
- no silent schema-default insertion;
- typed immutable references rather than bare digests;
- logical id distinct from immutable instance identity;
- exact strong-evidence subject binding;
- Unicode scalar-value object-key ordering;
- UTF-8 byte / uppercase `%HH` reference component spelling.

Do **not** start the state store, work ledger, integration engine, model adapter, networking, UI, or Game Studio expansion in this repair.

## Lane 03 — Institutional Continuity / Adversarial Systems Specialist

Current claim: **verify the exact Decision 004 repaired PR #7 head after Lane 02 publishes it**.

Verified repairs to preserve:

- `ADV-021-A` — Unicode scalar-value object-key ordering is explicit and survives exact-head verification;
- `ADV-022-A` — UTF-8 byte / uppercase `%HH` reference spelling is explicit and survives exact-head verification.

Integrated new finding:

- `ADV-023-A` — canonical JSON string escape spelling must be reconstructable independently of host serializer ancestry.

When Lane 02 repairs PR #7:

- confirm Decision 004 is encoded coherently in docs/code/tests;
- challenge literal solidus, quote/reverse-solidus spelling, short controls, non-short controls with lowercase hex, and literal non-ASCII output on the exact new head;
- confirm fresh test evidence corresponds to the changed blobs;
- preserve the Decision 003 negative findings accurately;
- do not pull Stage 3 stale-state, lineage, epoch, integration, or replay obligations into this bounded verification;
- if no new Stage 2 portability failure is found, leave an explicit verification return packet rather than inventing work.

Later integrated oracles that remain out of Stage 2 scope:

- `ADV-002-B` — stale packet/target detection;
- `ADV-011-B` — epoch packet/base coherence and replayable progression;
- `ADV-006-B` — immutable supersession lineage is resolvable and acyclic.

## Coordination cadence

Recommended stagger for recurring activations:

- Lane 01 lead: minute `:57`
- Lane 02 kernel: minute `:12`
- Lane 03 adversarial: minute `:27`

Typical flow:

```text
lead/integration -> kernel implementation -> adversarial challenge -> integration window -> next lead cycle
```

Timing is coordination convenience only and grants no authority.

## Shared return-packet minimum

Each lane should leave:

- base commit/revision inspected;
- bounded claim;
- files changed;
- evidence/test results;
- uncertainty/blockers;
- dependency/downstream effects;
- next recommended action;
- explicit status such as proposed / implemented / automated_tested / runtime_tested / measured / inferred / blocked / not_tested.

## Merge boundary

Inside AXM, the four roots remain the constitutional merge gate:

1. Truth
2. Agency / non-domination
3. Continuity
4. Wisdom before speed

No lane, founder, model, specialist, schedule position, or Git permission becomes authority by identity. When evidence is insufficient, preserve uncertainty or dissent instead of converting confidence into canon.
