from __future__ import annotations

from typing import Any, Mapping, NamedTuple

from .packet_evidence_subject import (
    ResolvedReturnPacketEvidenceSubjects,
    resolve_return_packet_evidence_subjects,
)
from .packet_output_identity import ExactPacketRelation, ReturnPacketOutputIdentityError
from .resolution import resolve_exact_revision_member
from .store import FilesystemObjectStore


class CreatedOutputCompatibilityError(ReturnPacketOutputIdentityError):
    """Base error for the bounded created-output compatibility preflight."""


class PacketLaneContextError(CreatedOutputCompatibilityError):
    """The packet cannot reconstruct one grounded historical lane context."""


class OutputContractNotFoundError(CreatedOutputCompatibilityError):
    """A created artifact type has no declared output contract in its exact lane."""


class OutputContractAmbiguityError(CreatedOutputCompatibilityError):
    """A created artifact type matches more than one declared output contract."""


class EvidenceRequirementNotFoundError(CreatedOutputCompatibilityError):
    """A created output type has no evidence requirement in its exact lane."""


class EvidenceRequirementAmbiguityError(CreatedOutputCompatibilityError):
    """A created output type matches more than one lane evidence requirement."""


class RequiredStateSemanticsUnresolvedError(CreatedOutputCompatibilityError):
    """The current bounded preflight cannot interpret multiple required states."""


class CreatedArtifactCompatibility(NamedTuple):
    """Bounded compatibility result for one exact packet-created artifact.

    ``satisfied`` means only that the exact historical lane contract has one matching
    output declaration, exactly one evidence requirement with exactly one required
    state, and at least one exact subject-bound evidence record whose state equals that
    required state. It does not imply packet acceptance, claim closure, evidence
    quality/closure, state ranking, successor publication, integration, or replay.
    """

    artifact: ExactPacketRelation
    output_type: str
    required_state: str
    satisfying_evidence: tuple[ExactPacketRelation, ...]
    satisfied: bool


class ResolvedCreatedOutputCompatibility(NamedTuple):
    """Read-only created-output compatibility preflight for one exact packet."""

    packet_ref: str
    claim_ref: str
    occupancy_ref: str
    lane_ref: str
    subject_resolution: ResolvedReturnPacketEvidenceSubjects
    created_outputs: tuple[CreatedArtifactCompatibility, ...]


def _require_mapping(value: Any, *, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CreatedOutputCompatibilityError(f"{field} must expose a mapping")
    return value


def _ground_packet_lane_context(
    store: FilesystemObjectStore,
    subject_resolution: ResolvedReturnPacketEvidenceSubjects,
) -> tuple[str, str, str, Mapping[str, Any]]:
    """Reconstruct only the historical lifecycle relations needed for lane policy.

    Exact immutable object presence is not treated as proof that historical lifecycle
    relationships were grounded. The packet->claim->claim-base->lane relation and the
    claim->occupancy->occupancy-entry-base->lane relation are reconstructed from durable
    exact state before the lane contract is used operationally.

    No mutable HEAD/current pointer, storage recency, array order, actor identity,
    schedule position, founder status, or private chat state participates.
    """

    packet = subject_resolution.output_identity.packet
    packet_base_ref = packet.get("base_state_revision_ref")
    packet_lane_id = packet.get("lane_id")
    claim_ref = packet.get("claim_ref")
    if not all(isinstance(item, str) and item for item in (packet_base_ref, packet_lane_id, claim_ref)):
        raise PacketLaneContextError(
            "exact return packet exposes no usable base_state_revision_ref/lane_id/claim_ref"
        )

    store.load(packet_base_ref, "state-revision.schema.json")
    claim = store.load(claim_ref, "work-claim.schema.json")

    if packet_base_ref != claim.get("base_state_revision_ref"):
        raise PacketLaneContextError(
            "return-packet base_state_revision_ref does not match the exact claim_ref base"
        )
    if packet_lane_id != claim.get("lane_id"):
        raise PacketLaneContextError(
            "return-packet lane_id does not match the exact claim_ref lane_id"
        )

    claim_base_ref = claim["base_state_revision_ref"]
    store.load(claim_base_ref, "state-revision.schema.json")
    resolved_lane = resolve_exact_revision_member(
        store,
        claim_base_ref,
        "lane_refs",
        "lane",
        claim["lane_id"],
    )

    occupancy_ref = claim.get("occupancy_ref")
    if not isinstance(occupancy_ref, str) or not occupancy_ref:
        raise PacketLaneContextError("exact claim exposes no usable occupancy_ref")
    occupancy = store.load(occupancy_ref, "occupancy.schema.json")
    occupancy_entry_base_ref = occupancy["base_state_revision_ref"]
    store.load(occupancy_entry_base_ref, "state-revision.schema.json")
    resolve_exact_revision_member(
        store,
        occupancy_entry_base_ref,
        "lane_refs",
        "lane",
        occupancy["lane_id"],
    )

    if occupancy.get("lane_id") != claim.get("lane_id"):
        raise PacketLaneContextError(
            "return-packet claim_ref occupancy relation names a different logical lane"
        )
    if claim.get("status") != "open":
        raise PacketLaneContextError(
            "created-output preflight requires claim_ref to name an exact claim snapshot "
            "whose local status is 'open'; this does not establish global currentness"
        )
    if occupancy.get("status") != "active":
        raise PacketLaneContextError(
            "created-output preflight requires claim_ref occupancy_ref to name an exact "
            "occupancy snapshot whose local status is 'active'; this does not establish "
            "global currentness"
        )

    return claim_ref, occupancy_ref, resolved_lane.reference, resolved_lane.value


def preflight_created_output_compatibility(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedCreatedOutputCompatibility:
    """Evaluate only the first unambiguous created-output compatibility surface.

    The function consumes the canonical exact evidence-subject resolver, reconstructs
    the packet's historical lane context from durable exact lifecycle relationships,
    and evaluates each packet-created artifact independently.

    Supported semantics are deliberately narrow:

    * artifact ``type`` must match exactly one ``lane.outputs[]`` entry;
    * that output type must match exactly one ``lane.evidence_requirements[]`` entry;
    * the requirement must contain exactly one ``required_states`` value;
    * satisfaction requires at least one exact subject-bound evidence record whose
      ``state`` equals that one required state exactly.

    Missing/duplicate contract entries and multiple required states fail closed. No
    evidence-state hierarchy, implication, conjunction, alternative, ranking, recency,
    array order, mutable current state, or actor authority is invented. Unmatched
    packet evidence remains unmatched through the subject-resolution result and cannot
    satisfy a created artifact. ``artifacts_modified`` remains fail-closed because the
    consumed subject resolver inherits the exact output-identity boundary.

    This is a read-only preflight. It does not accept a packet, close a claim, mutate
    evidence, publish a successor revision, integrate outputs, open an epoch, or replay.
    """

    subject_resolution = resolve_return_packet_evidence_subjects(store, packet_ref)
    claim_ref, occupancy_ref, lane_ref, lane = _ground_packet_lane_context(
        store, subject_resolution
    )

    outputs = lane.get("outputs", ())
    evidence_requirements = lane.get("evidence_requirements", ())
    created_results: list[CreatedArtifactCompatibility] = []

    for binding in subject_resolution.created_artifact_bindings:
        artifact = binding.artifact
        artifact_type = artifact.value.get("type")
        if not isinstance(artifact_type, str) or not artifact_type:
            raise CreatedOutputCompatibilityError(
                f"exact artifact {artifact.reference!r} exposes no usable type"
            )

        output_matches = tuple(
            _require_mapping(item, field="lane.outputs[]")
            for item in outputs
            if _require_mapping(item, field="lane.outputs[]").get("type") == artifact_type
        )
        if not output_matches:
            raise OutputContractNotFoundError(
                f"created artifact type {artifact_type!r} has no declared output in exact lane {lane_ref}"
            )
        if len(output_matches) != 1:
            raise OutputContractAmbiguityError(
                f"created artifact type {artifact_type!r} matches {len(output_matches)} lane outputs; expected exactly one"
            )

        requirement_matches = tuple(
            _require_mapping(item, field="lane.evidence_requirements[]")
            for item in evidence_requirements
            if _require_mapping(item, field="lane.evidence_requirements[]").get("for_output")
            == artifact_type
        )
        if not requirement_matches:
            raise EvidenceRequirementNotFoundError(
                f"created artifact type {artifact_type!r} has no evidence requirement in exact lane {lane_ref}"
            )
        if len(requirement_matches) != 1:
            raise EvidenceRequirementAmbiguityError(
                f"created artifact type {artifact_type!r} matches {len(requirement_matches)} evidence requirements; expected exactly one"
            )

        required_states = requirement_matches[0].get("required_states")
        if not isinstance(required_states, (list, tuple)) or len(required_states) != 1:
            count = len(required_states) if isinstance(required_states, (list, tuple)) else 0
            raise RequiredStateSemanticsUnresolvedError(
                f"created artifact type {artifact_type!r} has {count} required states; "
                "the bounded preflight supports exactly one and does not invent AND/OR/rank semantics"
            )
        required_state = required_states[0]
        if not isinstance(required_state, str) or not required_state:
            raise RequiredStateSemanticsUnresolvedError(
                f"created artifact type {artifact_type!r} exposes no usable single required evidence state"
            )

        satisfying_evidence = tuple(
            evidence
            for evidence in binding.evidence_records
            if evidence.value.get("state") == required_state
        )
        created_results.append(
            CreatedArtifactCompatibility(
                artifact=artifact,
                output_type=artifact_type,
                required_state=required_state,
                satisfying_evidence=satisfying_evidence,
                satisfied=bool(satisfying_evidence),
            )
        )

    return ResolvedCreatedOutputCompatibility(
        packet_ref=packet_ref,
        claim_ref=claim_ref,
        occupancy_ref=occupancy_ref,
        lane_ref=lane_ref,
        subject_resolution=subject_resolution,
        created_outputs=tuple(created_results),
    )
