import hashlib
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

from app.core.errors import UploadError
from app.core.settings import Settings


@dataclass(frozen=True, slots=True)
class StoredVideo:
    original_name: str
    stored_name: str
    content_type: str | None
    size_bytes: int
    sha256: str


class LocalVideoStorage:
    """Stores uploads under generated names and never trusts client paths."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._root = settings.upload_dir.resolve()

    async def save(self, upload: UploadFile) -> StoredVideo:
        original_name = Path(upload.filename or "video").name
        extension = Path(original_name).suffix.lower()
        if extension not in self._settings.allowed_video_extensions:
            allowed = ", ".join(sorted(self._settings.allowed_video_extensions))
            raise UploadError(
                "unsupported_video_extension",
                f"Unsupported video extension. Allowed extensions: {allowed}.",
            )
        if (
            upload.content_type
            and upload.content_type not in self._settings.allowed_video_content_types
        ):
            raise UploadError(
                "unsupported_content_type",
                f"Unsupported content type: {upload.content_type}.",
            )

        stored_name = f"{uuid4()}{extension}"
        final_path = self.resolve(stored_name)
        temporary_path = final_path.with_suffix(f"{final_path.suffix}.part")
        digest = hashlib.sha256()
        size = 0

        try:
            async with aiofiles.open(temporary_path, "wb") as destination:
                while chunk := await upload.read(self._settings.upload_chunk_bytes):
                    size += len(chunk)
                    if size > self._settings.max_upload_bytes:
                        raise UploadError(
                            "upload_too_large",
                            "The uploaded video exceeds the configured size limit.",
                        )
                    digest.update(chunk)
                    await destination.write(chunk)
            if size == 0:
                raise UploadError("empty_upload", "The uploaded video is empty.")
            temporary_path.replace(final_path)
        except Exception:
            temporary_path.unlink(missing_ok=True)
            raise
        finally:
            await upload.close()

        return StoredVideo(
            original_name=original_name,
            stored_name=stored_name,
            content_type=upload.content_type,
            size_bytes=size,
            sha256=digest.hexdigest(),
        )

    def resolve(self, stored_name: str) -> Path:
        path = (self._root / stored_name).resolve()
        if path.parent != self._root:
            raise UploadError("invalid_storage_path", "Invalid video storage path.")
        return path

    def delete(self, stored_name: str) -> None:
        self.resolve(stored_name).unlink(missing_ok=True)
