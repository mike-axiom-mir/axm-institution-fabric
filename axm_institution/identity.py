from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from jsonschema import Draft202012Validator, FormatChecker

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA_DIR = PACKAGE_ROOT / "schemas"

STRONG_EVIDENCE_STATES = frozenset(
    {
        "compiled",
        "automated_tested",
        "runtime_tested",
        "visually_inspected",
        "playtested",
        "measured",
    }
)

_KIND_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
_HEX = "0123456789ABCDEF"
_UNRESERVED = frozenset(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")
_MAX_SAFE_INTEGER = 9_007_199_254_740_991
_SHORT_JSON_ESCAPES = {
    "\b": "\\b",
    "\t": "\\t",
    "\n": "\\n",
    "\f": "\\f",
    "\r": "\\r",
}
_STATE_REVISION_MEMBER_KINDS: tuple[tuple[str, str, bool], ...] = (
    ("parent_revision_ref", "state-revision", False),
    ("objective_ref", "objective", False),
    ("lane_refs", "lane", True),
    ("occupancy_refs", "occupancy", True),
    ("claim_refs", "work-claim", True),
    ("artifact_refs", "artifact", True),
    ("evidence_refs", "evidence-record", True),
    ("return_packet_refs", "return-packet", True),
    ("integration_receipt_refs", "integration-receipt", True),
)
_EXACT_REFERENCE_FIELDS: dict[str, tuple[tuple[str, str], ...]] = {
    "work-claim.schema.json": (("occupancy_ref", "occupancy"),),
    "return-packet.schema.json": (("claim_ref", "work-claim"),),
}


class IdentityError(ValueError):
    """Base error for deterministic identity failures."""


class CanonicalizationError(IdentityError):
    """Input cannot be represented unambiguously by the v0 canonical form."""


class ContractValidationError(IdentityError):
    """An object does not satisfy its kernel contract."""


class ImmutableReferenceError(IdentityError):
    """An immutable reference is malformed, ambiguous, or does not resolve exactly."""


class EvidenceBindingError(IdentityError):
    """Evidence does not bind the exact immutable subject instance it claims to support."""


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CanonicalizationError(f"duplicate object key: {key!r}")
        result[key] = value
    return result


def _parse_int(token: str) -> int:
    value = int(token)
    if str(value) != token:
        raise CanonicalizationError(f"non-canonical integer spelling is not supported: {token!r}")
    if abs(value) > _MAX_SAFE_INTEGER:
        raise CanonicalizationError(
            f"integer {token!r} is outside the v0 cross-runtime safe range"
        )
    return value


def _reject_float(token: str) -> Any:
    raise CanonicalizationError(
        f"floating-point JSON number {token!r} is outside the v0 canonical subset"
    )


def _reject_constant(token: str) -> Any:
    raise CanonicalizationError(f"non-standard JSON constant is not supported: {token}")


def _assert_canonical_subset(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, bool):
        return
    if isinstance(value, int):
        if abs(value) > _MAX_SAFE_INTEGER:
            raise CanonicalizationError(
                f"integer value at {path} is outside the v0 cross-runtime safe range"
            )
        return
    if isinstance(value, float):
        raise CanonicalizationError(f"floating-point value at {path} is not supported")
    if isinstance(value, str):
        if any(0xD800 <= ord(ch) <= 0xDFFF for ch in value):
            raise CanonicalizationError(f"surrogate code point at {path} is not supported")
        if unicodedata.normalize("NFC", value) != value:
            raise CanonicalizationError(
                f"non-NFC text at {path} is ambiguous; provide NFC-normalized input"
            )
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _assert_canonical_subset(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError(f"non-string object key at {path}: {key!r}")
            _assert_canonical_subset(key, f"{path}.<key>")
            _assert_canonical_subset(item, f"{path}.{key}")
        return
    raise CanonicalizationError(
        f"unsupported value type at {path}: {type(value).__name__}"
    )


def parse_json_strict(text: str) -> Any:
    """Parse JSON without silently normalizing ambiguous input.

    V0 intentionally supports integer JSON numbers only. Duplicate keys, NaN/Infinity,
    floating-point spellings, non-NFC text, and surrogate code points fail loudly.
    """

    try:
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_pairs,
            parse_int=_parse_int,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except CanonicalizationError:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise CanonicalizationError(str(exc)) from exc
    _assert_canonical_subset(value)
    return value


def _scalar_key(value: str) -> tuple[int, ...]:
    """Unicode-scalar-value lexicographic key required by Decision 003."""

    return tuple(ord(ch) for ch in value)


def _render_json_string(value: str) -> str:
    """Render a string with the explicit Decision 004 canonical JSON spelling."""

    rendered = ['"']
    for char in value:
        codepoint = ord(char)
        if char == '"':
            rendered.append('\\"')
        elif char == "\\":
            rendered.append("\\\\")
        elif char in _SHORT_JSON_ESCAPES:
            rendered.append(_SHORT_JSON_ESCAPES[char])
        elif codepoint <= 0x1F:
            rendered.append(f"\\u{codepoint:04x}")
        else:
            rendered.append(char)
    rendered.append('"')
    return "".join(rendered)


def _render_canonical(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, str):
        return _render_json_string(value)
    if isinstance(value, list):
        return "[" + ",".join(_render_canonical(item) for item in value) + "]"
    if isinstance(value, dict):
        members = []
        for key in sorted(value.keys(), key=_scalar_key):
            members.append(
                _render_json_string(key)
                + ":"
                + _render_canonical(value[key])
            )
        return "{" + ",".join(members) + "}"
    raise CanonicalizationError(f"unsupported value type: {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    """Return the single v0 canonical UTF-8 JSON representation for a supported value."""

    _assert_canonical_subset(value)
    try:
        return _render_canonical(value).encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as exc:
        raise CanonicalizationError(str(exc)) from exc


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _schema_path(schema_name: str, schema_dir: Path | None = None) -> Path:
    if not schema_name.endswith(".schema.json") or "/" in schema_name or "\\" in schema_name:
        raise ContractValidationError(f"invalid schema name: {schema_name!r}")
    return (schema_dir or DEFAULT_SCHEMA_DIR) / schema_name


def load_schema(schema_name: str, schema_dir: Path | None = None) -> Mapping[str, Any]:
    path = _schema_path(schema_name, schema_dir)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ContractValidationError(f"cannot read schema {schema_name}: {exc}") from exc
    schema = parse_json_strict(text)
    if not isinstance(schema, dict):
        raise ContractValidationError(f"schema {schema_name} is not a JSON object")
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        raise ContractValidationError(f"invalid schema {schema_name}: {exc}") from exc
    return schema


def validate_instance(
    value: Any, schema_name: str, schema_dir: Path | None = None
) -> Mapping[str, Any]:
    _assert_canonical_subset(value)
    if not isinstance(value, dict):
        raise ContractValidationError("kernel contract instance must be a JSON object")
    schema = load_schema(schema_name, schema_dir)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(value), key=lambda err: list(err.absolute_path))
    if errors:
        err = errors[0]
        location = "$" + "".join(
            f"[{segment}]" if isinstance(segment, int) else f".{segment}"
            for segment in err.absolute_path
        )
        raise ContractValidationError(
            f"{schema_name} validation failed at {location}: {err.message}"
        )
    if schema_name == "state-revision.schema.json":
        _validate_state_revision_member_refs(value)
    exact_fields = _EXACT_REFERENCE_FIELDS.get(schema_name)
    if exact_fields:
        _validate_exact_reference_fields(value, schema_name, exact_fields)
    return value


def load_and_validate(
    path: Path | str, schema_name: str, schema_dir: Path | None = None
) -> Mapping[str, Any]:
    file_path = Path(path)
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ContractValidationError(f"cannot read {file_path}: {exc}") from exc
    value = parse_json_strict(text)
    return validate_instance(value, schema_name, schema_dir)


def canonical_validated_bytes(
    value: Any, schema_name: str, schema_dir: Path | None = None
) -> bytes:
    validated = validate_instance(value, schema_name, schema_dir)
    return canonical_bytes(validated)


def canonical_validated_sha256(
    value: Any, schema_name: str, schema_dir: Path | None = None
) -> str:
    return hashlib.sha256(canonical_validated_bytes(value, schema_name, schema_dir)).hexdigest()


def _kind_for_schema(schema_name: str) -> str:
    suffix = ".schema.json"
    if not schema_name.endswith(suffix):
        raise ImmutableReferenceError(f"invalid schema name: {schema_name!r}")
    kind = schema_name[: -len(suffix)]
    if not _KIND_RE.fullmatch(kind):
        raise ImmutableReferenceError(f"schema kind is not reference-safe: {kind!r}")
    return kind


def _encode_component(value: str) -> str:
    """Decision 003: UTF-8 bytes with RFC3986 unreserved ASCII left raw."""

    _assert_canonical_subset(value, "reference.component")
    encoded: list[str] = []
    for byte in value.encode("utf-8"):
        if byte in _UNRESERVED:
            encoded.append(chr(byte))
        else:
            encoded.append("%" + _HEX[byte >> 4] + _HEX[byte & 0x0F])
    return "".join(encoded)


def _decode_component(encoded: str, label: str) -> str:
    raw = bytearray()
    index = 0
    while index < len(encoded):
        ch = encoded[index]
        code = ord(ch)
        if code < 128 and code in _UNRESERVED:
            raw.append(code)
            index += 1
            continue
        if ch != "%" or index + 2 >= len(encoded):
            raise ImmutableReferenceError(f"non-canonical {label} encoding")
        high, low = encoded[index + 1], encoded[index + 2]
        if high not in _HEX or low not in _HEX:
            raise ImmutableReferenceError(f"non-canonical {label} encoding")
        raw.append(int(high + low, 16))
        index += 3
    try:
        decoded = bytes(raw).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ImmutableReferenceError(f"invalid UTF-8 in {label} encoding") from exc
    _assert_canonical_subset(decoded, f"reference.{label}")
    if _encode_component(decoded) != encoded:
        raise ImmutableReferenceError(f"non-canonical {label} encoding")
    if not decoded:
        raise ImmutableReferenceError(f"empty {label} is not allowed")
    return decoded


@dataclass(frozen=True)
class ImmutableRef:
    kind: str
    logical_id: str
    version: str | None
    sha256: str

    def __str__(self) -> str:
        version = "-" if self.version is None else "v=" + _encode_component(self.version)
        return (
            f"axmref:v1:{self.kind}:{_encode_component(self.logical_id)}:"
            f"{version}:sha256:{self.sha256}"
        )


def parse_immutable_ref(reference: str) -> ImmutableRef:
    parts = reference.split(":")
    if len(parts) != 7 or parts[0:2] != ["axmref", "v1"] or parts[5] != "sha256":
        raise ImmutableReferenceError("malformed immutable reference")
    kind, encoded_id, encoded_version, digest = parts[2], parts[3], parts[4], parts[6]
    if not _KIND_RE.fullmatch(kind):
        raise ImmutableReferenceError(f"invalid reference kind: {kind!r}")
    logical_id = _decode_component(encoded_id, "logical id")
    if encoded_version == "-":
        version = None
    else:
        if not encoded_version.startswith("v="):
            raise ImmutableReferenceError("present version token must start with 'v='")
        version = _decode_component(encoded_version[2:], "version")
    if not _DIGEST_RE.fullmatch(digest):
        raise ImmutableReferenceError("invalid sha256 digest")
    parsed = ImmutableRef(kind=kind, logical_id=logical_id, version=version, sha256=digest)
    if str(parsed) != reference:
        raise ImmutableReferenceError("reference is not in canonical form")
    return parsed


def _validate_state_revision_member_refs(value: Mapping[str, Any]) -> None:
    """Require state-revision members to use the exact Stage 2 reference language.

    JSON Schema remains the structural/spelling filter. This semantic pass reuses the
    canonical Stage 2 parser for UTF-8, NFC, percent-encoding, digest, and round-trip
    checks, then enforces the kind required by each membership field. It intentionally
    does not check whether referenced objects exist in the store.
    """

    for field, expected_kind, is_array in _STATE_REVISION_MEMBER_KINDS:
        raw = value.get(field)
        if raw is None:
            continue
        references = raw if is_array else [raw]
        for index, reference in enumerate(references):
            location = f"$.{field}[{index}]" if is_array else f"$.{field}"
            try:
                parsed = parse_immutable_ref(reference)
            except IdentityError as exc:
                raise ContractValidationError(
                    "state-revision.schema.json semantic reference validation failed "
                    f"at {location}: {exc}"
                ) from exc
            if parsed.kind != expected_kind:
                raise ContractValidationError(
                    "state-revision.schema.json semantic reference validation failed "
                    f"at {location}: expected kind {expected_kind!r}, got {parsed.kind!r}"
                )


def _validate_exact_reference_fields(
    value: Mapping[str, Any],
    schema_name: str,
    fields: tuple[tuple[str, str], ...],
) -> None:
    """Validate authoritative exact-reference fields through the Stage 2 parser."""

    for field, expected_kind in fields:
        reference = value.get(field)
        if reference is None:
            continue
        try:
            parsed = parse_immutable_ref(reference)
        except IdentityError as exc:
            raise ContractValidationError(
                f"{schema_name} semantic reference validation failed at $.{field}: {exc}"
            ) from exc
        if parsed.kind != expected_kind:
            raise ContractValidationError(
                f"{schema_name} semantic reference validation failed at $.{field}: "
                f"expected kind {expected_kind!r}, got {parsed.kind!r}"
            )


def make_immutable_ref(
    schema_name: str, value: Mapping[str, Any], schema_dir: Path | None = None
) -> str:
    validated = validate_instance(value, schema_name, schema_dir)
    logical_id = validated.get("id")
    if not isinstance(logical_id, str) or not logical_id:
        raise ImmutableReferenceError(f"{schema_name} has no usable logical id")
    version = validated.get("version")
    if version is not None and (not isinstance(version, str) or not version):
        raise ImmutableReferenceError(f"{schema_name} has invalid version")
    return str(
        ImmutableRef(
            kind=_kind_for_schema(schema_name),
            logical_id=logical_id,
            version=version,
            sha256=canonical_validated_sha256(validated, schema_name, schema_dir),
        )
    )


def reference_matches(
    reference: str,
    schema_name: str,
    value: Mapping[str, Any],
    schema_dir: Path | None = None,
) -> bool:
    parsed = parse_immutable_ref(reference)
    if parsed.kind != _kind_for_schema(schema_name):
        return False
    return reference == make_immutable_ref(schema_name, value, schema_dir)


def resolve_reference(
    reference: str,
    schema_name: str,
    candidates: Iterable[Mapping[str, Any]],
    schema_dir: Path | None = None,
) -> Mapping[str, Any]:
    parsed = parse_immutable_ref(reference)
    expected_kind = _kind_for_schema(schema_name)
    if parsed.kind != expected_kind:
        raise ImmutableReferenceError(
            f"reference kind {parsed.kind!r} does not match {expected_kind!r}"
        )
    matches = [
        candidate
        for candidate in candidates
        if reference_matches(reference, schema_name, candidate, schema_dir)
    ]
    if len(matches) != 1:
        raise ImmutableReferenceError(
            f"reference resolved to {len(matches)} candidate instances; expected exactly one"
        )
    return matches[0]


def validate_evidence_subject_binding(
    evidence: Mapping[str, Any],
    subject_schema_name: str,
    subject: Mapping[str, Any],
    schema_dir: Path | None = None,
) -> None:
    """Require exact immutable binding for strong evidence about a kernel object.

    This is an identity-layer check only. It does not claim repository existence,
    supersession acyclicity, stale-base validation, or state-store enforcement.
    """

    validate_instance(evidence, "evidence-record.schema.json", schema_dir)
    expected = make_immutable_ref(subject_schema_name, subject, schema_dir)
    state = evidence.get("state")
    subject_ref = evidence.get("subject_ref")
    if state in STRONG_EVIDENCE_STATES:
        if subject_ref != expected:
            raise EvidenceBindingError(
                "strong evidence must bind the exact immutable subject instance; "
                f"expected {expected!r}, got {subject_ref!r}"
            )
    elif isinstance(subject_ref, str) and subject_ref.startswith("axmref:") and subject_ref != expected:
        raise EvidenceBindingError(
            "immutable evidence subject reference does not match the supplied subject instance"
        )
