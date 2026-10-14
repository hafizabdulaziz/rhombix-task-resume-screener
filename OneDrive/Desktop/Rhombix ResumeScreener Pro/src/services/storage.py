import os
import uuid
import asyncio
from src.core.exceptions import AppError
import structlog

logger = structlog.get_logger()

UPLOAD_DIR = os.path.join(os.getcwd(), "storage", "resumes")

class StorageManager:
    @staticmethod
    async def ensure_upload_dir():
        def _create_dir():
            os.makedirs(UPLOAD_DIR, exist_ok=True)
        await asyncio.to_thread(_create_dir)

    @classmethod
    async def save_file(cls, file_bytes: bytes, original_filename: str) -> str:
        """
        Saves uploaded file bytes to local storage with a unique filename.
        Returns the absolute or relative file path.
        """
        await cls.ensure_upload_dir()
        ext = os.path.splitext(original_filename)[1].lower()
        unique_filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        def _write():
            with open(file_path, "wb") as f:
                f.write(file_bytes)

        try:
            await asyncio.to_thread(_write)
            logger.info("file_saved_to_storage", original_filename=original_filename, stored_path=file_path)
            return file_path
        except Exception as e:
            logger.error("file_storage_failed", filename=original_filename, error=str(e))
            raise AppError(f"Failed to persist file to storage: {str(e)}", status_code=500)
