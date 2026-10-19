from io import BytesIO

import pytest
from fastapi import UploadFile

from src.core.exceptions import AppError
from src.services.storage import StorageManager
from src.services.upload import FileValidator


@pytest.mark.asyncio
async def test_file_validator_invalid_extension():
    f = UploadFile(file=BytesIO(b"some content"), filename="test.txt")
    with pytest.raises(AppError) as exc_info:
        await FileValidator.validate(f)
    assert "Unsupported file extension" in str(exc_info.value)

@pytest.mark.asyncio
async def test_file_validator_empty_file():
    f = UploadFile(file=BytesIO(b""), filename="resume.pdf")
    with pytest.raises(AppError) as exc_info:
        await FileValidator.validate(f)
    assert "Uploaded file is empty" in str(exc_info.value)

@pytest.mark.asyncio
async def test_file_validator_invalid_pdf_signature():
    f = UploadFile(file=BytesIO(b"NOTAPDFCONTENT"), filename="resume.pdf")
    with pytest.raises(AppError) as exc_info:
        await FileValidator.validate(f)
    assert "Invalid PDF file format" in str(exc_info.value)

@pytest.mark.asyncio
async def test_file_validator_valid_pdf():
    valid_pdf_bytes = b"%PDF-1.4 sample pdf content"
    f = UploadFile(file=BytesIO(valid_pdf_bytes), filename="resume.pdf")
    file_type, content = await FileValidator.validate(f)
    assert file_type == "pdf"
    assert content == valid_pdf_bytes

@pytest.mark.asyncio
async def test_storage_manager():
    sample_bytes = b"test resume bytes"
    filename = "test_resume.pdf"
    path = await StorageManager.save_file(sample_bytes, filename)
    assert path is not None
    assert "storage" in path and "resumes" in path
