from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .integration_receipt_identity import validate_exact_integration_receipt_identity
from .packet_integration_eligibility import (
    ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE,
    ResolvedPacketIntegrationEligibility,
    preflight_packet_integration_eligibility,
)
from .store import FilesystemObjectStore


COHERENT_STAGE5_ACCEPTANCE_CANDIDATE_BINDING = (
    "coherent_stage5_acceptance_candidate_binding"
)
UNSUPPORTED_MULTI_PACKET_RECEIPT_SLICE = "unsupported_multi_packet_receipt_slice"
RECEIPT_PACKET_NOT_ELIGIBLE = "receipt_packet_not_eligible"
RECEIPT_BASE_MISMATCH = "receipt_base_mismatch"
RECEIPT_PACKET_MISMATCH = "receipt_packet_mismatch"
NON_ACCEPTING_RECEIPT_DECISION = "non_accepting_receipt_decision"


@dataclass(frozen=True)
class IntegrationCandidateBindingReason:
    """Deterministic named reason for one Decision 026 disposition."""

    code: str
    related_refs: tuple[str, ...]


@dataclass(frozen=True)
class ResolvedIntegrationCandidateBinding:
    """Read-only Decision 026 binding between exact stored Stage 5 inputs.

    A positive outcome means only that one proposed v0.2 receipt, one exact stored
    base revision, one exact stored packet, and the canonical Decision 024 eligibility
    fact are mutually coherent for the first bounded acceptance-candidate slice.

    ``base_materialized`` and ``packet_materialized`` are tri-state facts: ``True``
    means the exact load completed; ``None`` means Decision 026 deliberately did not
    attempt materialization because the receipt was already outside the one-packet
    first slice. Typed load failures propagate instead of being rewritten as ``False``.

    This result does not publish the receipt, accept the packet, construct or publish a
    successor revision, close a claim/occupancy, complete an epoch, establish replay,
    approve root reasoning, or grant authority from actor identity, schedule, CI,
    branch state, or Git permission.
    """

    receipt_ref: str
    receipt_decision: str
    base_state_revision_ref: str
    packet_refs: tuple[str, ...]
    base_materialized: bool | None
    packet_materialized: bool | None
    packet_eligibility: ResolvedPacketIntegrationEligibility | None
    candidate_binding_outcome: str
    reasons: tuple[IntegrationCandidateBindingReason, ...]


def _result(
    *,
    receipt_ref: str,
    receipt_decision: str,
    base_ref: str,
    packet_refs: tuple[str, ...],
    base_materialized: bool | None,
    packet_materialized: bool | None,
    eligibility: ResolvedPacketIntegrationEligibility | None,
    outcome: str,
    reasons: tuple[IntegrationCandidateBindingReason, ...],
) -> ResolvedIntegrationCandidateBinding:
    return ResolvedIntegrationCandidateBinding(
        receipt_ref=receipt_ref,
        receipt_decision=receipt_decision,
        base_state_revision_ref=base_ref,
        packet_refs=packet_refs,
        base_materialized=base_materialized,
        packet_materialized=packet_materialized,
        packet_eligibility=eligibility,
        candidate_binding_outcome=outcome,
        reasons=reasons,
    )


def preflight_exact_stored_integration_candidate_binding(
    store: FilesystemObjectStore,
    receipt: Mapping[str, Any],
) -> ResolvedIntegrationCandidateBinding:
    """Compose Decision 025 exact receipt identity with Decision 024 eligibility.

    The proposed receipt is validated through the canonical Decision 025 path first.
    The first Decision 026 slice supports exactly one packet reference. For that slice,
    the receipt's exact base and packet are exact-loaded through the immutable store,
    then Decision 024 eligibility is recomputed from that exact packet. Exact packet and
    base identities must agree across both facts.

    Existing typed identity/store failures deliberately propagate. In particular, a
    well-formed but absent or corrupt exact reference is not converted into a weaker
    local status. This function performs no writes and introduces no logical-id,
    current/newest/HEAD, actor, schedule, CI, branch, or Git fallback.
    """

    identity = validate_exact_integration_receipt_identity(receipt, store.schema_dir)
    receipt_ref = identity.immutable_ref
    receipt_decision = receipt["decision"]
    base_ref = str(identity.base_state_revision_ref)
    packet_refs = tuple(str(reference) for reference in identity.packet_refs)

    if len(packet_refs) != 1:
        return _result(
            receipt_ref=receipt_ref,
            receipt_decision=receipt_decision,
            base_ref=base_ref,
            packet_refs=packet_refs,
            base_materialized=None,
            packet_materialized=None,
            eligibility=None,
            outcome=UNSUPPORTED_MULTI_PACKET_RECEIPT_SLICE,
            reasons=(
                IntegrationCandidateBindingReason(
                    code="multiple_packet_refs_outside_first_slice",
                    related_refs=tuple(sorted(packet_refs)),
                ),
            ),
        )

    packet_ref = packet_refs[0]

    # Preserve the supplied-store exact-load paths, but do not let caller-owned
    # instance dispatch alone establish either stronger materialization fact.
    # Independently reproduce the exact receipt base and packet through the canonical
    # base-class loads; typed absence/corruption/reference failures remain stronger
    # facts and propagate before any True materialization result can be emitted.
    store.load(base_ref, "state-revision.schema.json")
    FilesystemObjectStore.load(store, base_ref, "state-revision.schema.json")
    store.load(packet_ref, "return-packet.schema.json")
    FilesystemObjectStore.load(store, packet_ref, "return-packet.schema.json")

    eligibility = preflight_packet_integration_eligibility(store, packet_ref)

    if eligibility.packet_ref != packet_ref:
        return _result(
            receipt_ref=receipt_ref,
            receipt_decision=receipt_decision,
            base_ref=base_ref,
            packet_refs=packet_refs,
            base_materialized=True,
            packet_materialized=True,
            eligibility=eligibility,
            outcome=RECEIPT_PACKET_MISMATCH,
            reasons=(
                IntegrationCandidateBindingReason(
                    code="decision024_packet_ref_mismatch",
                    related_refs=tuple(sorted((packet_ref, eligibility.packet_ref))),
                ),
            ),
        )

    if eligibility.base_state_revision_ref != base_ref:
        return _result(
            receipt_ref=receipt_ref,
            receipt_decision=receipt_decision,
            base_ref=base_ref,
            packet_refs=packet_refs,
            base_materialized=True,
            packet_materialized=True,
            eligibility=eligibility,
            outcome=RECEIPT_BASE_MISMATCH,
            reasons=(
                IntegrationCandidateBindingReason(
                    code="decision024_base_ref_mismatch",
                    related_refs=tuple(
                        sorted((base_ref, eligibility.base_state_revision_ref))
                    ),
                ),
            ),
        )

    if eligibility.eligibility_outcome != ELIGIBLE_FOR_STAGE5_ACCEPTANCE_CANDIDATE:
        return _result(
            receipt_ref=receipt_ref,
            receipt_decision=receipt_decision,
            base_ref=base_ref,
            packet_refs=packet_refs,
            base_materialized=True,
            packet_materialized=True,
            eligibility=eligibility,
            outcome=RECEIPT_PACKET_NOT_ELIGIBLE,
            reasons=(
                IntegrationCandidateBindingReason(
                    code="decision024_outcome_not_eligible",
                    related_refs=(packet_ref,),
                ),
            ),
        )

    if receipt_decision != "accepted":
        return _result(
            receipt_ref=receipt_ref,
            receipt_decision=receipt_decision,
            base_ref=base_ref,
            packet_refs=packet_refs,
            base_materialized=True,
            packet_materialized=True,
            eligibility=eligibility,
            outcome=NON_ACCEPTING_RECEIPT_DECISION,
            reasons=(
                IntegrationCandidateBindingReason(
                    code="receipt_decision_not_accepted",
                    related_refs=(receipt_ref,),
                ),
            ),
        )

    return _result(
        receipt_ref=receipt_ref,
        receipt_decision=receipt_decision,
        base_ref=base_ref,
        packet_refs=packet_refs,
        base_materialized=True,
        packet_materialized=True,
        eligibility=eligibility,
        outcome=COHERENT_STAGE5_ACCEPTANCE_CANDIDATE_BINDING,
        reasons=(
            IntegrationCandidateBindingReason(
                code="exact_stored_receipt_packet_base_binding_coherent",
                related_refs=(base_ref, packet_ref),
            ),
        ),
    )
