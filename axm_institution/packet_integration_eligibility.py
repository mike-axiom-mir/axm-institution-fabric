from __future__ import annotations

from typing import NamedTuple

from .packet_artifact_provenance import preflight_exact_artifact_work_base_provenance
from .packet_mixed_compatibility import (
    ResolvedMixedPacketCompatibility,
    preflight_mixed_packet_compatibility,
)
from .store import FilesystemObjectStore


ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE = "eligible_for_stage5_acceptance_candidate"
NOT_ELIGIBLE_UNSATISFIED_OUTPUT_EVIDENCE = "not_eligible_unsatisfied_output_evidence"
NOT_ELIGIBLE_CONFLICTING_SUBJECT_EVIDENCE = "not_eligible_conflicting_subject_evidence"
UNSUPPORTED_MODIFIED_OUTPUT_SLICE = "unsupported_modified_output_slice"
UNSUPPORTED_DEPENDENCY_POLICY = "unsupported_dependency_policy"


class PacketIntegrationEligibilityError(Exception):
    """Internal consistency failure while composing Decision 024 facts."""


class PacketIntegrationEligibilityReason(NamedTuple):
    """Deterministic reason fact for one Decision 024 eligibility disposition."""

    code: str
    artifact_ref: str | None
    required_state: str | None
    observed_states: tuple[str, ...]
    related_refs: tuple[str, ...]


class PacketReportedFacts(NamedTuple):
    """Packet-authored text preserved as exact historical facts, without authority."""

    uncertainties: tuple[str, ...]
    failures_or_blockers: tuple[str, ...]
    downstream_effects: tuple[str, ...]
    requested_followup: tuple[str, ...]


class ResolvedPacketIntegrationEligibility(NamedTuple):
    """Read-only Decision 024 first-slice eligibility projection.

    ``eligibility_outcome`` is not packet acceptance. A positive result means only that
    the exact packet fits Decision 024's first bounded Stage 5 acceptance-candidate
    slice. No canonical state mutation, claim closure, successor publication,
    integration receipt, epoch, replay, source trust/closure, dependency admissibility,
    mutable currentness, actor authority, schedule authority, CI authority, branch
    authority, or Git authority is established here.
    """

    packet_ref: str
    base_state_revision_ref: str
    claim_ref: str
    lane_ref: str
    created_output_refs: tuple[str, ...]
    unmatched_evidence_refs: tuple[str, ...]
    eligibility_outcome: str
    reasons: tuple[PacketIntegrationEligibilityReason, ...]
    packet_reported_facts: PacketReportedFacts


def _reason_sort_key(reason: PacketIntegrationEligibilityReason):
    return (
        reason.code,
        reason.artifact_ref or "",
        reason.required_state or "",
        reason.observed_states,
        reason.related_refs,
    )


def _packet_reported_facts(packet) -> PacketReportedFacts:
    return PacketReportedFacts(
        uncertainties=tuple(packet.get("uncertainties", ())),
        failures_or_blockers=tuple(packet.get("failures_or_blockers", ())),
        downstream_effects=tuple(packet.get("downstream_effects", ())),
        requested_followup=tuple(packet.get("requested_followup", ())),
    )


def _result(
    *,
    mixed: ResolvedMixedPacketCompatibility,
    packet,
    outcome: str,
    reasons: tuple[PacketIntegrationEligibilityReason, ...],
) -> ResolvedPacketIntegrationEligibility:
    return ResolvedPacketIntegrationEligibility(
        packet_ref=mixed.packet_ref,
        base_state_revision_ref=mixed.claim_base_ref,
        claim_ref=mixed.claim_ref,
        lane_ref=mixed.lane_ref,
        created_output_refs=tuple(
            sorted(item.artifact.reference for item in mixed.created_outputs)
        ),
        unmatched_evidence_refs=tuple(
            sorted(item.evidence.reference for item in mixed.unmatched_evidence)
        ),
        eligibility_outcome=outcome,
        reasons=tuple(sorted(reasons, key=_reason_sort_key)),
        packet_reported_facts=_packet_reported_facts(packet),
    )


def preflight_packet_integration_eligibility(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedPacketIntegrationEligibility:
    """Compose Decision 024's first read-only packet eligibility fact.

    Existing Stage 4 preflights remain the authority for exact packet/claim/base/
    occupancy/lane reconstruction, exact output identity, exact subject-bound evidence,
    and lane/output compatibility. This projection adds only the Decision 024
    composition rule:

    * modified outputs are explicitly outside the first created-only slice;
    * at least one created output is required;
    * each created artifact must pass Decision 010 exact work-base / producer-lane
      provenance against the same exact claim base and lane;
    * any non-empty created-artifact ``dependency_refs`` array is explicitly unsupported;
    * a created output with no exact required-state evidence is not eligible;
    * when required-state evidence exists, any additional exact-subject evidence in a
      different state makes the packet conflict-bound rather than choosing a winner;
    * packet uncertainty/blocker/downstream/follow-up text is preserved as fact and does
      not silently become a universal rejection rule.

    When multiple non-positive facts coexist, the returned label uses a deterministic
    boundary order only to name the projection: modified-slice boundary, dependency-policy
    boundary, evidence conflict, then evidence absence. Every detected evidence reason is
    retained, so this ordering does not rank one evidence state over another.

    The function is read-only and deliberately does not establish acceptance, root
    approval, source trust/closure, dependency satisfaction/closure, mutable/global
    currentness, claim closure, successor publication, integration, epochs, or replay.
    """

    mixed = preflight_mixed_packet_compatibility(store, packet_ref)
    packet = store.load(packet_ref, "return-packet.schema.json")

    if mixed.modified_results or packet.get("artifacts_modified"):
        modified_refs = tuple(
            sorted(
                item.modification.result_artifact.reference
                for item in mixed.modified_results
            )
        )
        return _result(
            mixed=mixed,
            packet=packet,
            outcome=UNSUPPORTED_MODIFIED_OUTPUT_SLICE,
            reasons=(
                PacketIntegrationEligibilityReason(
                    code="modified_outputs_present",
                    artifact_ref=None,
                    required_state=None,
                    observed_states=(),
                    related_refs=modified_refs,
                ),
            ),
        )

    if not mixed.created_outputs:
        return _result(
            mixed=mixed,
            packet=packet,
            outcome=NOT_ELIGIBLE_UNSATISFIED_OUTPUT_EVIDENCE,
            reasons=(
                PacketIntegrationEligibilityReason(
                    code="created_output_required",
                    artifact_ref=None,
                    required_state=None,
                    observed_states=(),
                    related_refs=(),
                ),
            ),
        )

    # Decision 010 remains the provenance authority. Let its existing typed failures
    # propagate instead of converting provenance mismatch into a new local policy.
    for output in mixed.created_outputs:
        preflight_exact_artifact_work_base_provenance(
            store,
            output.artifact,
            claim_base_ref=mixed.claim_base_ref,
            lane_ref=mixed.lane_ref,
        )

    dependency_reasons: list[PacketIntegrationEligibilityReason] = []
    for output in mixed.created_outputs:
        dependency_refs = output.artifact.value.get("dependency_refs", ())
        if dependency_refs:
            dependency_reasons.append(
                PacketIntegrationEligibilityReason(
                    code="created_output_dependencies_present",
                    artifact_ref=output.artifact.reference,
                    required_state=None,
                    observed_states=(),
                    related_refs=tuple(sorted(dependency_refs)),
                )
            )
    if dependency_reasons:
        return _result(
            mixed=mixed,
            packet=packet,
            outcome=UNSUPPORTED_DEPENDENCY_POLICY,
            reasons=tuple(dependency_reasons),
        )

    binding_by_ref = {
        binding.artifact.reference: binding for binding in mixed.created_bindings
    }
    evidence_reasons: list[PacketIntegrationEligibilityReason] = []
    has_conflict = False
    has_unsatisfied = False

    for output in mixed.created_outputs:
        binding = binding_by_ref.get(output.artifact.reference)
        if binding is None:
            raise PacketIntegrationEligibilityError(
                "mixed compatibility did not expose an evidence binding for a created output"
            )

        subject_evidence = tuple(binding.evidence_records)
        observed_states = tuple(
            sorted({item.value.get("state") for item in subject_evidence})
        )
        related_refs = tuple(sorted(item.reference for item in subject_evidence))

        if not output.satisfied:
            has_unsatisfied = True
            evidence_reasons.append(
                PacketIntegrationEligibilityReason(
                    code="required_subject_evidence_unsatisfied",
                    artifact_ref=output.artifact.reference,
                    required_state=output.required_state,
                    observed_states=observed_states,
                    related_refs=related_refs,
                )
            )
            continue

        conflicting = tuple(
            item
            for item in subject_evidence
            if item.value.get("state") != output.required_state
        )
        if conflicting:
            has_conflict = True
            evidence_reasons.append(
                PacketIntegrationEligibilityReason(
                    code="conflicting_subject_evidence_state",
                    artifact_ref=output.artifact.reference,
                    required_state=output.required_state,
                    observed_states=observed_states,
                    related_refs=tuple(sorted(item.reference for item in conflicting)),
                )
            )

    if has_conflict:
        return _result(
            mixed=mixed,
            packet=packet,
            outcome=NOT_ELIGIBLE_CONFLICTING_SUBJECT_EVIDENCE,
            reasons=tuple(evidence_reasons),
        )
    if has_unsatisfied:
        return _result(
            mixed=mixed,
            packet=packet,
            outcome=NOT_ELIGIBLE_UNSATISFIED_OUTPUT_EVIDENCE,
            reasons=tuple(evidence_reasons),
        )

    return _result(
        mixed=mixed,
        packet=packet,
        outcome=ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
        reasons=(
            PacketIntegrationEligibilityReason(
                code="first_slice_conditions_grounded",
                artifact_ref=None,
                required_state=None,
                observed_states=(),
                related_refs=tuple(
                    sorted(item.artifact.reference for item in mixed.created_outputs)
                ),
            ),
        ),
    )
