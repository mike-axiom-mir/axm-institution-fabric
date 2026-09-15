# Lane 01 Return — Connected Monolith capability bridge

Date: 2026-09-15

## Base inspected

Canonical `main` at bridge start: `cb4f8d91693bbcb8fe00588b77bd2c0735ff5795`.

Existing Stage 5 work on PR #168 / PR #176 was treated as occupied and left unchanged. Scheduled Institution Fabric lanes were paused before this manual connection work.

## Bounded claim

Connect Institution Fabric to the user-supplied Connected Monolith as an **external discovery-only capability substrate** while preserving the deterministic kernel, current Stage-5 sequencing, source truth states, and authority boundaries.

This claim does not include capability execution.

## Exact external source

User-supplied archive: `AXM_Connected_Monolith_v0.3.2.zip`

- ZIP SHA-256: `f0a0d1d30007d71bb4ded6a9cc03259e5a12ceb7967cd532b12d366ae0cdf55e`
- `EXECUTION_FABRIC.json` SHA-256: `da1e384fc7107bfb70103d0c39e45e8fbe1b4eb3ecc19a77840bfd2c41ef05c4`
- `WORKFLOW_REGISTRY.json` SHA-256: `6659baf4a075c018858863db21cdc028586f62463db27a536bf49b1bb1ef5121`
- endpoint count: `23472`

Source adapter counts are preserved rather than upgraded:

- `blocked_missing_callable_binding`: 23248
- `blocked_missing_native_contract`: 68
- `callable_through_named_workflow`: 3
- `executable_inspection`: 87
- `executable_test_evidence`: 37
- `launchable_local_surface`: 29

## Connection demonstrated

Query:

- module = `axm-universal-creation`
- provides includes `capability.generated`

Exact result count: 1.

Exact result:

`axm-universal-creation::creation.universal`

The source execution fabric marks it callable only through named workflow `ghost-studio.blackline-3d.v0.4`, stage `brief-to-visual-recipe`. The same archive's workflow registry is independently cross-checked as callable and includes the exact endpoint among its stages.

The Institution projection remains `discovery_only_no_action_authority`.

## Files changed

- `axm_institution/connected_monolith.py`
- `axm_institution/__init__.py`
- `tools/query_connected_monolith_capabilities.py`
- `tests/test_connected_monolith.py`
- `fixtures/CONNECTED_MONOLITH_V0_3_2_CAPABILITY_EVIDENCE.json`
- `domain-packs/capability-substrates/connected-monolith/README.md`
- `.github/workflows/connected-monolith-bridge.yml`

## Evidence

Local/direct:

- exact uploaded ZIP hash verified;
- exact execution fabric and workflow registry inspected;
- full 23,472-endpoint catalog loaded without extraction or source execution;
- Creation Machine discovery query returned the one exact result above;
- focused adapter suite after workflow cross-check: 11/11 passed.

GitHub:

- first focused run failed because the new workflow omitted the repository's existing `jsonschema` test dependency; no adapter semantic failure was inferred from that environment/setup error;
- workflow repaired by installing the same bounded `jsonschema>=4.0,<5` dependency used by the existing deterministic workflow;
- subsequent focused bridge workflow passed tests and explicit compile;
- repository-wide deterministic workflow was requested by the touched kernel/test paths and must be green before merge.

## Truth boundary

This bridge proves capability discovery and source-status preservation only.

It does not establish:

- addressable = callable;
- wired = executable;
- executable test evidence = tests passed;
- launchable = runtime verified;
- source callability = Institution action permission;
- package integrity = semantic correctness;
- monolith status = AXM CANON;
- discovery = install / merge / network / source-mutation authority.

No Stage-5 mutation or existing Decision 026 branch was changed.

## Root review

- **Truth:** source states are preserved; unknown adapter/workflow semantics fail closed; exact package/fabric/workflow identities are recorded.
- **Agency / non-domination:** catalog output grants no action authority and exposes no execution operation.
- **Continuity:** source repository commits, package hashes, deterministic query inputs/results, and bounded evidence are persisted outside chat state.
- **Wisdom before speed:** the integration begins with discovery above the kernel; execution is a separate future contract rather than silently piggybacking on source callability.

## Next logical continuation

Only after this discovery bridge is integrated and a later explicit contract is grounded: define a bounded capability-invocation request that consumes a discovered fact while preserving lane scope, product/user authority, evidence obligations, and the four roots. Do not infer invocation permission from discovery alone.
