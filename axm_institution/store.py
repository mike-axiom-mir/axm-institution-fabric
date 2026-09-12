from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .identity import (
    ContractValidationError,
    ImmutableReferenceError,
    canonical_validated_bytes,
    make_immutable_ref,
    parse_immutable_ref,
    parse_json_strict,
    validate_instance,
)


class ObjectStoreError(RuntimeError):
    """Base error for immutable object-store failures."""


class ObjectNotFoundError(ObjectStoreError):
    """The requested exact immutable object is not present."""


class ObjectCorruptionError(ObjectStoreError):
    """Stored bytes do not reproduce the exact immutable object requested."""


class ObjectReferenceMismatchError(ObjectStoreError):
    """A caller-supplied immutable reference does not match the object being stored."""


@dataclass(frozen=True)
class StoreWriteResult:
    reference: str
    created: bool
    referenced_members_verified: bool | None


class FilesystemObjectStore:
    """Small local/offline immutable store for validated canonical kernel objects.

    Objects are addressed only by their Stage 2 ``axmref:v1`` immutable identity.
    Files are published atomically from a temporary file in the destination directory,
    so an interrupted pre-publication write is not visible through exact lookup.

    Persisting a ``state-revision`` object does not prove that its member references
    exist. ``referenced_members_verified`` is therefore ``False`` for state-revision
    writes in this first Stage 3 slice. No mutable current/HEAD pointer is implemented.
    """

    def __init__(self, root: Path | str, schema_dir: Path | None = None) -> None:
        self.root = Path(root)
        self.objects_dir = self.root / "objects"
        self.schema_dir = schema_dir

    @staticmethod
    def _schema_for_kind(kind: str) -> str:
        return f"{kind}.schema.json"

    def _object_path(self, reference: str) -> Path:
        parsed = parse_immutable_ref(reference)
        return self.objects_dir / parsed.kind / parsed.sha256[:2] / f"{parsed.sha256}.json"

    def _verify_existing(self, reference: str, schema_name: str) -> Mapping[str, Any]:
        path = self._object_path(reference)
        try:
            raw = path.read_bytes()
        except FileNotFoundError as exc:
            raise ObjectNotFoundError(f"immutable object not found: {reference}") from exc
        except OSError as exc:
            raise ObjectStoreError(f"cannot read immutable object {reference}: {exc}") from exc

        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ObjectCorruptionError(
                f"stored object is not valid UTF-8 for {reference}"
            ) from exc

        try:
            value = parse_json_strict(text)
            validated = validate_instance(value, schema_name, self.schema_dir)
            canonical = canonical_validated_bytes(validated, schema_name, self.schema_dir)
            actual_reference = make_immutable_ref(schema_name, validated, self.schema_dir)
        except (ContractValidationError, ImmutableReferenceError, ValueError) as exc:
            raise ObjectCorruptionError(
                f"stored object cannot reproduce validated identity for {reference}: {exc}"
            ) from exc

        if raw != canonical:
            raise ObjectCorruptionError(
                f"stored bytes are not the canonical bytes for {reference}"
            )
        if actual_reference != reference:
            raise ObjectCorruptionError(
                f"stored object reproduces {actual_reference}, not requested {reference}"
            )
        return validated

    def store(
        self,
        value: Mapping[str, Any],
        schema_name: str,
        *,
        expected_reference: str | None = None,
    ) -> StoreWriteResult:
        """Validate, canonicalize, and immutably persist one object.

        Re-storing byte-identical content is idempotent. If a final object path already
        exists, it is verified rather than overwritten. ``expected_reference`` can be
        supplied when the caller already claims an exact identity; disagreement fails
        before publication.
        """

        canonical = canonical_validated_bytes(value, schema_name, self.schema_dir)
        reference = make_immutable_ref(schema_name, value, self.schema_dir)
        parsed = parse_immutable_ref(reference)

        if expected_reference is not None:
            try:
                parse_immutable_ref(expected_reference)
            except ImmutableReferenceError as exc:
                raise ObjectReferenceMismatchError(
                    f"expected reference is invalid: {expected_reference!r}"
                ) from exc
            if expected_reference != reference:
                raise ObjectReferenceMismatchError(
                    f"object identity {reference} does not match expected {expected_reference}"
                )

        target = self._object_path(reference)
        if target.exists():
            self._verify_existing(reference, schema_name)
            return StoreWriteResult(
                reference=reference,
                created=False,
                referenced_members_verified=False if parsed.kind == "state-revision" else None,
            )

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise ObjectStoreError(f"cannot create object-store directory: {exc}") from exc

        temp_path: Path | None = None
        try:
            fd, temp_name = tempfile.mkstemp(prefix=".axm-tmp-", dir=target.parent)
            temp_path = Path(temp_name)
            with os.fdopen(fd, "wb") as handle:
                handle.write(canonical)
                handle.flush()
                os.fsync(handle.fileno())

            try:
                # Hard-link publication is atomic and never overwrites an existing
                # immutable object. The temp file lives in the same directory/filesystem.
                os.link(temp_path, target)
                created = True
            except FileExistsError:
                created = False
                self._verify_existing(reference, schema_name)
            except OSError as exc:
                raise ObjectStoreError(f"cannot publish immutable object {reference}: {exc}") from exc

            if created:
                # Verify the just-published bytes through the same exact lookup path.
                self._verify_existing(reference, schema_name)
                if hasattr(os, "O_DIRECTORY"):
                    try:
                        dir_fd = os.open(target.parent, os.O_RDONLY | os.O_DIRECTORY)
                    except OSError:
                        dir_fd = None
                    if dir_fd is not None:
                        try:
                            os.fsync(dir_fd)
                        finally:
                            os.close(dir_fd)

            return StoreWriteResult(
                reference=reference,
                created=created,
                referenced_members_verified=False if parsed.kind == "state-revision" else None,
            )
        finally:
            if temp_path is not None:
                try:
                    temp_path.unlink(missing_ok=True)
                except OSError:
                    pass

    def load_bytes(self, reference: str, schema_name: str | None = None) -> bytes:
        """Return canonical bytes only after exact identity verification."""

        parsed = parse_immutable_ref(reference)
        chosen_schema = schema_name or self._schema_for_kind(parsed.kind)
        if chosen_schema != self._schema_for_kind(parsed.kind):
            raise ObjectReferenceMismatchError(
                f"reference kind {parsed.kind!r} does not match schema {chosen_schema!r}"
            )
        self._verify_existing(reference, chosen_schema)
        try:
            return self._object_path(reference).read_bytes()
        except OSError as exc:
            raise ObjectStoreError(f"cannot reread immutable object {reference}: {exc}") from exc

    def load(self, reference: str, schema_name: str | None = None) -> Mapping[str, Any]:
        """Return the validated object only when it reproduces the exact requested ref."""

        parsed = parse_immutable_ref(reference)
        chosen_schema = schema_name or self._schema_for_kind(parsed.kind)
        if chosen_schema != self._schema_for_kind(parsed.kind):
            raise ObjectReferenceMismatchError(
                f"reference kind {parsed.kind!r} does not match schema {chosen_schema!r}"
            )
        return self._verify_existing(reference, chosen_schema)
