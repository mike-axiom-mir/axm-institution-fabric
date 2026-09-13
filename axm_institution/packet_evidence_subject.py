from __future__ import annotations

from typing import Any, Mapping, NamedTuple

from .identity import IdentityError, parse_immutable_ref
from .packet_output_identity import (
    ExactPacketRelation,
    ResolvedReturnPacketOutputIdentity,
    ReturnPacketOutputIdentityError,
    resolve_return_packet_output_identity,
)
from .store import FilesystemObjectStore


class EvidenceSubjectResolutionError(ReturnPacketOutputIdentityError):
    """Base error for exact evidence-to-created-artifact subject resolution."""


class EvidenceSubjectKindError(EvidenceSubjectResolutionError):
    """An exact evidence subject uses a kind other than ``artifact``."""


class UnmatchedEvidenceSubject(NamedTuple):
    """One packet evidence record that cannot support a created artifact in this slice.

    ``reason`` is intentionally descriptive rather than a compatibility verdict. Evidence
    may remain valid for another purpose even when it cannot satisfy the exact created-
    artifact subject precondition opened by Decision 008.

    A tuple-backed record is used intentionally rather than a frozen dataclass. The
    subject-binding projection is handed to later stages as operational continuity state;
    ``object.__setattr__`` must not be able to rewrite that projection after exact subject
    grounding has already succeeded (ADV-039).
    """

    evidence: ExactPacketRelation
    subject_ref: str
    reason: str


class ExactCreatedArtifactEvidenceBinding(NamedTuple):
    """Evidence records whose subject is one exact packet-created artifact instance.

    The tuple-backed wrapper is physically non-assignable through the demonstrated
    ``object.__setattr__`` path, so caller access to the returned projection cannot silently
    replace the grounded evidence tuple with unrelated exact evidence (ADV-039-A).
    """

    artifact: ExactPacketRelation
    evidence_records: tuple[ExactPacketRelation, ...]


class ResolvedReturnPacketEvidenceSubjects(NamedTuple):
    """Read-only exact subject binding for one already-grounded return packet.

    This result proves only that each bound evidence record explicitly names the exact
    immutable packet-created artifact ref it is grouped under. The tuple-backed result
    also keeps explicit unmatched evidence non-assignable through the demonstrated
    ``object.__setattr__`` path (ADV-039-B).

    It does not decide lane output compatibility, required-state semantics, evidence
    quality/closure, artifact provenance, packet acceptance, claim closure, successor
    publication, integration, epochs, or replay.
    """

    output_identity: ResolvedReturnPacketOutputIdentity
    created_artifact_bindings: tuple[ExactCreatedArtifactEvidenceBinding, ...]
    unmatched_evidence: tuple[UnmatchedEvidenceSubject, ...]


def _subject_ref(evidence: Mapping[str, Any]) -> str:
    subject_ref = evidence.get("subject_ref")
    if not isinstance(subject_ref, str) or not subject_ref:
        # Exact packet-output identity loading already validates the evidence schema, so
        # reaching this branch means a future alternate relation provider violated that
        # grounded contract. Do not invent a fallback interpretation.
        raise EvidenceSubjectResolutionError(
            "exact evidence relation exposes no usable subject_ref"
        )
    return subject_ref


def resolve_return_packet_evidence_subjects(
    store: FilesystemObjectStore,
    packet_ref: str,
) -> ResolvedReturnPacketEvidenceSubjects:
    """Bind exact packet evidence only to exact created artifacts it explicitly names.

    The resolver begins from ``resolve_return_packet_output_identity(...)`` so exact packet,
    created-artifact, evidence-record, proof-to-use/materialization, and modified-artifact
    fail-closed invariants are inherited rather than reimplemented.

    Evidence subject handling is deliberately narrow:

    * every ``subject_ref`` is offered to the shared Stage 2 immutable-ref parser;
    * non-exact strings remain explicit unmatched evidence and gain no compatibility
      standing from type, logical id, array order, recency, actor intent, or storage order;
    * a syntactically exact subject ref must have kind ``artifact`` or resolution fails
      closed for this artifact-compatibility precondition;
    * an exact artifact subject binds only when its full canonical immutable ref exactly
      equals one of the packet's already-grounded ``artifacts_created`` refs;
    * ``artifact.evidence_refs`` is intentionally ignored because Decision 008 does not
      make that earlier artifact field authoritative for later evidence compatibility.

    The returned subject-binding projection is tuple-backed so the demonstrated
    ``object.__setattr__`` wrapper mutation path cannot reassign bindings or erase explicit
    unmatched evidence after grounding. The function remains read-only and intentionally
    stops before compatibility semantics.
    """

    output_identity = resolve_return_packet_output_identity(store, packet_ref)
    created_by_ref = {
        relation.reference: relation for relation in output_identity.created_artifacts
    }
    bound_by_ref: dict[str, list[ExactPacketRelation]] = {
        relation.reference: [] for relation in output_identity.created_artifacts
    }
    unmatched: list[UnmatchedEvidenceSubject] = []

    for evidence in output_identity.evidence_records:
        subject_ref = _subject_ref(evidence.value)
        try:
            parsed_subject = parse_immutable_ref(subject_ref)
        except IdentityError:
            unmatched.append(
                UnmatchedEvidenceSubject(
                    evidence=evidence,
                    subject_ref=subject_ref,
                    reason="non_exact_subject",
                )
            )
            continue

        if parsed_subject.kind != "artifact":
            raise EvidenceSubjectKindError(
                "evidence subject considered against packet-created artifacts must use "
                f"kind 'artifact', got {parsed_subject.kind!r} in {subject_ref!r}"
            )

        artifact = created_by_ref.get(subject_ref)
        if artifact is None:
            unmatched.append(
                UnmatchedEvidenceSubject(
                    evidence=evidence,
                    subject_ref=subject_ref,
                    reason="exact_artifact_not_created_by_packet",
                )
            )
            continue

        bound_by_ref[artifact.reference].append(evidence)

    bindings = tuple(
        ExactCreatedArtifactEvidenceBinding(
            artifact=artifact,
            evidence_records=tuple(bound_by_ref[artifact.reference]),
        )
        for artifact in output_identity.created_artifacts
    )

    return ResolvedReturnPacketEvidenceSubjects(
        output_identity=output_identity,
        created_artifact_bindings=bindings,
        unmatched_evidence=tuple(unmatched),
    )
