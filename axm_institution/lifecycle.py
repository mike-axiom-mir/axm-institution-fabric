from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any, Mapping

from .identity import validate_instance
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
