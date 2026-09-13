from __future__ import annotations

from typing import NamedTuple

from .identity import IdentityError, parse_immutable_ref
from .packet_output_compatibility import (
    CreatedOutputCompatibilityError,
    ResolvedCreatedOutputCompatibility,
    preflight_created_output_compatibility,
)
from .packet_output_identity import ExactPacketRelation
from .store import FilesystemObjectStore, ObjectStoreError


class CreatedArtifactProvenanceError(CreatedOutputCompatibilityError):
    """Base error for the bounded packet-created artifact provenance preflight."""


class ArtifactProvenanceSchemaVersionError(CreatedArtifactProvenanceError):
    """The artifact contract version does not assert an exact provenance work base."""


class ArtifactProvenanceReferenceError(CreatedArtifactProvenanceError):
    """The artifact provenance work-base ref is malformed, wrong-kind, or unresolved."""


class ArtifactProvenanceBaseMismatchError(CreatedArtifactProvenanceError):
    """The exact artifact work base differs from the exact packet claim base."""


class ArtifactProducerLaneMismatchError(CreatedArtifactProvenanceError):
    """The artifact producer lane differs from the exact packet claim-base lane."""


class CreatedArtifactProvenance(NamedTuple):
    """Exact work-base provenance result for one packet-created artifact."""

    artifact: ExactPacketRelation
    provenance_base_ref: str
    producer_lane_id: str


class ResolvedCreatedArtifactProvenance(NamedTuple):
    """Read-only Decision 010 preflight for one exact return packet."""

    packet_ref: str
    claim_ref: str
    claim_base_ref: str
    lane_ref: str
    compatibility: ResolvedCreatedOutputCompatibility
    created_artifacts: tuple[CreatedArtifactProvenance, ...]


def preflight_created_artifact_provenance(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedCreatedArtifactProvenance:
    """Ground Decision 010 for packet-created artifacts and stop before acceptance.

    The bounded chronology is:

    exact packet -> exact claim -> exact claim base -> exact claim-base lane
        then
    exact packet-created artifact -> artifact schema v0.2 exact provenance base
        -> exact-load that state revision -> require equality to the claim base
        -> require producer_lane_id equality to the claim-base lane logical id.

    Historical artifact schema v0.1 remains loadable as historical state, but its
    ``provenance.base_state_revision`` string is not silently reinterpreted as an exact
    immutable relation. Such an artifact therefore fails this preflight until an
    explicit migration produces a v0.2 artifact instance.

    The function first runs the canonical read-only created-output compatibility
    preflight, so exact packet/claim/lane/artifact/evidence selection, subject binding,
    bounded output compatibility, explicit conflicting evidence, and the
    ``artifacts_modified`` fail-closed boundary remain in force. This function adds no
    source/dependency closure, evidence-conflict policy, packet acceptance, claim
    closure, successor publication, integration, epochs, or replay semantics.
    """

    compatibility = preflight_created_output_compatibility(store, packet_ref)

    claim = store.load(compatibility.claim_ref, "work-claim.schema.json")
    claim_base_ref = claim.get("base_state_revision_ref")
    if not isinstance(claim_base_ref, str) or not claim_base_ref:
        raise CreatedArtifactProvenanceError(
            "exact claim exposes no usable base_state_revision_ref"
        )
    try:
        parsed_claim_base = parse_immutable_ref(claim_base_ref)
    except IdentityError as exc:
        raise CreatedArtifactProvenanceError(
            f"exact claim base_state_revision_ref is not canonical: {exc}"
        ) from exc
    if parsed_claim_base.kind != "state-revision":
        raise CreatedArtifactProvenanceError(
            "exact claim base_state_revision_ref is not a state-revision reference"
        )
    store.load(claim_base_ref, "state-revision.schema.json")

    lane = store.load(compatibility.lane_ref, "lane.schema.json")
    lane_id = lane.get("id")
    if not isinstance(lane_id, str) or not lane_id:
        raise CreatedArtifactProvenanceError(
            "exact claim-base lane exposes no usable logical id"
        )
    if claim.get("lane_id") != lane_id:
        raise CreatedArtifactProvenanceError(
            "exact claim lane_id does not match the exact claim-base lane logical id"
        )

    resolved: list[CreatedArtifactProvenance] = []
    for created in compatibility.created_outputs:
        artifact = created.artifact
        artifact_value = artifact.value
        schema_version = artifact_value.get("schema_version")
        if schema_version != "0.2":
            raise ArtifactProvenanceSchemaVersionError(
                f"exact artifact {artifact.reference!r} uses schema_version "
                f"{schema_version!r}; Decision 010 requires artifact schema v0.2 "
                "with explicit base_state_revision_ref and does not reinterpret "
                "historical v0.1 base_state_revision strings"
            )

        provenance = artifact_value.get("provenance")
        if provenance is None or not hasattr(provenance, "get"):
            raise CreatedArtifactProvenanceError(
                f"exact artifact {artifact.reference!r} exposes no usable provenance mapping"
            )

        producer_lane_id = provenance.get("producer_lane_id")
        if producer_lane_id != lane_id:
            raise ArtifactProducerLaneMismatchError(
                f"exact artifact {artifact.reference!r} producer_lane_id "
                f"{producer_lane_id!r} does not match exact claim-base lane {lane_id!r}"
            )

        provenance_base_ref = provenance.get("base_state_revision_ref")
        if not isinstance(provenance_base_ref, str) or not provenance_base_ref:
            raise ArtifactProvenanceReferenceError(
                f"exact artifact {artifact.reference!r} exposes no usable "
                "provenance.base_state_revision_ref"
            )
        try:
            parsed = parse_immutable_ref(provenance_base_ref)
        except IdentityError as exc:
            raise ArtifactProvenanceReferenceError(
                f"exact artifact {artifact.reference!r} provenance base is not a "
                f"canonical immutable reference: {exc}"
            ) from exc
        if parsed.kind != "state-revision":
            raise ArtifactProvenanceReferenceError(
                f"exact artifact {artifact.reference!r} provenance base kind "
                f"{parsed.kind!r} is not 'state-revision'"
            )

        try:
            store.load(provenance_base_ref, "state-revision.schema.json")
        except ObjectStoreError as exc:
            raise ArtifactProvenanceReferenceError(
                f"exact artifact {artifact.reference!r} provenance base could not be "
                f"exact-loaded and identity-verified: {exc}"
            ) from exc

        if provenance_base_ref != claim_base_ref:
            raise ArtifactProvenanceBaseMismatchError(
                f"exact artifact {artifact.reference!r} provenance base "
                f"{provenance_base_ref!r} differs from exact claim base {claim_base_ref!r}"
            )

        resolved.append(
            CreatedArtifactProvenance(
                artifact=artifact,
                provenance_base_ref=provenance_base_ref,
                producer_lane_id=producer_lane_id,
            )
        )

    return ResolvedCreatedArtifactProvenance(
        packet_ref=packet_ref,
        claim_ref=compatibility.claim_ref,
        claim_base_ref=claim_base_ref,
        lane_ref=compatibility.lane_ref,
        compatibility=compatibility,
        created_artifacts=tuple(resolved),
    )
