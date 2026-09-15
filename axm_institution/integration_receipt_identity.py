from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .identity import (
    ContractValidationError,
    IdentityError,
    ImmutableRef,
    canonical_validated_sha256,
    make_immutable_ref,
    parse_immutable_ref,
    validate_instance,
)

_SCHEMA_NAME = "integration-receipt.schema.json"


class HistoricalReceiptInsufficientError(ContractValidationError):
    """A readable historical receipt does not establish Decision 025 exact input identity."""


@dataclass(frozen=True)
class ExactIntegrationReceiptIdentity:
    """Exact Decision 025 receipt inputs plus deterministic receipt identity."""

    receipt_id: str
    base_state_revision_ref: ImmutableRef
    packet_refs: tuple[ImmutableRef, ...]
    canonical_sha256: str
    immutable_ref: str


def _parse_expected_ref(reference: str, expected_kind: str, location: str) -> ImmutableRef:
    try:
        parsed = parse_immutable_ref(reference)
    except IdentityError as exc:
        raise ContractValidationError(
            f"{_SCHEMA_NAME} semantic reference validation failed at {location}: {exc}"
        ) from exc
    if parsed.kind != expected_kind:
        raise ContractValidationError(
            f"{_SCHEMA_NAME} semantic reference validation failed at {location}: "
            f"expected kind {expected_kind!r}, got {parsed.kind!r}"
        )
    return parsed


def validate_exact_integration_receipt_identity(
    value: Mapping[str, Any],
    schema_dir: Path | None = None,
) -> ExactIntegrationReceiptIdentity:
    """Validate the bounded Decision 025 exact-input receipt contract.

    Historical v0.1 receipts remain valid under the versioned schema, but this
    function refuses to promote their logical ids into exact Stage 5 proof.

    V0.2 uses the shared Stage 2 immutable-reference parser for both the exact
    base revision and every exact return-packet reference. This function does
    not exact-load those objects, publish a successor, mutate state, decide
    constitutional acceptance, close claims, or implement replay.
    """

    validated = validate_instance(value, _SCHEMA_NAME, schema_dir)
    if validated.get("schema_version") != "0.2":
        raise HistoricalReceiptInsufficientError(
            "integration-receipt v0.1 remains readable historical data but "
            "does not establish Decision 025 exact base/packet identity"
        )

    base_reference = validated["base_state_revision_ref"]
    packet_references = validated["packet_refs"]

    parsed_base = _parse_expected_ref(
        base_reference,
        "state-revision",
        "$.base_state_revision_ref",
    )
    parsed_packets = tuple(
        _parse_expected_ref(reference, "return-packet", f"$.packet_refs[{index}]")
        for index, reference in enumerate(packet_references)
    )

    return ExactIntegrationReceiptIdentity(
        receipt_id=validated["id"],
        base_state_revision_ref=parsed_base,
        packet_refs=parsed_packets,
        canonical_sha256=canonical_validated_sha256(
            validated,
            _SCHEMA_NAME,
            schema_dir,
        ),
        immutable_ref=make_immutable_ref(
            _SCHEMA_NAME,
            validated,
            schema_dir,
        ),
    )
