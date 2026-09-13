from __future__ import annotations

from typing import NamedTuple

from .identity import IdentityError, parse_immutable_ref
from .packet_mixed_compatibility import (
    ResolvedMixedPacketCompatibility,
    preflight_mixed_packet_compatibility,
)
from .packet_output_identity import ExactPacketRelation, _load_exact_relation
from .store import FilesystemObjectStore, ObjectStoreError


class OutputDependencyIdentityError(ObjectStoreError):
    """Base error for Decision 014 exact output dependency identity."""


class HistoricalDependencySemanticsUnresolvedError(OutputDependencyIdentityError):
    """Historical artifact dependency strings cannot be reinterpreted as exact refs."""


class OutputDependencyReferenceError(OutputDependencyIdentityError):
    """A v0.3 dependency ref is malformed, wrong-kind, missing, corrupt, or mismatched."""


class OutputDependencySchemaVersionError(OutputDependencyIdentityError):
    """An artifact version has no declared Decision 014 dependency semantics."""


class ResolvedOutputArtifactDependencies(NamedTuple):
    """Exact dependency identities declared by one exact packet output.

    ``category`` is only the Decision 013 output family label: ``created`` or
    ``modified_result``. ``dependencies`` preserves the declared presentation order but
    gives that order no authority. Each member is one exact immutable ref/value pair.
    """

    category: str
    artifact: ExactPacketRelation
    dependencies: tuple[ExactPacketRelation, ...]


class ResolvedPacketOutputDependencyIdentity(NamedTuple):
    """Read-only Decision 014 projection for one exact return packet.

    The mixed compatibility result remains the authority for exact packet/claim/base/
    occupancy/lane context and output categories. This wrapper adds only exact dependency
    target identity. It deliberately exposes no dependency-closure, aggregate-success,
    packet-acceptance, claim-closure, publication, integration, epoch, or replay field.
    """

    packet_ref: str
    claim_ref: str
    claim_base_ref: str
    occupancy_ref: str
    lane_ref: str
    mixed_compatibility: ResolvedMixedPacketCompatibility
    created_outputs: tuple[ResolvedOutputArtifactDependencies, ...]
    modified_results: tuple[ResolvedOutputArtifactDependencies, ...]


def _resolve_artifact_dependencies(
    store: FilesystemObjectStore,
    artifact: ExactPacketRelation,
    *,
    category: str,
) -> ResolvedOutputArtifactDependencies:
    schema_version = artifact.value.get("schema_version")
    dependency_refs = artifact.value.get("dependency_refs", ())
    if not isinstance(dependency_refs, (list, tuple)):
        raise OutputDependencyIdentityError(
            f"exact output artifact {artifact.reference!r} exposes no usable "
            "dependency_refs array"
        )

    if schema_version in ("0.1", "0.2"):
        if dependency_refs:
            raise HistoricalDependencySemanticsUnresolvedError(
                f"exact output artifact {artifact.reference!r} uses historical artifact "
                f"schema_version {schema_version!r} with non-empty dependency_refs; "
                "Decision 014 does not reinterpret historical path/logical/exact-looking "
                "strings as immutable dependency identities"
            )
        return ResolvedOutputArtifactDependencies(
            category=category,
            artifact=artifact,
            dependencies=(),
        )

    if schema_version != "0.3":
        raise OutputDependencySchemaVersionError(
            f"exact output artifact {artifact.reference!r} uses schema_version "
            f"{schema_version!r}; Decision 014 defines dependency identity only for "
            "historical v0.1/v0.2 and exact-dependency v0.3"
        )

    resolved: list[ExactPacketRelation] = []
    for index, reference in enumerate(dependency_refs):
        field = f"{category}:{artifact.reference}:dependency_refs[{index}]"
        if not isinstance(reference, str) or not reference:
            raise OutputDependencyReferenceError(
                f"{field} exposes no usable immutable dependency reference"
            )
        try:
            parsed = parse_immutable_ref(reference)
        except IdentityError as exc:
            raise OutputDependencyReferenceError(
                f"{field} is not a canonical immutable reference: {exc}"
            ) from exc
        if parsed.kind != "artifact":
            raise OutputDependencyReferenceError(
                f"{field} must have kind 'artifact', got {parsed.kind!r}"
            )
        try:
            relation = _load_exact_relation(
                store,
                reference,
                expected_kind="artifact",
                field=field,
            )
        except ObjectStoreError as exc:
            raise OutputDependencyReferenceError(
                f"{field} could not be exact-loaded and identity-verified: {exc}"
            ) from exc
        if relation.reference != reference:
            raise OutputDependencyReferenceError(
                f"{field} exact-load returned a different immutable reference"
            )
        resolved.append(relation)

    return ResolvedOutputArtifactDependencies(
        category=category,
        artifact=artifact,
        dependencies=tuple(resolved),
    )


def preflight_output_dependency_identity(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedPacketOutputDependencyIdentity:
    """Resolve Decision 014 exact dependency targets for Decision 013 packet outputs.

    The function first consumes the canonical mixed created+modified compatibility
    projection. It does not rebuild packet, claim, base, occupancy, lane, output, or
    evidence selection through a parallel authority path.

    For each exact created output and exact modification-result output:

    * artifact v0.3 dependency refs are parsed through the shared Stage 2 immutable-ref
      language, required to have kind ``artifact``, exact-loaded, and returned as exact
      ref/value pairs;
    * historical v0.1/v0.2 artifacts with empty dependency arrays continue because they
      assert no dependency target on this surface;
    * historical v0.1/v0.2 artifacts with non-empty dependency arrays fail closed even
      when a string happens to resemble a canonical immutable ref.

    A successful result establishes dependency target identity only. It does not establish
    base membership, chronology, same-packet dependency validity, transitive closure,
    cycle freedom, completeness, source provenance closure, evidence precedence, lineage,
    packet acceptance, claim closure, successor publication, integration, epochs, or
    replay. ``source_refs``, ``evidence_refs``, ``content_ref``, ``version``, and
    ``supersedes_ref`` do not participate in dependency selection.
    """

    mixed = preflight_mixed_packet_compatibility(store, packet_ref)

    created = tuple(
        _resolve_artifact_dependencies(
            store,
            item.artifact,
            category="created",
        )
        for item in mixed.created_outputs
    )
    modified = tuple(
        _resolve_artifact_dependencies(
            store,
            item.modification.result_artifact,
            category="modified_result",
        )
        for item in mixed.modified_results
    )

    return ResolvedPacketOutputDependencyIdentity(
        packet_ref=mixed.packet_ref,
        claim_ref=mixed.claim_ref,
        claim_base_ref=mixed.claim_base_ref,
        occupancy_ref=mixed.occupancy_ref,
        lane_ref=mixed.lane_ref,
        mixed_compatibility=mixed,
        created_outputs=created,
        modified_results=modified,
    )
