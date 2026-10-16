import pytest
from fastapi import UploadFile
from io import BytesIO
from src.services.upload import FileValidator
from src.services.storage import StorageManager
from src.services.pdf_parser import PDFParser
from src.services.docx_parser import DocxParser
from src.core.exceptions import AppError

@pytest.mark.asyncio
async def test_file_validator_and_parsers():
    # Test valid PDF header
    valid_pdf_bytes = b"%PDF-1.4 John Doe Resume Software Engineer Python FastAPI"
    f = UploadFile(file=BytesIO(valid_pdf_bytes), filename="resume.pdf")
    file_type, content = await FileValidator.validate(f)
    assert file_type == "pdf"
    assert content == valid_pdf_bytes

    # Test valid DOCX header
    valid_docx_bytes = b"PK\x03\x04 fake docx content"
    f_docx = UploadFile(file=BytesIO(valid_docx_bytes), filename="resume.docx")
    file_type_docx, content_docx = await FileValidator.validate(f_docx)
    assert file_type_docx == "docx"
    assert content_docx == valid_docx_bytes
