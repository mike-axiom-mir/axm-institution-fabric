from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Mapping

from .identity import ContractValidationError, validate_instance
from .resolution import resolve_exact_revision_member
from .store import FilesystemObjectStore


@dataclass(frozen=True)
class OccupancyAdmissionResult:
    """Bounded result of grounding and immutably storing one occupancy.

    This result records only the exact stored occupancy identity and the exact lane
    identity resolved inside the named entry base. It does not publish a successor
    state revision and does not assert that the occupancy is current/canonical state.
    """

    occupancy_ref: str
    lane_ref: str
    created: bool


@dataclass(frozen=True)
class WorkClaimAdmissionResult:
    """Bounded result of grounding and immutably storing one opening work claim.

    The result records exact immutable identities only. It does not publish a
    successor state revision, establish global occupancy currentness, arbitrate
    overlap, mutate occupancy claim snapshots, or grant ownership/locking authority.
    """

    claim_ref: str
    occupancy_ref: str
    lane_ref: str
    created: bool


@dataclass(frozen=True)
class ReturnPacketAdmissionResult:
    """Bounded result of grounding and immutably storing one return packet.

    The result records the exact packet, claim, occupancy, and claim-base lane
    identities whose relationships were grounded. It does not close the claim,
    publish a successor revision, validate artifact/evidence closure, integrate the
    packet, or establish global currentness/authorization for any lifecycle object.
    """

    packet_ref: str
    claim_ref: str
    occupancy_ref: str
    lane_ref: str
    created: bool


def admit_occupancy(
    store: FilesystemObjectStore,
    occupancy: Mapping[str, Any],
) -> OccupancyAdmissionResult:
    """Admit one occupancy against the lane recorded in its exact entry base.

    One function-owned deep snapshot is created before validation or dependency
    grounding. The same detached candidate is then used through validation, exact
    base loading, exact lane resolution, identity derivation inside the store, and
    final immutable publication. Caller mutation after entry therefore cannot silently
    change the authoritative occupancy that gets persisted after a different relation
    was grounded.

    The occupancy contract is validated first. Its exact ``base_state_revision_ref``
    must then load as a state revision, and ``lane_id`` must resolve to exactly one
    immutable lane member inside that base. Only after those checks succeed is the
    occupancy itself persisted immutably.

    No mutable/current revision pointer, recency, array order, actor identity,
    capability identity, schedule position, founder status, or conversational state
    participates in lane selection. ``claim_ids`` remains snapshot/navigation data;
    this primitive does not create or resolve claims and does not synthesize a
    successor institutional revision.
    """

    candidate = copy.deepcopy(dict(occupancy))
    validated = validate_instance(candidate, "occupancy.schema.json", store.schema_dir)
    base_revision_ref = validated["base_state_revision_ref"]

    # Make the exact entry base an explicit prerequisite before any relationship is
    # treated as operationally valid. The resolver exact-loads it again while checking
    # its lane family; the deliberate duplication keeps this runtime boundary obvious
    # rather than turning an indirect helper side effect into lifecycle authority.
    store.load(base_revision_ref, "state-revision.schema.json")

    resolved_lane = resolve_exact_revision_member(
        store,
        base_revision_ref,
        "lane_refs",
        "lane",
        validated["lane_id"],
    )

    write_result = store.store(validated, "occupancy.schema.json")
    return OccupancyAdmissionResult(
        occupancy_ref=write_result.reference,
        lane_ref=resolved_lane.reference,
        created=write_result.created,
    )


def open_work_claim(
    store: FilesystemObjectStore,
    claim: Mapping[str, Any],
) -> WorkClaimAdmissionResult:
    """Ground and immutably persist one opening work claim.

    The caller's mapping is detached before validation so proof and publication bind
    the same function-owned candidate. The candidate must be a contract-valid claim
    whose local lifecycle state is ``open``. Its named exact base must exist, its
    logical lane must resolve exactly once from that base, and its authoritative
    post-base ``occupancy_ref`` must exact-load as the immutable occupancy instance it
    names before the claim is persisted.

    Exact object presence is not treated as proof that the occupancy's own historical
    admission relation was grounded. Before operational use, the loaded occupancy's
    exact ``base_state_revision_ref`` must itself load as a state revision and the
    occupancy's logical ``lane_id`` must resolve exactly once from that entry base.
    The occupancy entry base may differ from the claim base; each relation is grounded
    against its own exact historical revision.

    The exact occupancy and claim must name the same persistent logical lane. This
    primitive also requires the loaded occupancy snapshot itself to say ``active``;
    that is only a necessary property of this exact snapshot and is not evidence that
    the occupancy is globally current, unsuperseded, authorized, or scheduler-owned.

    ``occupancy.claim_ids`` and ``work-claim.overlap_with_claim_ids`` remain
    snapshot/reporting data. This primitive performs no overlap arbitration, locking,
    occupancy mutation, stale/current revision policy, claim closure/supersession,
    return submission, successor-revision publication, integration, epoch handling,
    or replay.
    """

    candidate = copy.deepcopy(dict(claim))
    validated = validate_instance(candidate, "work-claim.schema.json", store.schema_dir)

    if validated["status"] != "open":
        raise ContractValidationError(
            "open_work_claim requires the exact claim candidate to have status 'open'"
        )

    base_revision_ref = validated["base_state_revision_ref"]
    store.load(base_revision_ref, "state-revision.schema.json")

    resolved_lane = resolve_exact_revision_member(
        store,
        base_revision_ref,
        "lane_refs",
        "lane",
        validated["lane_id"],
    )

    occupancy_ref = validated["occupancy_ref"]
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

    if occupancy["lane_id"] != validated["lane_id"]:
        raise ContractValidationError(
            "work-claim lane_id does not match the exact occupancy_ref lane_id"
        )
    if occupancy["status"] != "active":
        raise ContractValidationError(
            "open_work_claim requires occupancy_ref to name an occupancy snapshot "
            "whose local status is 'active'; this does not establish global currentness"
        )

    write_result = store.store(validated, "work-claim.schema.json")
    return WorkClaimAdmissionResult(
        claim_ref=write_result.reference,
        occupancy_ref=occupancy_ref,
        lane_ref=resolved_lane.reference,
        created=write_result.created,
    )


def submit_return_packet(
    store: FilesystemObjectStore,
    packet: Mapping[str, Any],
) -> ReturnPacketAdmissionResult:
    """Ground and immutably persist one bounded return-packet handoff.

    The caller mapping is deep-copied before any validation or dependency grounding,
    and that same function-owned candidate is used for final publication. The packet's
    exact base and exact ``claim_ref`` must exist. Packet base and lane must match the
    exact claim's base and lane; this primitive never silently rebases a handoff.

    Exact claim presence is not itself lifecycle authority. Before the claim is used
    operationally, its own exact base/lane relation and its exact occupancy relation
    are reconstructed. The occupancy's own historical entry-base/lane relation is also
    reconstructed. Claim and occupancy must still name the same persistent logical
    lane. Only the exact snapshots' local ``open``/``active`` statuses are required;
    those local states are not relabeled as global currentness, authorization,
    supersession, scheduling authority, or scope ownership.

    The packet's changes, artifact arrays, evidence refs, uncertainties,
    failures/blockers, downstream effects, and requested follow-up are persisted as
    supplied by the validated candidate. This primitive does not dereference those
    artifact/evidence entries, assert lane-output compatibility or evidence closure,
    mutate the claim to submitted, publish a successor revision, integrate anything,
    open an epoch, or produce replay evidence.
    """

    candidate = copy.deepcopy(dict(packet))
    validated = validate_instance(candidate, "return-packet.schema.json", store.schema_dir)

    packet_base_ref = validated["base_state_revision_ref"]
    store.load(packet_base_ref, "state-revision.schema.json")

    claim_ref = validated["claim_ref"]
    claim = store.load(claim_ref, "work-claim.schema.json")

    if packet_base_ref != claim["base_state_revision_ref"]:
        raise ContractValidationError(
            "return-packet base_state_revision_ref does not match the exact claim_ref base"
        )
    if validated["lane_id"] != claim["lane_id"]:
        raise ContractValidationError(
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

    occupancy_ref = claim["occupancy_ref"]
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

    if occupancy["lane_id"] != claim["lane_id"]:
        raise ContractValidationError(
            "return-packet claim_ref occupancy relation names a different logical lane"
        )
    if claim["status"] != "open":
        raise ContractValidationError(
            "submit_return_packet requires claim_ref to name a claim snapshot whose "
            "local status is 'open'; this does not establish global currentness"
        )
    if occupancy["status"] != "active":
        raise ContractValidationError(
            "submit_return_packet requires claim_ref occupancy_ref to name an occupancy "
            "snapshot whose local status is 'active'; this does not establish global currentness"
        )

    write_result = store.store(validated, "return-packet.schema.json")
    return ReturnPacketAdmissionResult(
        packet_ref=write_result.reference,
        claim_ref=claim_ref,
        occupancy_ref=occupancy_ref,
        lane_ref=resolved_lane.reference,
        created=write_result.created,
    )
