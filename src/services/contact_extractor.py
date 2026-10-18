import re
import structlog
from typing import Dict, List, Optional

logger = structlog.get_logger()

class ContactExtractor:
    """
    Regex and NLP-based candidate contact metadata extractor.
    Extracts emails, phone numbers, LinkedIn URLs, and GitHub URLs from resume text.
    """
    
    EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    PHONE_REGEX = r'(?:\+\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}\b|\b\d{10,12}\b'
    LINKEDIN_REGEX = r'(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9_-]+'
    GITHUB_REGEX = r'(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]+'

    @classmethod
    def extract_contacts(cls, text: str) -> Dict[str, Optional[str] | List[str]]:
        if not text:
            return {
                "emails": [],
                "phones": [],
                "linkedin": None,
                "github": None
            }
        
        emails = list(set(re.findall(cls.EMAIL_REGEX, text)))
        phones = list(set(re.findall(cls.PHONE_REGEX, text)))
        
        linkedin_match = re.search(cls.LINKEDIN_REGEX, text, re.IGNORECASE)
        linkedin = linkedin_match.group(0) if linkedin_match else None
        
        github_match = re.search(cls.GITHUB_REGEX, text, re.IGNORECASE)
        github = github_match.group(0) if github_match else None
        
        logger.info("contacts_extracted", emails_count=len(emails), phones_count=len(phones), has_linkedin=bool(linkedin), has_github=bool(github))
        return {
            "emails": emails,
            "phones": phones,
            "linkedin": linkedin,
            "github": github
        }
