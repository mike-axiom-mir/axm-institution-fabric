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
    """Exact work-base provenance result for one artifact result.

    The name is retained for compatibility with Decision 010's created-output surface.
    Decision 011 reuses the same bounded work-base / producer-lane invariant for an
    explicitly named modified-artifact result without adding lineage or acceptance
    semantics.
    """

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


def preflight_exact_artifact_work_base_provenance(
    store: FilesystemObjectStore,
    artifact: ExactPacketRelation,
    *,
    claim_base_ref: str,
    lane_ref: str,
) -> CreatedArtifactProvenance:
    """Apply Decision 010's exact work-base / producer-lane invariant to one artifact.

    This helper is deliberately narrower than packet-created output compatibility. The
    caller must already have grounded the exact packet lifecycle context and exact-loaded
    the artifact relation. The helper then requires an artifact contract with the exact
    v0.2 work-base semantics (currently schema v0.2, v0.3, or v0.4), exact-loads the
    declared provenance state revision, requires exact equality to ``claim_base_ref``,
    and requires ``producer_lane_id`` to equal the exact ``lane_ref`` logical id.

    Artifact v0.3 extends dependency identity while preserving v0.2 provenance meaning.
    Artifact v0.4 replaces historical opaque source refs with typed source declarations
    while explicitly preserving v0.3 dependency/base semantics. Those source declarations
    are therefore not interpreted as provenance trust, closure, or acceptance here.
    Historical v0.1 remains unresolved for exact work-base provenance. Unknown future
    artifact versions are not silently assumed compatible.

    It does not evaluate output type, evidence state, evidence closure, source/dependency
    closure, logical lineage, ``supersedes_ref``, packet acceptance, claim closure,
    successor publication, integration, epochs, or replay.
    """

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

    try:
        parsed_lane = parse_immutable_ref(lane_ref)
    except IdentityError as exc:
        raise CreatedArtifactProvenanceError(
            f"exact claim-base lane reference is not canonical: {exc}"
        ) from exc
    if parsed_lane.kind != "lane":
        raise CreatedArtifactProvenanceError(
            "exact claim-base lane reference is not a lane reference"
        )
    lane = store.load(lane_ref, "lane.schema.json")
    lane_id = lane.get("id")
    if not isinstance(lane_id, str) or not lane_id:
        raise CreatedArtifactProvenanceError(
            "exact claim-base lane exposes no usable logical id"
        )
    if lane_id != parsed_lane.logical_id:
        raise CreatedArtifactProvenanceError(
            "exact claim-base lane logical id does not match its immutable reference"
        )

    artifact_value = artifact.value
    schema_version = artifact_value.get("schema_version")
    if schema_version not in ("0.2", "0.3", "0.4"):
        raise ArtifactProvenanceSchemaVersionError(
            f"exact artifact {artifact.reference!r} uses schema_version "
            f"{schema_version!r}; Decision 010 requires the exact work-base provenance "
            "contract carried by artifact schema v0.2/v0.3/v0.4 and does not reinterpret "
            "historical v0.1 base_state_revision strings or unknown future versions"
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

    return CreatedArtifactProvenance(
        artifact=artifact,
        provenance_base_ref=provenance_base_ref,
        producer_lane_id=producer_lane_id,
    )


def preflight_created_artifact_provenance(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedCreatedArtifactProvenance:
    """Ground Decision 010 for packet-created artifacts and stop before acceptance.

    The bounded chronology is:

    exact packet -> exact claim -> exact claim base -> exact claim-base lane
        then
    exact packet-created artifact -> artifact schema v0.2/v0.3/v0.4 exact provenance base
        -> exact-load that state revision -> require equality to the claim base
        -> require producer_lane_id equality to the claim-base lane logical id.

    Historical artifact schema v0.1 remains loadable as historical state, but its
    ``provenance.base_state_revision`` string is not silently reinterpreted as an exact
    immutable relation. Such an artifact therefore fails this preflight until an
    explicit migration produces an artifact instance carrying the v0.2 exact work-base
    provenance semantics. Artifact v0.3 preserves those provenance semantics while
    extending dependency identity; artifact v0.4 preserves both while changing source
    declaration representation only. No source trust/closure meaning is added here.

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

    resolved = tuple(
        preflight_exact_artifact_work_base_provenance(
            store,
            created.artifact,
            claim_base_ref=claim_base_ref,
            lane_ref=compatibility.lane_ref,
        )
        for created in compatibility.created_outputs
    )

    return ResolvedCreatedArtifactProvenance(
        packet_ref=packet_ref,
        claim_ref=compatibility.claim_ref,
        claim_base_ref=claim_base_ref,
        lane_ref=compatibility.lane_ref,
        compatibility=compatibility,
        created_artifacts=resolved,
    )
