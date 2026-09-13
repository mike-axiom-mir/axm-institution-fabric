from __future__ import annotations

from typing import NamedTuple

from .packet_output_dependency_identity import (
    ResolvedOutputArtifactDependencies,
    ResolvedPacketOutputDependencyIdentity,
    preflight_output_dependency_identity,
)
from .packet_output_identity import ExactPacketRelation, _load_exact_relation
from .store import FilesystemObjectStore, ObjectStoreError


class DependencyContextMembershipError(ObjectStoreError):
    """Base error for Decision 015 exact dependency-context membership."""


class DependencyContextClaimBaseError(DependencyContextMembershipError):
    """The exact claim-base state revision could not be re-grounded safely."""


class ExactDependencyContextMembership(NamedTuple):
    """Factual exact-ref context membership for one Decision 014 dependency.

    The three booleans are independent facts. More than one may be true and no field has
    precedence over another. All false means only that the exact target is outside the
    claim-base artifact membership and both packet output families on this bounded
    projection; it is not an acceptance/rejection or validity result.
    """

    dependency: ExactPacketRelation
    in_claim_base: bool
    in_packet_created: bool
    in_packet_modified_result: bool


class ResolvedOutputDependencyContext(NamedTuple):
    """Decision 015 dependency-context facts for one exact packet output."""

    category: str
    artifact: ExactPacketRelation
    dependencies: tuple[ExactDependencyContextMembership, ...]


class ResolvedPacketDependencyContextMembership(NamedTuple):
    """Read-only Decision 015 projection over one Decision 014 result.

    ``dependency_identity`` remains the authority for exact packet/output/dependency
    selection. ``claim_base`` is re-grounded through the same exact immutable-reference
    and object-store path before its ``artifact_refs`` membership is used.

    This type intentionally exposes no dependency-validity, dependency-closure,
    aggregate-success, packet-acceptance, claim-closure, publication, integration, epoch,
    or replay field.
    """

    packet_ref: str
    claim_ref: str
    claim_base_ref: str
    occupancy_ref: str
    lane_ref: str
    dependency_identity: ResolvedPacketOutputDependencyIdentity
    claim_base: ExactPacketRelation
    created_outputs: tuple[ResolvedOutputDependencyContext, ...]
    modified_results: tuple[ResolvedOutputDependencyContext, ...]


def _classify_output_dependencies(
    output: ResolvedOutputArtifactDependencies,
    *,
    claim_base_artifact_refs: frozenset[str],
    created_output_refs: frozenset[str],
    modified_result_refs: frozenset[str],
) -> ResolvedOutputDependencyContext:
    facts = tuple(
        ExactDependencyContextMembership(
            dependency=dependency,
            in_claim_base=dependency.reference in claim_base_artifact_refs,
            in_packet_created=dependency.reference in created_output_refs,
            in_packet_modified_result=dependency.reference in modified_result_refs,
        )
        for dependency in output.dependencies
    )
    return ResolvedOutputDependencyContext(
        category=output.category,
        artifact=output.artifact,
        dependencies=facts,
    )


def preflight_dependency_context_membership(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedPacketDependencyContextMembership:
    """Classify exact dependency targets by exact historical/packet context.

    Decision 014 remains the sole authority for exact packet context, exact output
    families, and exact dependency target selection. This function adds only factual
    membership observations:

    * exact equality with one member of the exact claim-base ``artifact_refs[]`` set;
    * exact equality with a packet-created output ref;
    * exact equality with a packet modification-result output ref.

    The exact claim base is re-loaded and identity-verified as a ``state-revision`` before
    its member refs are consulted. No logical-id, version, ``supersedes_ref``, recency,
    store order, dependency/output array order, source/evidence metadata, actor identity,
    scheduler position, or Git permission participates in classification.

    All membership booleans are independent. An exact dependency outside every listed
    context remains represented with all three flags false; it is not silently rejected or
    promoted to valid. A target present in more than one context retains every true fact.

    A successful result does not establish dependency validity, chronology, self-
    dependency policy, transitive closure, cycle freedom, declaration completeness,
    source/evidence closure, lineage, packet acceptance/rejection, claim closure,
    successor publication, Stage 5 integration, epochs/barriers, or replay correctness.
    """

    dependency_identity = preflight_output_dependency_identity(store, packet_ref)

    try:
        claim_base = _load_exact_relation(
            store,
            dependency_identity.claim_base_ref,
            expected_kind="state-revision",
            field="Decision015.claim_base_ref",
        )
    except ObjectStoreError as exc:
        raise DependencyContextClaimBaseError(
            "Decision 015 could not exact-load and identity-verify the exact claim-base "
            f"state revision {dependency_identity.claim_base_ref!r}: {exc}"
        ) from exc

    artifact_refs_value = claim_base.value.get("artifact_refs", ())
    try:
        claim_base_artifact_refs = frozenset(artifact_refs_value)
    except TypeError as exc:
        # A valid exact state revision currently makes this unreachable, but preserve the
        # boundary explicitly for future store/schema implementations rather than treating
        # a malformed operational value as an empty membership set.
        raise DependencyContextClaimBaseError(
            "Decision 015 exact claim base exposes no usable artifact_refs membership"
        ) from exc

    created_output_refs = frozenset(
        output.artifact.reference for output in dependency_identity.created_outputs
    )
    modified_result_refs = frozenset(
        output.artifact.reference for output in dependency_identity.modified_results
    )

    created = tuple(
        _classify_output_dependencies(
            output,
            claim_base_artifact_refs=claim_base_artifact_refs,
            created_output_refs=created_output_refs,
            modified_result_refs=modified_result_refs,
        )
        for output in dependency_identity.created_outputs
    )
    modified = tuple(
        _classify_output_dependencies(
            output,
            claim_base_artifact_refs=claim_base_artifact_refs,
            created_output_refs=created_output_refs,
            modified_result_refs=modified_result_refs,
        )
        for output in dependency_identity.modified_results
    )

    return ResolvedPacketDependencyContextMembership(
        packet_ref=dependency_identity.packet_ref,
        claim_ref=dependency_identity.claim_ref,
        claim_base_ref=dependency_identity.claim_base_ref,
        occupancy_ref=dependency_identity.occupancy_ref,
        lane_ref=dependency_identity.lane_ref,
        dependency_identity=dependency_identity,
        claim_base=claim_base,
        created_outputs=created,
        modified_results=modified,
    )
