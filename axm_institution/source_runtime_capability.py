from __future__ import annotations

import stat
from pathlib import Path
from typing import Any, Mapping

from . import identity as _identity
from .identity import (
    ContractValidationError,
    IdentityError,
    canonical_bytes,
    make_immutable_ref,
    parse_immutable_ref,
    parse_json_strict,
)


BUNDLED_SCHEMA_DIR = _identity.DEFAULT_SCHEMA_DIR.resolve()
_TYPED_CONTAINING_KINDS = {
    "artifact": ("artifact.schema.json", "0.4"),
    "evidence-record": ("evidence-record.schema.json", "0.2"),
}
_RUNTIME_CAPABILITIES = frozenset({"supported", "unsupported_kind"})


class SourceRuntimeCapabilityError(RuntimeError):
    """Base error for Decision 022 exact source runtime capability facts."""


class SourceRuntimeCapabilityInputError(SourceRuntimeCapabilityError):
    """The requested exact typed declaration occurrence is not grounded."""


class SourceRuntimeCapabilityContextError(SourceRuntimeCapabilityError):
    """The bundled kernel schema context cannot be interpreted safely."""


class ExactSourceRuntimeCapabilityFact(bytes):
    """Canonical-byte-backed named Decision 022 capability fact.

    The authoritative representation is immutable canonical JSON bytes. Ordinary stdlib
    JSON transport therefore fails closed for the object itself instead of silently
    turning named institutional meaning into positional data. ``_asdict()`` and
    ``bytes(fact)`` are explicit named materialization paths.
    """

    __slots__ = ()
    _fields = (
        "containing_object_ref",
        "declaration_key",
        "target_object_ref",
        "target_kind",
        "runtime_capability",
    )

    def __new__(
        cls,
        *,
        containing_object_ref: str,
        declaration_key: str,
        target_object_ref: str,
        target_kind: str,
        runtime_capability: str,
    ):
        if runtime_capability not in _RUNTIME_CAPABILITIES:
            raise ValueError(f"unsupported runtime capability: {runtime_capability!r}")
        return bytes.__new__(
            cls,
            canonical_bytes(
                {
                    "containing_object_ref": containing_object_ref,
                    "declaration_key": declaration_key,
                    "target_object_ref": target_object_ref,
                    "target_kind": target_kind,
                    "runtime_capability": runtime_capability,
                }
            ),
        )

    def _plain(self) -> dict[str, Any]:
        value = parse_json_strict(memoryview(self).tobytes().decode("utf-8"))
        if not isinstance(value, dict):
            raise TypeError("frozen Decision 022 capability fact did not decode as a mapping")
        return value

    def _asdict(self) -> dict[str, Any]:
        return {field: getattr(self, field) for field in self._fields}

    def __repr__(self) -> str:
        values = ", ".join(f"{field}={getattr(self, field)!r}" for field in self._fields)
        return f"{type(self).__name__}({values})"

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        return bytes.__eq__(self, other)

    __hash__ = bytes.__hash__

    @property
    def containing_object_ref(self) -> str:
        value = self._plain()["containing_object_ref"]
        if not isinstance(value, str):
            raise TypeError("Decision 022 containing_object_ref is not a string")
        return value

    @property
    def declaration_key(self) -> str:
        value = self._plain()["declaration_key"]
        if not isinstance(value, str):
            raise TypeError("Decision 022 declaration_key is not a string")
        return value

    @property
    def target_object_ref(self) -> str:
        value = self._plain()["target_object_ref"]
        if not isinstance(value, str):
            raise TypeError("Decision 022 target_object_ref is not a string")
        return value

    @property
    def target_kind(self) -> str:
        value = self._plain()["target_kind"]
        if not isinstance(value, str):
            raise TypeError("Decision 022 target_kind is not a string")
        return value

    @property
    def runtime_capability(self) -> str:
        value = self._plain()["runtime_capability"]
        if value not in _RUNTIME_CAPABILITIES:
            raise TypeError("Decision 022 runtime_capability is outside the bounded enum")
        return value


def _bundled_runtime_capability(target_kind: str) -> str:
    """Classify only the fixed package-bundled schema context.

    Absence of ``<kind>.schema.json`` means only that this bundled runtime does not have
    an interpretation contract. A path that exists but cannot be read/validated is a
    runtime configuration failure and must not be relabelled ``unsupported_kind``.
    """

    schema_name = f"{target_kind}.schema.json"
    schema_path = BUNDLED_SCHEMA_DIR / schema_name
    try:
        metadata = schema_path.stat()
    except FileNotFoundError:
        return "unsupported_kind"
    except OSError as exc:
        raise SourceRuntimeCapabilityContextError(
            f"cannot inspect bundled schema context for {target_kind!r}: {exc}"
        ) from exc

    if not stat.S_ISREG(metadata.st_mode):
        raise SourceRuntimeCapabilityContextError(
            f"bundled schema path for {target_kind!r} is not a regular file"
        )

    try:
        _identity.load_schema(schema_name, BUNDLED_SCHEMA_DIR)
    except (ContractValidationError, IdentityError, UnicodeError) as exc:
        raise SourceRuntimeCapabilityContextError(
            f"bundled schema context for {target_kind!r} is invalid: {exc}"
        ) from exc
    return "supported"


def _exact_declaration_occurrence(
    *,
    containing_object_ref: str,
    containing_value: Mapping[str, Any],
    declaration_key: str,
) -> tuple[str, str]:
    if not isinstance(containing_value, Mapping):
        raise SourceRuntimeCapabilityInputError("containing_value must be a mapping")
    if not isinstance(declaration_key, str) or not declaration_key:
        raise SourceRuntimeCapabilityInputError("declaration_key must be a non-empty string")

    try:
        parsed_container = parse_immutable_ref(containing_object_ref)
    except IdentityError as exc:
        raise SourceRuntimeCapabilityInputError(
            f"containing_object_ref is not canonical: {exc}"
        ) from exc

    contract = _TYPED_CONTAINING_KINDS.get(parsed_container.kind)
    if contract is None:
        raise SourceRuntimeCapabilityInputError(
            "Decision 022 supports only typed artifact v0.4 and evidence-record v0.2 containers"
        )
    schema_name, required_version = contract

    try:
        actual_ref = make_immutable_ref(schema_name, containing_value)
    except (ContractValidationError, IdentityError, ValueError) as exc:
        raise SourceRuntimeCapabilityInputError(
            f"containing value does not satisfy {schema_name}: {exc}"
        ) from exc

    if actual_ref != containing_object_ref:
        raise SourceRuntimeCapabilityInputError(
            "containing value does not reproduce the supplied exact immutable reference"
        )
    if containing_value.get("schema_version") != required_version:
        raise SourceRuntimeCapabilityInputError(
            f"Decision 022 requires {parsed_container.kind} schema_version {required_version}"
        )

    if parsed_container.kind == "artifact":
        provenance = containing_value.get("provenance")
        if not isinstance(provenance, Mapping):
            raise SourceRuntimeCapabilityInputError("typed artifact provenance is unavailable")
        declarations = provenance.get("source_declarations")
    else:
        declarations = containing_value.get("source_declarations")

    if not isinstance(declarations, Mapping):
        raise SourceRuntimeCapabilityInputError("typed source declarations are unavailable")
    if declaration_key not in declarations:
        raise SourceRuntimeCapabilityInputError(
            f"declaration key is absent from the exact containing object: {declaration_key!r}"
        )

    declaration = declarations[declaration_key]
    if not isinstance(declaration, Mapping):
        raise SourceRuntimeCapabilityInputError("selected declaration is not a mapping")
    if declaration.get("source_class") != "exact_axm_object":
        raise SourceRuntimeCapabilityInputError(
            "selected declaration is not an exact_axm_object occurrence"
        )

    target_ref = declaration.get("object_ref")
    try:
        parsed_target = parse_immutable_ref(target_ref)
    except (IdentityError, TypeError) as exc:
        raise SourceRuntimeCapabilityInputError(
            f"selected exact_axm_object target is not canonical: {exc}"
        ) from exc
    return target_ref, parsed_target.kind


def project_exact_source_runtime_capability(
    *,
    containing_object_ref: str,
    containing_value: Mapping[str, Any],
    declaration_key: str,
) -> ExactSourceRuntimeCapabilityFact:
    """Project Decision 022 bundled-runtime capability for one exact declaration occurrence.

    The function consumes only the exact containing value, one exact declaration key, and
    the fixed bundled schema set. It performs no source-target object-store lookup and
    grants no existence, retrieval, integrity, provenance, trust, closure, acceptance,
    integration, epoch, or replay authority.
    """

    target_ref, target_kind = _exact_declaration_occurrence(
        containing_object_ref=containing_object_ref,
        containing_value=containing_value,
        declaration_key=declaration_key,
    )
    runtime_capability = _bundled_runtime_capability(target_kind)
    return ExactSourceRuntimeCapabilityFact(
        containing_object_ref=containing_object_ref,
        declaration_key=declaration_key,
        target_object_ref=target_ref,
        target_kind=target_kind,
        runtime_capability=runtime_capability,
    )
