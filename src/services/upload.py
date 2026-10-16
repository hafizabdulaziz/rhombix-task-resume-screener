import os
from typing import Optional, Tuple
from fastapi import UploadFile
from src.core.exceptions import AppError
import structlog

logger = structlog.get_logger()

# Allowed MIME types and magic headers
ALLOWED_MIME_TYPES = {
    "application/pdf": b"%PDF-",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": b"PK\x03\x04"
}

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

class FileValidator:
    @staticmethod
    async def validate(file: UploadFile) -> Tuple[str, bytes]:
        """
        Validates uploaded file format, MIME type, magic headers, and file size.
        Returns tuple of (file_extension, file_bytes).
        """
        if not file.filename:
            raise AppError("No filename provided.", status_code=400)

        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in [".pdf", ".docx"]:
            raise AppError(f"Unsupported file extension '{ext}'. Only .pdf and .docx are allowed.", status_code=400)

        # Check content type if available
        content_type = file.content_type
        if content_type and content_type not in ALLOWED_MIME_TYPES:
            logger.warning("invalid_mime_type_header", filename=file.filename, content_type=content_type)

        # Read file content
        content = await file.read()
        file_size = len(content)

        if file_size == 0:
            raise AppError("Uploaded file is empty.", status_code=400)

        if file_size > MAX_FILE_SIZE_BYTES:
            raise AppError(f"File size exceeds maximum allowed limit of {MAX_FILE_SIZE_MB}MB.", status_code=400)

        # Verify magic headers (binary signature)
        if ext == ".pdf":
            if not content.startswith(b"%PDF-"):
                raise AppError("Invalid PDF file format: missing PDF signature header.", status_code=400)
            file_type = "pdf"
        elif ext == ".docx":
            # DOCX is a zipped archive starting with PK\x03\x04
            if not content.startswith(b"PK\x03\x04"):
                raise AppError("Invalid DOCX file format: missing ZIP/DOCX signature header.", status_code=400)
            file_type = "docx"
        else:
            raise AppError("Unsupported file type.", status_code=400)

        # Reset file pointer for subsequent reads if needed
        await file.seek(0)
        logger.info("file_validation_passed", filename=file.filename, file_type=file_type, size_bytes=file_size)
        return file_type, content
