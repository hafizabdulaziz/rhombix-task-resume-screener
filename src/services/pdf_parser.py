import io
import pdfplumber
from pypdf import PdfReader
from src.core.exceptions import AppError
import structlog

logger = structlog.get_logger()

class PDFParser:
    @staticmethod
    async def extract_pdf(file_bytes: bytes) -> dict:
        """
        Extracts text and metadata from PDF bytes using pdfplumber and pypdf fallback.
        """
        text_content = ""
        metadata = {}
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                metadata = pdf.metadata or {}
                pages_text = [page.extract_text() or "" for page in pdf.pages]
                text_content = "\n".join(pages_text)

            if not text_content.strip():
                reader = PdfReader(io.BytesIO(file_bytes))
                metadata = reader.metadata or metadata
                pages_text = [page.extract_text() or "" for page in reader.pages]
                text_content = "\n".join(pages_text)

            logger.info("pdf_parsed_successfully", total_chars=len(text_content))
            return {
                "text": text_content.strip(),
                "metadata": {k: str(v) for k, v in metadata.items() if v}
            }
        except Exception as e:
            logger.error("pdf_parsing_failed", error=str(e))
            raise AppError(f"Failed to parse PDF document: {str(e)}", status_code=400)
