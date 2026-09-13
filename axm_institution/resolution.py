from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .identity import ImmutableReferenceError, parse_immutable_ref
from .store import FilesystemObjectStore, ObjectStoreError


class RevisionMemberResolutionError(ObjectStoreError):
    """Base error for exact base-local state-revision member resolution."""


class RevisionMemberConfigurationError(RevisionMemberResolutionError):
    """The requested membership field/kind combination is not an allowed contract."""


class RevisionMemberNotFoundError(RevisionMemberResolutionError):
    """No exact member in the requested base-local family has the logical id."""


class RevisionMemberAmbiguityError(RevisionMemberResolutionError):
    """More than one exact base-local member has the requested logical id."""


@dataclass(frozen=True)
class ResolvedRevisionMember:
    """One exact immutable member selected from one exact state revision."""

    reference: str
    value: Mapping[str, Any]


# This table mirrors the membership families already defined by state-revision v0.2.
# It is intentionally explicit rather than inferred from filenames or mutable registry
# state, so callers cannot turn recency/current state into hidden resolution authority.
_REVISION_MEMBER_FAMILIES: Mapping[str, tuple[str, bool]] = {
    "parent_revision_ref": ("state-revision", False),
    "objective_ref": ("objective", False),
    "lane_refs": ("lane", True),
    "occupancy_refs": ("occupancy", True),
    "claim_refs": ("work-claim", True),
    "artifact_refs": ("artifact", True),
    "evidence_refs": ("evidence-record", True),
    "return_packet_refs": ("return-packet", True),
    "integration_receipt_refs": ("integration-receipt", True),
}


def resolve_exact_revision_member(
    store: FilesystemObjectStore,
    base_revision_ref: str,
    member_field: str,
    required_kind: str,
    logical_id: str,
) -> ResolvedRevisionMember:
    """Resolve exactly one immutable member from one exact immutable base revision.

    Resolution authority comes only from the exact membership recorded by
    ``base_revision_ref``. Every referenced object in the selected membership family is
    loaded and identity-verified through the immutable store before its logical id is
    considered. No newest/current pointer, array order, recency, actor identity,
    schedule order, or hidden conversational context participates.

    This is a read-only primitive. It does not claim the entire revision is
    referentially closed and it does not decide which lifecycle relationships should
    use base-local resolution.
    """

    try:
        parsed_base = parse_immutable_ref(base_revision_ref)
    except ImmutableReferenceError:
        # Preserve the identity-layer error exactly: malformed/noncanonical base refs
        # are not converted into a softer lookup miss.
        raise

    if parsed_base.kind != "state-revision":
        raise RevisionMemberConfigurationError(
            f"base reference kind {parsed_base.kind!r} is not 'state-revision'"
        )

    family = _REVISION_MEMBER_FAMILIES.get(member_field)
    if family is None:
        raise RevisionMemberConfigurationError(
            f"unsupported state-revision membership field: {member_field!r}"
        )

    expected_kind, is_array = family
    if required_kind != expected_kind:
        raise RevisionMemberConfigurationError(
            f"membership field {member_field!r} requires kind {expected_kind!r}, "
            f"got {required_kind!r}"
        )
    if not isinstance(logical_id, str) or not logical_id:
        raise RevisionMemberConfigurationError("logical_id must be a non-empty string")

    base_revision = store.load(base_revision_ref, "state-revision.schema.json")
    raw_members = base_revision.get(member_field)
    if is_array:
        member_refs = tuple(raw_members)
    elif raw_members is None:
        member_refs = ()
    else:
        member_refs = (raw_members,)

    matches: list[ResolvedRevisionMember] = []
    member_schema = f"{required_kind}.schema.json"

    for member_ref in member_refs:
        parsed_member = parse_immutable_ref(member_ref)
        if parsed_member.kind != required_kind:
            # A current valid state-revision object should already make this
            # impossible, but keeping the failure explicit protects historical or
            # externally supplied store implementations from silent reinterpretation.
            raise RevisionMemberResolutionError(
                f"member {member_ref!r} in {member_field!r} has kind "
                f"{parsed_member.kind!r}, expected {required_kind!r}"
            )

        # Load every exact member in the selected family before deciding whether it is
        # a match. A missing or corrupt referenced object therefore fails loudly rather
        # than being skipped because its encoded logical id did not happen to match.
        member = store.load(member_ref, member_schema)
        member_id = member.get("id")
        if member_id != parsed_member.logical_id:
            raise RevisionMemberResolutionError(
                f"verified member {member_ref!r} exposes logical id {member_id!r}, "
                f"not reference id {parsed_member.logical_id!r}"
            )
        if member_id == logical_id:
            matches.append(ResolvedRevisionMember(reference=member_ref, value=member))

    if not matches:
        raise RevisionMemberNotFoundError(
            f"no {required_kind!r} member with logical id {logical_id!r} exists in "
            f"{member_field!r} of exact base {base_revision_ref}"
        )
    if len(matches) != 1:
        raise RevisionMemberAmbiguityError(
            f"{len(matches)} exact {required_kind!r} members with logical id "
            f"{logical_id!r} exist in {member_field!r} of exact base "
            f"{base_revision_ref}; expected exactly one"
        )
    return matches[0]
