import pytest

from src.core.exceptions import AppError
from src.services.upload_sanitizer import UploadSanitizer


def test_sanitize_filename_valid():
    filename = "John_Doe_Resume (1).pdf"
    clean = UploadSanitizer.sanitize_filename(filename)
    assert clean == "John_Doe_Resume__1_.pdf"

def test_sanitize_filename_sqli():
    with pytest.raises(AppError):
        UploadSanitizer.sanitize_filename("resume.pdf'; DROP TABLE candidates; --")

def test_inspect_content_clean():
    UploadSanitizer.inspect_content("Experienced Python developer with FastAPI skills.")

def test_inspect_content_malicious():
    with pytest.raises(AppError):
        UploadSanitizer.inspect_content("Developer <script>alert('hack')</script>")
