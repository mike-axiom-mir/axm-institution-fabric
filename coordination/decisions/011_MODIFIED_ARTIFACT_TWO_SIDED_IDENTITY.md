# Decision 011 — Modified Artifact Two-Sided Identity

Status: **accepted as the next bounded Stage 4 identity precondition**. This decision defines only the minimum exact relationship needed to stop `artifacts_modified[]` from depending on hidden interpretation. It does not open packet acceptance, claim closure, successor publication, Stage 5 integration, epochs, or replay.

## Problem

The current return-packet contract (`schema_version: 0.3`) represents each `artifacts_modified[]` entry as one opaque string.

The canonical output-identity runtime therefore fails closed on every non-empty modified-artifact list, because one value cannot truthfully establish both:

1. the exact immutable artifact instance observed before the modification; and
2. the exact immutable artifact instance produced by the work.

This is not a formatting inconvenience. A replacement occupant must be able to reconstruct which exact prior object was changed and which exact result was returned without relying on logical-id lookup, newest/current state, storage order, array order, private chat memory, actor identity, or an ungrounded `supersedes_ref` convention.

Decision 010 now gives packet-created artifact results an exact claim-base provenance precondition, but it does not repair the missing prior/result pair. Artifact `supersedes_ref` also remains a generic string and is not promoted to exact lineage authority by this decision.

## Decision

For the bounded v0 modification path, one operational modified-artifact relation must explicitly carry **two canonical exact immutable artifact references**:

```text
modified relation M
    -> exact prior_artifact_ref A0
    -> exact result_artifact_ref A1
```

The relation must be represented explicitly in the return-packet contract rather than reconstructed from artifact ids, versions, storage order, recency, or another field whose semantics are not yet grounded.

### Prior side

For this v0 path, `A0` is a pre-existing institutional artifact observed from the exact work-claim base. Therefore:

```text
exact packet P
    -> exact claim C
    -> exact claim base B
    -> B.artifact_refs contains exact A0
```

The kernel must exact-load and identity-verify `A0` through the canonical revision membership/store path. Same-logical-id alternatives elsewhere do not substitute.

If a future workflow needs to modify an artifact created after the claim base, that is a different chronology and must be grounded explicitly rather than silently weakening this rule.

### Result side

`A1` is the produced post-base result. It must exact-load as an artifact and satisfy the already-canonical Decision 010 created-artifact work-base provenance precondition against the same exact claim base and claim-base lane.

This decision does **not** require the prior and result to share a logical id, version convention, content-ref scheme, or `supersedes_ref` rule. Those lineage semantics remain unresolved and must not be invented merely to make the pair convenient.

## Contract migration boundary

Historical return-packet schema v0.3 remains historical truth. Its one-string `artifacts_modified[]` entries must not be silently reinterpreted as two-sided exact relations.

The next implementation may introduce an explicit newer packet schema in which a modified entry has an unambiguous structural shape such as:

```json
{
  "prior_artifact_ref": "<exact artifact ref>",
  "result_artifact_ref": "<exact artifact ref>"
}
```

Exact field spelling/version is an implementation detail only if the resulting contract preserves the invariant above and retains explicit historical behavior. No dual authority between old opaque entries and new exact relations is permitted.

## What this proves if implemented

Only this bounded statement:

> For each packet-declared modification used operationally, the kernel can reconstruct the exact prior artifact from the exact claim base and the exact produced result from an explicit immutable ref, without hidden selection authority.

It does not prove:

- that the prior/result represent the same logical artifact;
- that the result validly supersedes the prior;
- stale/current authorization beyond exact claim-base membership;
- source/dependency closure;
- evidence conflict or evidence closure policy;
- packet acceptance;
- claim closure;
- successor state publication;
- integration receipts/runtime;
- epochs/barriers;
- replay.

## Required next implementation behavior

Lane 02 should implement only the smallest two-sided identity precondition:

1. preserve historical packet v0.3 meaning without reinterpretation;
2. introduce an explicit newer packet shape for modified relations only if versioning can remain unambiguous;
3. parse both refs through the shared Stage 2 immutable-ref parser and require kind `artifact`;
4. reconstruct the exact claim base already grounded by the packet lifecycle;
5. require the exact prior ref to be an exact member of that base revision;
6. exact-load the exact result ref;
7. apply Decision 010 work-base/producer-lane provenance to that result;
8. preserve all current created-output/evidence/provenance regressions;
9. remain read-only and stop before lineage, acceptance, closure, successor publication, or integration.

If the existing contracts cannot express this migration without ambiguous old/new authority, stop with an explicit blocker rather than guessing.

## Adversarial surface for Lane 03

Attack the exact Lane 02 head for:

- same logical prior id / different exact base member substitution;
- prior exact artifact not present in the exact claim base;
- same logical result id / different exact result substitution;
- result provenance tied to another exact revision;
- wrong-kind or noncanonical refs on either side;
- missing/corrupt prior or result targets;
- array-order, newest/current, storage-order, actor, scheduler, or founder authority;
- historical v0.3 one-string entries accidentally acquiring new exact meaning;
- `supersedes_ref` or version fields silently overriding the explicit pair.

## Root grounding

- **Truth:** one opaque value is not relabelled as proof of two immutable objects; historical packet meaning remains explicit.
- **Agency / non-domination:** no actor identity, recency, scheduler position, founder status, or Git permission chooses the prior/result relation.
- **Continuity:** a replacement occupant can reconstruct both sides from durable exact state rather than private execution history.
- **Wisdom before speed:** repair the minimum identity gap first and leave lineage, acceptance, integration, epochs, and replay closed until their evidence exists.
