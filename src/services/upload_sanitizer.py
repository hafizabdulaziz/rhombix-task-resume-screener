import re

import structlog

from src.core.exceptions import AppError

logger = structlog.get_logger()

class UploadSanitizer:
    SQLI_PATTERN = re.compile(r"('|--|union\s+select|drop\s+table|exec\s*\(|insert\s+into)", re.IGNORECASE)
    SUSPICIOUS_MACRO_PATTERN = re.compile(r"(eval\s*\(|script\s*>\s*alert|vbscript:|javascript:)", re.IGNORECASE)

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename against directory traversal and SQL injection payloads.
        """
        if not filename:
            return "unnamed_file"
        
        if UploadSanitizer.SQLI_PATTERN.search(filename):
            logger.warning("sql_injection_filename_detected", filename=filename)
            raise AppError("Malformed or malicious filename payload detected.", status_code=400)
        
        clean_name = filename.split("/")[-1].split("\\")[-1]
        clean_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', clean_name)
        return clean_name

    @staticmethod
    def inspect_content(text: str):
        """
        Inspect extracted text for malicious script injection or macro payloads.
        """
        if UploadSanitizer.SUSPICIOUS_MACRO_PATTERN.search(text):
            logger.warning("malicious_script_or_macro_detected")
            raise AppError("Document contains suspicious script or macro payload.", status_code=400)
