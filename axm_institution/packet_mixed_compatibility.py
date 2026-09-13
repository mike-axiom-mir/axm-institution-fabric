from __future__ import annotations

from collections import Counter
from typing import Any, Mapping, NamedTuple

from .identity import IdentityError, parse_immutable_ref
from .packet_evidence_subject import (
    EvidenceSubjectKindError,
    ExactCreatedArtifactEvidenceBinding,
)
from .packet_modified_artifact_identity import (
    ResolvedReturnPacketModifiedArtifacts,
    preflight_modified_artifact_identity,
)
from .packet_modified_result_compatibility import (
    ModifiedArtifactResultCompatibility,
    ResolvedModifiedResultCompatibility,
    preflight_modified_result_compatibility,
)
from .packet_output_compatibility import (
    CreatedArtifactCompatibility,
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


class MixedPacketCompatibilityError(CreatedOutputCompatibilityError):
    """Base error for Decision 013 mixed created+modified compatibility projection."""


class MixedPacketContextMismatchError(MixedPacketCompatibilityError):
    """Created/modified component facts do not share one exact historical context."""


class MixedOutputCategoryCollisionError(MixedPacketCompatibilityError):
    """One exact artifact is classified as both created and modification result."""


class MixedComponentEvidenceMismatchError(MixedPacketCompatibilityError):
    """Decision 012 evidence facts disagree with the mixed exact-subject classification."""


class MixedPacketEvidenceReferenceError(MixedPacketCompatibilityError):
    """A packet evidence relationship cannot be exact-loaded for the mixed projection."""


class UnmatchedMixedPacketEvidence(NamedTuple):
    """Packet evidence that does not name any exact created or modified-result output."""

    evidence: ExactPacketRelation
    subject_ref: str
    reason: str


class ResolvedMixedPacketCompatibility(NamedTuple):
    """Read-only Decision 013 projection for created and modified-result outputs.

    The result exposes component compatibility facts only. It deliberately contains no
    packet-level ``accepted``, ``complete``, ``closed``, or aggregate ``satisfied`` field.
    """

    packet_ref: str
    claim_ref: str
    claim_base_ref: str
    occupancy_ref: str
    lane_ref: str
    created_bindings: tuple[ExactCreatedArtifactEvidenceBinding, ...]
    created_outputs: tuple[CreatedArtifactCompatibility, ...]
    modified_results: tuple[ModifiedArtifactResultCompatibility, ...]
    unmatched_evidence: tuple[UnmatchedMixedPacketEvidence, ...]


def _packet_evidence_records(
    store: FilesystemObjectStore,
    resolution: ResolvedReturnPacketModifiedArtifacts,
) -> tuple[ExactPacketRelation, ...]:
    records: list[ExactPacketRelation] = []
    for index, reference in enumerate(resolution.packet.get("evidence_refs", ())):
        if not isinstance(reference, str) or not reference:
            raise MixedPacketEvidenceReferenceError(
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
            raise MixedPacketEvidenceReferenceError(
                f"mixed compatibility could not exact-load $.evidence_refs[{index}]: {exc}"
            ) from exc
    return tuple(records)


def _created_artifact_relations(
    store: FilesystemObjectStore,
    resolution: ResolvedReturnPacketModifiedArtifacts,
) -> tuple[ExactPacketRelation, ...]:
    relations: list[ExactPacketRelation] = []
    for index, reference in enumerate(resolution.packet.get("artifacts_created", ())):
        if not isinstance(reference, str) or not reference:
            raise MixedPacketCompatibilityError(
                f"$.artifacts_created[{index}] exposes no usable exact artifact reference"
            )
        relations.append(
            _load_exact_relation(
                store,
                reference,
                expected_kind="artifact",
                field=f"$.artifacts_created[{index}]",
            )
        )
    return tuple(relations)


def _exact_modification_pairs(
    resolution: ResolvedReturnPacketModifiedArtifacts,
) -> Counter[tuple[str, str]]:
    return Counter(
        (
            item.prior_artifact.reference,
            item.result_artifact.reference,
        )
        for item in resolution.modifications
    )


def _require_same_modified_context(
    identity_resolution: ResolvedReturnPacketModifiedArtifacts,
    modified_compatibility: ResolvedModifiedResultCompatibility,
) -> None:
    expected_context = (
        identity_resolution.packet_ref,
        identity_resolution.claim_ref,
        identity_resolution.claim_base_ref,
        identity_resolution.occupancy_ref,
        identity_resolution.lane_ref,
    )
    observed_context = (
        modified_compatibility.packet_ref,
        modified_compatibility.claim_ref,
        modified_compatibility.claim_base_ref,
        modified_compatibility.occupancy_ref,
        modified_compatibility.lane_ref,
    )
    if observed_context != expected_context:
        raise MixedPacketContextMismatchError(
            "Decision 012 component does not expose the same exact "
            "packet/claim/base/occupancy/lane context as Decision 011"
        )
    if _exact_modification_pairs(
        modified_compatibility.identity_resolution
    ) != _exact_modification_pairs(identity_resolution):
        raise MixedPacketContextMismatchError(
            "Decision 012 component does not expose the same exact prior/result relations "
            "as the Decision 011 identity context"
        )


def _bind_mixed_evidence(
    evidence_records: tuple[ExactPacketRelation, ...],
    created_artifacts: tuple[ExactPacketRelation, ...],
    modified_result_refs: tuple[str, ...],
) -> tuple[
    tuple[ExactCreatedArtifactEvidenceBinding, ...],
    dict[str, tuple[ExactPacketRelation, ...]],
    tuple[UnmatchedMixedPacketEvidence, ...],
]:
    created_bound: dict[str, list[ExactPacketRelation]] = {
        item.reference: [] for item in created_artifacts
    }
    modified_bound: dict[str, list[ExactPacketRelation]] = {
        reference: [] for reference in modified_result_refs
    }
    unmatched: list[UnmatchedMixedPacketEvidence] = []

    for evidence in evidence_records:
        subject_ref = evidence.value.get("subject_ref")
        if not isinstance(subject_ref, str) or not subject_ref:
            raise MixedPacketCompatibilityError(
                "exact evidence relation exposes no usable subject_ref"
            )
        try:
            parsed_subject = parse_immutable_ref(subject_ref)
        except IdentityError:
            unmatched.append(
                UnmatchedMixedPacketEvidence(
                    evidence=evidence,
                    subject_ref=subject_ref,
                    reason="non_exact_subject",
                )
            )
            continue

        if parsed_subject.kind != "artifact":
            raise EvidenceSubjectKindError(
                "evidence subject considered against mixed packet outputs must use "
                f"kind 'artifact', got {parsed_subject.kind!r} in {subject_ref!r}"
            )

        if subject_ref in created_bound:
            created_bound[subject_ref].append(evidence)
            continue
        if subject_ref in modified_bound:
            modified_bound[subject_ref].append(evidence)
            continue

        unmatched.append(
            UnmatchedMixedPacketEvidence(
                evidence=evidence,
                subject_ref=subject_ref,
                reason="exact_artifact_not_packet_output",
            )
        )

    created_bindings = tuple(
        ExactCreatedArtifactEvidenceBinding(
            artifact=artifact,
            evidence_records=tuple(created_bound[artifact.reference]),
        )
        for artifact in created_artifacts
    )
    return (
        created_bindings,
        {reference: tuple(items) for reference, items in modified_bound.items()},
        tuple(unmatched),
    )


def _evaluate_created_outputs(
    lane: Mapping[str, Any],
    lane_ref: str,
    bindings: tuple[ExactCreatedArtifactEvidenceBinding, ...],
) -> tuple[CreatedArtifactCompatibility, ...]:
    outputs = lane.get("outputs", ())
    evidence_requirements = lane.get("evidence_requirements", ())
    results: list[CreatedArtifactCompatibility] = []

    for binding in bindings:
        artifact = binding.artifact
        artifact_type = artifact.value.get("type")
        if not isinstance(artifact_type, str) or not artifact_type:
            raise MixedPacketCompatibilityError(
                f"exact created artifact {artifact.reference!r} exposes no usable type"
            )

        output_matches = tuple(
            _require_mapping(item, field="lane.outputs[]")
            for item in outputs
            if _require_mapping(item, field="lane.outputs[]").get("type") == artifact_type
        )
        if not output_matches:
            raise OutputContractNotFoundError(
                f"created artifact type {artifact_type!r} has no declared output "
                f"in exact lane {lane_ref}"
            )
        if len(output_matches) != 1:
            raise OutputContractAmbiguityError(
                f"created artifact type {artifact_type!r} matches "
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
                f"created artifact type {artifact_type!r} has no evidence requirement "
                f"in exact lane {lane_ref}"
            )
        if len(requirement_matches) != 1:
            raise EvidenceRequirementAmbiguityError(
                f"created artifact type {artifact_type!r} matches "
                f"{len(requirement_matches)} evidence requirements; expected exactly one"
            )

        required_states = requirement_matches[0].get("required_states")
        if not isinstance(required_states, (list, tuple)) or len(required_states) != 1:
            count = len(required_states) if isinstance(required_states, (list, tuple)) else 0
            raise RequiredStateSemanticsUnresolvedError(
                f"created artifact type {artifact_type!r} has {count} required states; "
                "the bounded preflight supports exactly one and does not invent "
                "AND/OR/rank semantics"
            )
        required_state = required_states[0]
        if not isinstance(required_state, str) or not required_state:
            raise RequiredStateSemanticsUnresolvedError(
                f"created artifact type {artifact_type!r} exposes no usable single "
                "required evidence state"
            )

        satisfying_evidence = tuple(
            evidence
            for evidence in binding.evidence_records
            if evidence.value.get("state") == required_state
        )
        results.append(
            CreatedArtifactCompatibility(
                artifact=artifact,
                output_type=artifact_type,
                required_state=required_state,
                satisfying_evidence=satisfying_evidence,
                satisfied=bool(satisfying_evidence),
            )
        )

    return tuple(results)


def _require_modified_evidence_agreement(
    modified_compatibility: ResolvedModifiedResultCompatibility,
    mixed_modified_evidence: dict[str, tuple[ExactPacketRelation, ...]],
) -> None:
    component_results = {
        result.modification.result_artifact.reference: result
        for result in modified_compatibility.modified_results
    }
    if set(component_results) != set(mixed_modified_evidence):
        raise MixedComponentEvidenceMismatchError(
            "Decision 012 result identities disagree with the mixed output categories"
        )

    for result_ref, mixed_evidence in mixed_modified_evidence.items():
        component = component_results[result_ref]
        component_refs = Counter(item.reference for item in component.subject_evidence)
        mixed_refs = Counter(item.reference for item in mixed_evidence)
        if component_refs != mixed_refs:
            raise MixedComponentEvidenceMismatchError(
                f"Decision 012 evidence subjects disagree for exact result {result_ref!r}"
            )


def preflight_mixed_packet_compatibility(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedMixedPacketCompatibility:
    """Compose Decision 013's created+modified compatibility facts read-only.

    Decision 011 is used as the exact packet/claim/base/occupancy/lane context authority.
    Decision 012 is consumed unchanged for modification results. Created artifact and
    packet evidence refs are exact-loaded directly from that same already-grounded
    packet so the historical created-only resolver keeps its deliberate fail-closed
    behavior for non-empty ``artifacts_modified`` lists.

    Evidence is then classified once by full exact artifact subject identity across the
    two output families. Exact category collisions fail closed. Non-exact and unrelated
    evidence remains explicit, while exact wrong-kind subjects fail closed. No logical-id
    fallback, type pooling, recency/currentness, array/storage order, version,
    ``supersedes_ref``, actor identity, scheduler position, founder status, or Git
    permission participates.

    The function exposes only per-output component facts. It does not establish evidence
    conflict precedence, source/dependency closure, lineage/supersession validity, packet
    acceptance, claim closure, successor publication, integration, epochs, or replay.
    """

    identity_resolution = preflight_modified_artifact_identity(store, packet_ref)
    modified_compatibility = preflight_modified_result_compatibility(store, packet_ref)
    _require_same_modified_context(identity_resolution, modified_compatibility)

    created_artifacts = _created_artifact_relations(store, identity_resolution)
    modified_result_refs = tuple(
        item.result_artifact.reference for item in identity_resolution.modifications
    )
    collisions = set(item.reference for item in created_artifacts).intersection(
        modified_result_refs
    )
    if collisions:
        collision_list = ", ".join(sorted(collisions))
        raise MixedOutputCategoryCollisionError(
            "the same exact artifact ref is classified as both created and modified "
            f"result: {collision_list}"
        )

    evidence_records = _packet_evidence_records(store, identity_resolution)
    created_bindings, mixed_modified_evidence, unmatched_evidence = _bind_mixed_evidence(
        evidence_records,
        created_artifacts,
        modified_result_refs,
    )
    _require_modified_evidence_agreement(
        modified_compatibility,
        mixed_modified_evidence,
    )

    lane = store.load(identity_resolution.lane_ref, "lane.schema.json")
    created_outputs = _evaluate_created_outputs(
        lane,
        identity_resolution.lane_ref,
        created_bindings,
    )

    return ResolvedMixedPacketCompatibility(
        packet_ref=packet_ref,
        claim_ref=identity_resolution.claim_ref,
        claim_base_ref=identity_resolution.claim_base_ref,
        occupancy_ref=identity_resolution.occupancy_ref,
        lane_ref=identity_resolution.lane_ref,
        created_bindings=created_bindings,
        created_outputs=created_outputs,
        modified_results=modified_compatibility.modified_results,
        unmatched_evidence=unmatched_evidence,
    )
