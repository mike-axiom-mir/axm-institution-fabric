# Connected Monolith Capability Substrate

Status: **bounded discovery adapter / no execution authority**

This bridge lets Institution Fabric inspect a Connected Monolith `EXECUTION_FABRIC.json` as an external capability substrate without extracting or executing the monolith. When the input is a ZIP, callable named-workflow routes are also cross-checked against that same package's `WORKFLOW_REGISTRY.json`.

It exists so a lane can answer questions such as:

- which exact capability addresses are present;
- what each endpoint accepts and provides;
- whether the source snapshot marks the endpoint blocked, inspectable, test-entrypoint-evidenced, launchable, or callable through a named workflow;
- whether a claimed callable endpoint actually appears in the package's callable named workflow;
- which repository commit the source endpoint came from;
- which exact monolith ZIP, execution-fabric bytes, and workflow-registry bytes were inspected.

It does **not** let discovery become authority.

## First real connection

The adapter was exercised against the user-supplied `AXM_Connected_Monolith_v0.3.2.zip`.

Observed exact package facts:

- ZIP SHA-256: `f0a0d1d30007d71bb4ded6a9cc03259e5a12ceb7967cd532b12d366ae0cdf55e`
- `EXECUTION_FABRIC.json` SHA-256: `da1e384fc7107bfb70103d0c39e45e8fbe1b4eb3ecc19a77840bfd2c41ef05c4`
- `WORKFLOW_REGISTRY.json` SHA-256: `6659baf4a075c018858863db21cdc028586f62463db27a536bf49b1bb1ef5121`
- execution-fabric schema: `axm.monolith.execution-fabric/v0.1`
- endpoints: `23,472`
- statuses:
  - `23,248` blocked missing callable binding
  - `68` blocked missing native contract
  - `3` callable through named workflow
  - `87` executable inspection surfaces
  - `37` executable test-evidence surfaces
  - `29` launchable local surfaces

A query for module `axm-universal-creation` providing `capability.generated` returns exactly one endpoint:

`axm-universal-creation::creation.universal`

The execution fabric marks that endpoint `callable_through_named_workflow` through workflow `ghost-studio.blackline-3d.v0.4`, stage `brief-to-visual-recipe`. The ZIP loader additionally verifies that `WORKFLOW_REGISTRY.json` marks that workflow callable and contains the exact endpoint address among its stages.

That means the Building can now **discover the Creation Machine route truthfully**. It does not mean arbitrary Universal Creation calls are authorized, that unrelated monolith compositions are executable, or that the institution may automatically invoke the route.

The compact evidence is stored in `fixtures/CONNECTED_MONOLITH_V0_3_2_CAPABILITY_EVIDENCE.json`. The 194 MB ZIP is intentionally not copied into this repository.

## Local use

```bash
python tools/query_connected_monolith_capabilities.py \
  AXM_Connected_Monolith_v0.3.2.zip \
  --expected-zip-sha256 sha256:f0a0d1d30007d71bb4ded6a9cc03259e5a12ceb7967cd532b12d366ae0cdf55e \
  --module axm-universal-creation \
  --provides capability.generated
```

The command reads the ZIP directly and does not extract or execute module contents.

## Institution truth mapping

The bridge preserves the monolith status instead of upgrading it:

| Source status | Institution standing |
| --- | --- |
| `blocked_missing_callable_binding` | blocked; declaration is not callable |
| `blocked_missing_native_contract` | blocked; native contract missing |
| `executable_inspection` | inspectable, not source execution |
| `executable_test_evidence` | test entrypoints discovered, **not tests passed** |
| `launchable_local_surface` | launch surface discovered, **not runtime verified** |
| `callable_through_named_workflow` | source-callable only through the exact named workflow/stage |

Every returned fact also carries `institution_action_authority = discovery_only_no_action_authority`.

The adapter intentionally has no `execute()`, `install()`, `merge()`, `canon()`, network, or source-mutation operation.

## Why this belongs above the kernel

Institution Fabric's deterministic kernel should remain independent of one capability source. The Connected Monolith is therefore treated as an **external capability substrate**:

```text
lane objective
   -> capability query
   -> Connected Monolith discovery adapter
   -> exact capability facts + source standing
   -> lane judgment / work claim
   -> later explicit invocation adapter (not built here)
```

This allows a future software, research, game, 3D, hardware, or other domain package to reuse the same institution while discovering different tool surfaces.

## Explicit non-claims

This bridge does not claim:

- addressable = callable;
- wired composition = executable composition;
- test entrypoint discovered = tests passed;
- launchable surface = runtime verified;
- source callability = institution permission;
- monolith integrity = semantic correctness;
- monolith status = AXM CANON;
- capability discovery = merge authority;
- the three-stage Blackline workflow makes unrelated endpoints callable.

A later bridge may convert a grounded capability fact into a bounded invocation request. That later step must preserve user/product authority, lane contracts, evidence obligations, and the four AXM roots rather than silently treating discovery as execution permission.
