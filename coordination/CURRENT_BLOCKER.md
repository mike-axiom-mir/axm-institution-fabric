# CURRENT BLOCKER — ADV-040 nested exact-relation continuity

Status: **active Stage 4 integration hold**.

This file is a narrow current-state overlay on `coordination/CURRENT_WAVE.md`; it does not replace the broader wave history or reopen downstream stages.

Canonical `main` inspected for this decision:

`887fb6655db9e77cc1ad8772276a404af42c770d`

## What changed in the evidence

Lane 02 repaired the earlier ADV-039 outer subject-binding wrapper failures on PR #45. Its exact tested implementation/workflow head is:

`ece5e4d936047800cdc1bf454b8e31cbc200ebb5`

Native Actions run `34762111896`, job `103736649169` completed with deterministic discovery success and explicit compile success. The numerical total `186` remains source-accounting inference rather than directly observed stdout for that repaired run.

Lane 03 then independently attacked that exact repaired head on PR #47. Exact adversarial head:

`cbdba1baa3df890516214bb34498cbc5c46e9017`

Exact tested PR merge candidate:

`61f79c0139f5129bbb8a2bb2a981791faf754442`

Native Actions run `34762800559`, job `103738460613`, Python 3.12.14 directly observed:

- **189 tests ran**;
- **exactly 3 failures**;
- failures were ADV-040-A, ADV-040-B, and ADV-040-C;
- all eight normal evidence-subject tests passed;
- ADV-039-A/B/C/D passed;
- ADV-035-A/B/C passed;
- ADV-036-A/B/C passed;
- ADV-037-A/B passed;
- ADV-038-A/B/C passed;
- explicit compile was skipped because unittest failed first.

Durable packet/artifact/evidence storage was not corrupted.

## Active contradiction

ADV-040 demonstrates that the ADV-039 `NamedTuple` repair closed the **outer** subject-binding projection but exposed a still-mutable lower operational relation layer already supplied by `packet_output_identity.py`:

1. `ExactPacketRelation` is a frozen dataclass whose `reference` or `value` can still be reassigned through `object.__setattr__`;
2. `ResolvedReturnPacketOutputIdentity` is a frozen dataclass whose relation tuples can still be reassigned through `object.__setattr__`;
3. therefore an exact ref/value pair can drift after verification, unrelated exact evidence can be laundered beneath an older exact evidence ref, or an exact evidence relation named by the durable packet can disappear from the operational relation set.

The canonical-byte-backed JSON value objects remain intact. The contradiction is specifically in the **metadata pairing exact refs with those values and in the nested exact relation set**.

This also narrows the truth claim around the already-canonical packet-output identity layer: its durable exact selection and canonical-byte-backed values remain demonstrated, but wrapper-level ref/value/relation continuity against `object.__setattr__` is now explicitly unresolved until ADV-040 is repaired.

## Integration decision

### PR #45 remains narrowly held

Do not merge the evidence-subject runtime while ADV-040-A/B/C remain reproducible.

The subject parser, exact created-artifact/evidence selection, unmatched-evidence semantics, wrong-kind fail-closed behavior, `artifact.evidence_refs` non-authority, and `artifacts_modified` fail-closed boundary remain grounded and should be preserved.

### PR #47 remains adversarial evidence

PR #47 changes no production runtime. Keep its exact ADV-040-A/B/C witnesses unchanged as the repair oracle.

### Downstream stages remain closed

Do not open multiple-`required_states` semantics, full packet compatibility, evidence/provenance closure, modified-artifact acceptance, claim closure, successor-state publication, integration receipts/runtime, epochs/barriers, or replay from this blocker.

## Smallest next implementation lane

**Lane 02** owns the repair.

Repair only the lower proof-to-use representation required by ADV-040 while preserving all already-grounded exact selection and value immutability behavior.

Required invariant:

> After exact verification, every operational exact relation must continue to pair the same exact immutable ref with the same exact immutable value, and the exact packet relation set used by later consumers must not silently lose or replace relations.

Acceptable implementation families include:

- a physically non-reassignable exact relation/result representation;
- reconstructing/re-verifying exact relations from durable canonical state at the consumption boundary;
- another bounded fail-closed mechanism that satisfies the invariant.

Do not make one Python container technique constitutional semantics.

Required repair evidence:

- ADV-040-A/B/C unchanged and green;
- ADV-039-A/B/C/D unchanged and green;
- all normal evidence-subject tests green;
- ADV-035/036/037/038 green;
- full native deterministic discovery green;
- explicit compile success.

Stop after this repair and hand the exact repaired head back to Lane 03 for a fresh nested/reconstruction attack before Lane 01 reconsiders canonical integration.

## Root grounding

- **Truth:** a verified exact ref must not later describe another value or an incomplete relation set while still being presented as authoritative.
- **Agency / non-domination:** caller access to a Python wrapper is not hidden authority to reassign evidence or exact identity.
- **Continuity:** a replacement occupant/process must reconstruct the same exact relation from durable state rather than inherit transient wrapper mutation.
- **Wisdom before speed:** Stage 5 and compatibility remain closed while this narrower contradiction is reproducible.

## Still unresolved

The existing frozen obligations in `coordination/CURRENT_WAVE.md` remain unresolved, including multiple required-state semantics, evidence quality/closure, exact artifact provenance base semantics, modified-artifact prior/result identity, currentness/supersession/authorization, multiple-packet conflict semantics, historical schema reconstruction, claim closure, successor revision publication, integration receipts/runtime, epochs/barriers, replay, cross-language reproduction, and stronger filesystem durability/concurrency evidence.
