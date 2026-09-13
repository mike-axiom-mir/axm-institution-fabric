from __future__ import annotations

from typing import Any, Mapping, NamedTuple

from .identity import IdentityError, parse_immutable_ref
from .packet_evidence_subject import EvidenceSubjectKindError
from .packet_modified_artifact_identity import (
    ResolvedModifiedArtifact,
    ResolvedReturnPacketModifiedArtifacts,
    preflight_modified_artifact_identity,
)
from .packet_output_compatibility import (
    CreatedOutputCompatibilityError,
    EvidenceRequirementAmbiguityError,
    EvidenceRequirementNotFoundError,
    OutputContractAmbiguityError,
    OutputContractNotFoundError,
    RequiredStateSemanticsUnresolvedError,
    _require_mapping,
)
from .packet_output_identity import ExactPacketRelation, _load_exact_relation
from .store import FilesystemObjectStore, ObjectStoreError


class ModifiedResultCompatibilityError(CreatedOutputCompatibilityError):
    """Base error for Decision 012 modified-result compatibility preflight."""


class ModifiedResultEvidenceReferenceError(ModifiedResultCompatibilityError):
    """A packet evidence relationship cannot be used as an exact evidence record."""


class UnmatchedModifiedResultEvidence(NamedTuple):
    """Packet evidence that does not support an exact modification result in this slice."""

    evidence: ExactPacketRelation
    subject_ref: str
    reason: str


class ModifiedArtifactResultCompatibility(NamedTuple):
    """Bounded compatibility result for one exact Decision 011 result endpoint.

    ``satisfied`` has the same deliberately narrow meaning as the created-output
    preflight: one exact historical lane output declaration, one evidence requirement,
    exactly one currently-supported required state, and at least one exact packet
    evidence record whose subject is this exact result and whose state equals that
    required state. ``subject_evidence`` preserves every exact packet evidence record
    bound to the result so additional/conflicting states are not silently collapsed.
    """

    modification: ResolvedModifiedArtifact
    output_type: str
    required_state: str
    subject_evidence: tuple[ExactPacketRelation, ...]
    satisfying_evidence: tuple[ExactPacketRelation, ...]
    satisfied: bool


class ResolvedModifiedResultCompatibility(NamedTuple):
    """Read-only Decision 012 compatibility projection for one exact return packet."""

    packet_ref: str
    claim_ref: str
    claim_base_ref: str
    occupancy_ref: str
    lane_ref: str
    identity_resolution: ResolvedReturnPacketModifiedArtifacts
    modified_results: tuple[ModifiedArtifactResultCompatibility, ...]
    unmatched_evidence: tuple[UnmatchedModifiedResultEvidence, ...]


def _packet_evidence_records(
    store: FilesystemObjectStore,
    resolution: ResolvedReturnPacketModifiedArtifacts,
) -> tuple[ExactPacketRelation, ...]:
    evidence_refs = resolution.packet.get("evidence_refs", ())
    records: list[ExactPacketRelation] = []
    for index, reference in enumerate(evidence_refs):
        if not isinstance(reference, str) or not reference:
            raise ModifiedResultEvidenceReferenceError(
                f"$.evidence_refs[{index}] exposes no usable exact evidence reference"
            )
        try:
            records.append(
                _load_exact_relation(
                    store,
                    reference,
                    expected_kind="evidence-record",
                    field=f"$.evidence_refs[{index}]",
                )
            )
        except ObjectStoreError as exc:
            raise ModifiedResultEvidenceReferenceError(
                f"modified-result compatibility could not exact-load $.evidence_refs[{index}]: {exc}"
            ) from exc
    return tuple(records)


def _subject_ref(evidence: Mapping[str, Any]) -> str:
    subject_ref = evidence.get("subject_ref")
    if not isinstance(subject_ref, str) or not subject_ref:
        raise ModifiedResultCompatibilityError(
            "exact evidence relation exposes no usable subject_ref"
        )
    return subject_ref


def _bind_result_evidence(
    evidence_records: tuple[ExactPacketRelation, ...],
    result_refs: tuple[str, ...],
) -> tuple[
    dict[str, tuple[ExactPacketRelation, ...]],
    tuple[UnmatchedModifiedResultEvidence, ...],
]:
    """Bind packet evidence only by full exact immutable modification-result identity."""

    bound: dict[str, list[ExactPacketRelation]] = {reference: [] for reference in result_refs}
    unmatched: list[UnmatchedModifiedResultEvidence] = []

    for evidence in evidence_records:
        subject_ref = _subject_ref(evidence.value)
        try:
            parsed_subject = parse_immutable_ref(subject_ref)
        except IdentityError:
            unmatched.append(
                UnmatchedModifiedResultEvidence(
                    evidence=evidence,
                    subject_ref=subject_ref,
                    reason="non_exact_subject",
                )
            )
            continue

        if parsed_subject.kind != "artifact":
            raise EvidenceSubjectKindError(
                "evidence subject considered against packet modification results must use "
                f"kind 'artifact', got {parsed_subject.kind!r} in {subject_ref!r}"
            )

        if subject_ref not in bound:
            unmatched.append(
                UnmatchedModifiedResultEvidence(
                    evidence=evidence,
                    subject_ref=subject_ref,
                    reason="exact_artifact_not_modified_result",
                )
            )
            continue

        bound[subject_ref].append(evidence)

    return (
        {reference: tuple(records) for reference, records in bound.items()},
        tuple(unmatched),
    )


def preflight_modified_result_compatibility(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedModifiedResultCompatibility:
    """Evaluate only Decision 012's exact modification-result compatibility surface.

    Decision 011 is consumed as the sole prior/result/context authority. Packet evidence
    is exact-loaded independently, then may support a modification result only when the
    evidence ``subject_ref`` is the full exact immutable ref of that exact result.
    Evidence about the exact prior endpoint, another same-logical artifact, another
    modification result, or a non-exact subject remains explicitly unmatched. An exact
    non-artifact subject fails closed. ``artifact.evidence_refs`` is not consulted.

    The lane contract uses exactly the already-demonstrated created-output semantics:
    one matching ``lane.outputs[]`` entry, one matching ``lane.evidence_requirements[]``
    entry, and exactly one required state. No AND/OR/rank implication, logical-id
    fallback, version ordering, ``supersedes_ref`` authority, recency/currentness,
    storage/array order, actor identity, scheduler position, founder status, or Git
    permission is invented.

    ``satisfied=True`` is not evidence closure, packet acceptance, valid lineage or
    supersession, claim closure, successor publication, integration, epochs, or replay.
    The function is read-only and deliberately stops before those stages.
    """

    identity_resolution = preflight_modified_artifact_identity(store, packet_ref)

    # Decision 011 already grounds this exact immutable lane ref through the packet's
    # exact claim base. Loading that exact ref from the object store preserves the same
    # identity authority while returning the ordinary mapping/list representation that
    # the existing compatibility evaluator expects. Do not weaken that evaluator merely
    # to accommodate the canonical-byte operational view used for exposed output data.
    lane = store.load(identity_resolution.lane_ref, "lane.schema.json")

    evidence_records = _packet_evidence_records(store, identity_resolution)
    result_refs = tuple(
        modification.result_artifact.reference
        for modification in identity_resolution.modifications
    )
    evidence_by_result, unmatched_evidence = _bind_result_evidence(
        evidence_records,
        result_refs,
    )

    outputs = lane.get("outputs", ())
    evidence_requirements = lane.get("evidence_requirements", ())
    compatibility_results: list[ModifiedArtifactResultCompatibility] = []

    for modification in identity_resolution.modifications:
        artifact = modification.result_artifact
        artifact_type = artifact.value.get("type")
        if not isinstance(artifact_type, str) or not artifact_type:
            raise ModifiedResultCompatibilityError(
                f"exact modification result {artifact.reference!r} exposes no usable type"
            )

        output_matches = tuple(
            _require_mapping(item, field="lane.outputs[]")
            for item in outputs
            if _require_mapping(item, field="lane.outputs[]").get("type") == artifact_type
        )
        if not output_matches:
            raise OutputContractNotFoundError(
                f"modified result artifact type {artifact_type!r} has no declared output "
                f"in exact lane {identity_resolution.lane_ref}"
            )
        if len(output_matches) != 1:
            raise OutputContractAmbiguityError(
                f"modified result artifact type {artifact_type!r} matches "
                f"{len(output_matches)} lane outputs; expected exactly one"
            )

        requirement_matches = tuple(
            _require_mapping(item, field="lane.evidence_requirements[]")
            for item in evidence_requirements
            if _require_mapping(item, field="lane.evidence_requirements[]").get("for_output")
            == artifact_type
        )
        if not requirement_matches:
            raise EvidenceRequirementNotFoundError(
                f"modified result artifact type {artifact_type!r} has no evidence "
                f"requirement in exact lane {identity_resolution.lane_ref}"
            )
        if len(requirement_matches) != 1:
            raise EvidenceRequirementAmbiguityError(
                f"modified result artifact type {artifact_type!r} matches "
                f"{len(requirement_matches)} evidence requirements; expected exactly one"
            )

        required_states = requirement_matches[0].get("required_states")
        if not isinstance(required_states, (list, tuple)) or len(required_states) != 1:
            count = len(required_states) if isinstance(required_states, (list, tuple)) else 0
            raise RequiredStateSemanticsUnresolvedError(
                f"modified result artifact type {artifact_type!r} has {count} required "
                "states; the bounded preflight supports exactly one and does not invent "
                "AND/OR/rank semantics"
            )
        required_state = required_states[0]
        if not isinstance(required_state, str) or not required_state:
            raise RequiredStateSemanticsUnresolvedError(
                f"modified result artifact type {artifact_type!r} exposes no usable "
                "single required evidence state"
            )

        subject_evidence = evidence_by_result.get(artifact.reference, ())
        satisfying_evidence = tuple(
            evidence
            for evidence in subject_evidence
            if evidence.value.get("state") == required_state
        )
        compatibility_results.append(
            ModifiedArtifactResultCompatibility(
                modification=modification,
                output_type=artifact_type,
                required_state=required_state,
                subject_evidence=subject_evidence,
                satisfying_evidence=satisfying_evidence,
                satisfied=bool(satisfying_evidence),
            )
        )

    return ResolvedModifiedResultCompatibility(
        packet_ref=packet_ref,
        claim_ref=identity_resolution.claim_ref,
        claim_base_ref=identity_resolution.claim_base_ref,
        occupancy_ref=identity_resolution.occupancy_ref,
        lane_ref=identity_resolution.lane_ref,
        identity_resolution=identity_resolution,
        modified_results=tuple(compatibility_results),
        unmatched_evidence=unmatched_evidence,
    )
