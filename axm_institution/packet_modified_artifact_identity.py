from __future__ import annotations

from typing import Any, Mapping, NamedTuple

from .identity import IdentityError, parse_immutable_ref
from .packet_artifact_provenance import (
    CreatedArtifactProvenance,
    preflight_exact_artifact_work_base_provenance,
)
from .packet_output_identity import (
    ExactPacketRelation,
    ReturnPacketOutputIdentityError,
    _freeze_json,
    _load_exact_relation,
)
from .resolution import resolve_exact_revision_member
from .store import FilesystemObjectStore, ObjectStoreError


class ModifiedArtifactIdentityError(ReturnPacketOutputIdentityError):
    """Base error for Decision 011 modified-artifact two-sided identity preflight."""


class ModifiedArtifactContractVersionError(ModifiedArtifactIdentityError):
    """The packet contract cannot express an operational two-sided modification."""


class ModifiedArtifactRelationShapeError(ModifiedArtifactIdentityError):
    """A v0.4 modified-artifact relation is not the explicit prior/result pair."""


class ModifiedArtifactReferenceError(ModifiedArtifactIdentityError):
    """A prior/result endpoint is malformed, wrong-kind, missing, corrupt, or mismatched."""


class ModifiedArtifactPriorMembershipError(ModifiedArtifactIdentityError):
    """The exact prior artifact is not an exact member of the exact claim base."""


class PacketModificationContextError(ModifiedArtifactIdentityError):
    """The packet cannot reconstruct the exact lifecycle context required by Decision 011."""


class ResolvedModifiedArtifact(NamedTuple):
    """One exact Decision 011 prior/result pair with grounded result work-base provenance."""

    prior_artifact: ExactPacketRelation
    result_artifact: ExactPacketRelation
    result_provenance: CreatedArtifactProvenance


class ResolvedReturnPacketModifiedArtifacts(NamedTuple):
    """Read-only Decision 011 result for one exact return packet.

    The result proves only explicit exact prior/result identity, exact prior membership in
    the exact claim base, and Decision 010 work-base / producer-lane provenance on each
    exact result. It does not prove logical lineage, valid supersession, evidence/source/
    dependency closure, packet acceptance, claim closure, successor publication,
    integration, epochs, or replay.
    """

    packet_ref: str
    packet: Mapping[str, Any]
    claim_ref: str
    claim_base_ref: str
    occupancy_ref: str
    lane_ref: str
    modifications: tuple[ResolvedModifiedArtifact, ...]


def _parse_artifact_ref(reference: str, *, field: str):
    try:
        parsed = parse_immutable_ref(reference)
    except IdentityError as exc:
        raise ModifiedArtifactReferenceError(
            f"modified-artifact identity failed at {field}: {exc}"
        ) from exc
    if parsed.kind != "artifact":
        raise ModifiedArtifactReferenceError(
            f"modified-artifact identity failed at {field}: expected kind 'artifact', "
            f"got {parsed.kind!r}"
        )
    return parsed


def _load_artifact_relation(
    store: FilesystemObjectStore,
    reference: str,
    *,
    field: str,
) -> ExactPacketRelation:
    _parse_artifact_ref(reference, field=field)
    try:
        return _load_exact_relation(
            store,
            reference,
            expected_kind="artifact",
            field=field,
        )
    except ObjectStoreError as exc:
        raise ModifiedArtifactReferenceError(
            f"modified-artifact identity failed at {field}: {exc}"
        ) from exc


def _ground_packet_context(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> tuple[
    Mapping[str, Any],
    str,
    str,
    str,
    str,
    Mapping[str, Any],
]:
    """Reconstruct the exact historical packet lifecycle context used by Decision 011.

    The checks intentionally mirror the already-canonical Stage 4 packet/lane context:
    exact packet -> exact claim -> exact claim base -> exact claim-base lane, plus the
    exact claim occupancy and the occupancy's own historical entry-base/lane relation.
    Exact object presence alone is not treated as proof of those relationships.
    """

    try:
        parsed_packet = parse_immutable_ref(packet_ref)
    except IdentityError as exc:
        raise PacketModificationContextError(
            f"invalid exact return-packet reference: {exc}"
        ) from exc
    if parsed_packet.kind != "return-packet":
        raise PacketModificationContextError(
            f"packet_ref must have kind 'return-packet', got {parsed_packet.kind!r}"
        )

    packet = store.load(packet_ref, "return-packet.schema.json")
    packet_base_ref = packet.get("base_state_revision_ref")
    packet_lane_id = packet.get("lane_id")
    claim_ref = packet.get("claim_ref")
    if not all(
        isinstance(item, str) and item
        for item in (packet_base_ref, packet_lane_id, claim_ref)
    ):
        raise PacketModificationContextError(
            "exact return packet exposes no usable base_state_revision_ref/lane_id/claim_ref"
        )

    claim_base = store.load(packet_base_ref, "state-revision.schema.json")
    claim = store.load(claim_ref, "work-claim.schema.json")
    if packet_base_ref != claim.get("base_state_revision_ref"):
        raise PacketModificationContextError(
            "return-packet base_state_revision_ref does not match the exact claim_ref base"
        )
    if packet_lane_id != claim.get("lane_id"):
        raise PacketModificationContextError(
            "return-packet lane_id does not match the exact claim_ref lane_id"
        )

    claim_base_ref = claim.get("base_state_revision_ref")
    if not isinstance(claim_base_ref, str) or not claim_base_ref:
        raise PacketModificationContextError(
            "exact claim exposes no usable base_state_revision_ref"
        )
    if claim_base_ref != packet_base_ref:
        raise PacketModificationContextError(
            "exact claim base does not equal the exact packet base"
        )

    resolved_lane = resolve_exact_revision_member(
        store,
        claim_base_ref,
        "lane_refs",
        "lane",
        claim["lane_id"],
    )

    occupancy_ref = claim.get("occupancy_ref")
    if not isinstance(occupancy_ref, str) or not occupancy_ref:
        raise PacketModificationContextError("exact claim exposes no usable occupancy_ref")
    occupancy = store.load(occupancy_ref, "occupancy.schema.json")
    occupancy_entry_base_ref = occupancy.get("base_state_revision_ref")
    if not isinstance(occupancy_entry_base_ref, str) or not occupancy_entry_base_ref:
        raise PacketModificationContextError(
            "exact occupancy exposes no usable base_state_revision_ref"
        )
    store.load(occupancy_entry_base_ref, "state-revision.schema.json")
    resolve_exact_revision_member(
        store,
        occupancy_entry_base_ref,
        "lane_refs",
        "lane",
        occupancy["lane_id"],
    )

    if occupancy.get("lane_id") != claim.get("lane_id"):
        raise PacketModificationContextError(
            "return-packet claim_ref occupancy relation names a different logical lane"
        )
    if claim.get("status") != "open":
        raise PacketModificationContextError(
            "modified-artifact preflight requires claim_ref to name an exact claim "
            "snapshot whose local status is 'open'; this does not establish global currentness"
        )
    if occupancy.get("status") != "active":
        raise PacketModificationContextError(
            "modified-artifact preflight requires claim_ref occupancy_ref to name an exact "
            "occupancy snapshot whose local status is 'active'; this does not establish "
            "global currentness"
        )

    return (
        packet,
        claim_ref,
        claim_base_ref,
        occupancy_ref,
        resolved_lane.reference,
        claim_base,
    )


def preflight_modified_artifact_identity(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedReturnPacketModifiedArtifacts:
    """Ground Decision 011's explicit two-sided modified-artifact identity only.

    Historical return-packet v0.3 remains valid historical state, but any non-empty
    v0.3 ``artifacts_modified`` list stays operationally unresolved: one opaque string
    is not reinterpreted as two exact artifact identities. Return-packet v0.4 expresses
    each relation explicitly as ``prior_artifact_ref`` plus ``result_artifact_ref``.

    For each v0.4 relation this function:

    * parses both endpoints through the shared Stage 2 immutable-reference parser and
      requires kind ``artifact``;
    * requires the exact prior ref to occur in the exact claim-base ``artifact_refs``;
    * exact-loads and identity-verifies that exact prior artifact;
    * exact-loads and identity-verifies the exact result artifact;
    * applies Decision 010's exact work-base / producer-lane provenance invariant to
      the result against the same exact claim base and claim-base lane.

    No logical-id equality, artifact version ordering, ``supersedes_ref`` authority,
    recency/currentness, storage/array order, actor identity, scheduler position,
    founder status, or Git permission participates in endpoint selection. The function
    is read-only and stops before lineage policy, evidence/source/dependency closure,
    packet acceptance, claim closure, successor publication, integration, epochs, or
    replay.
    """

    (
        packet,
        claim_ref,
        claim_base_ref,
        occupancy_ref,
        lane_ref,
        claim_base,
    ) = _ground_packet_context(store, packet_ref)

    modified_entries = packet.get("artifacts_modified", ())
    schema_version = packet.get("schema_version")
    if modified_entries and schema_version != "0.4":
        raise ModifiedArtifactContractVersionError(
            f"return-packet schema_version {schema_version!r} cannot ground two-sided "
            "modified-artifact identity; historical v0.3 opaque entries are not "
            "silently reinterpreted"
        )

    base_artifact_refs = claim_base.get("artifact_refs", ())
    if not isinstance(base_artifact_refs, (list, tuple)):
        raise PacketModificationContextError(
            "exact claim base exposes no usable artifact_refs membership family"
        )

    resolved: list[ResolvedModifiedArtifact] = []
    for index, relation in enumerate(modified_entries):
        field = f"$.artifacts_modified[{index}]"
        if not isinstance(relation, Mapping):
            raise ModifiedArtifactRelationShapeError(
                f"{field} is not the explicit v0.4 prior/result mapping"
            )

        prior_ref = relation.get("prior_artifact_ref")
        result_ref = relation.get("result_artifact_ref")
        if not isinstance(prior_ref, str) or not prior_ref:
            raise ModifiedArtifactRelationShapeError(
                f"{field}.prior_artifact_ref is missing or unusable"
            )
        if not isinstance(result_ref, str) or not result_ref:
            raise ModifiedArtifactRelationShapeError(
                f"{field}.result_artifact_ref is missing or unusable"
            )

        _parse_artifact_ref(prior_ref, field=f"{field}.prior_artifact_ref")
        if prior_ref not in base_artifact_refs:
            raise ModifiedArtifactPriorMembershipError(
                f"{field}.prior_artifact_ref does not name an exact artifact member of "
                f"claim base {claim_base_ref!r}"
            )
        prior_artifact = _load_artifact_relation(
            store,
            prior_ref,
            field=f"{field}.prior_artifact_ref",
        )

        result_artifact = _load_artifact_relation(
            store,
            result_ref,
            field=f"{field}.result_artifact_ref",
        )
        result_provenance = preflight_exact_artifact_work_base_provenance(
            store,
            result_artifact,
            claim_base_ref=claim_base_ref,
            lane_ref=lane_ref,
        )

        resolved.append(
            ResolvedModifiedArtifact(
                prior_artifact=prior_artifact,
                result_artifact=result_artifact,
                result_provenance=result_provenance,
            )
        )

    return ResolvedReturnPacketModifiedArtifacts(
        packet_ref=packet_ref,
        packet=_freeze_json(packet),
        claim_ref=claim_ref,
        claim_base_ref=claim_base_ref,
        occupancy_ref=occupancy_ref,
        lane_ref=lane_ref,
        modifications=tuple(resolved),
    )
