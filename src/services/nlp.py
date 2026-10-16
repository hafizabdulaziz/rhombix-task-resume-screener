import re
import structlog

logger = structlog.get_logger()

COMMON_STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with",
    "by", "of", "as", "is", "are", "was", "were", "be", "been", "being", "have",
    "has", "had", "do", "does", "did", "it", "its", "you", "your", "he", "she",
    "they", "their", "this", "that", "from", "at", "which", "who", "whom", "this"
}

KNOWN_SKILLS = {
    "python", "fastapi", "flask", "django", "sqlalchemy", "postgresql", "postgres",
    "mysql", "redis", "mongodb", "docker", "kubernetes", "aws", "gcp", "azure",
    "react", "vue", "angular", "javascript", "typescript", "html", "css", "tailwind",
    "git", "linux", "ci/cd", "celery", "arq", "pandas", "numpy", "scikit-learn",
    "pytorch", "tensorflow", "nlp", "rest", "graphql", "sql", "agile", "scrum"
}

class NLPTokenizer:
    @staticmethod
    def tokenize(text: str) -> list[str]:
        """
        Tokenizes text into normalized lowercase keywords, removing stop-words and punctuation.
        """
        if not text:
            return []
        # Find all alphanumeric words or technical terms containing C++/C#/CI/CD
        words = re.findall(r'\b[a-zA-Z0-9\+\#\/\-\.]+\b', text.lower())
        tokens = [w.strip() for w in words if w not in COMMON_STOP_WORDS and len(w) > 1]
        return tokens

    @staticmethod
    def extract_skills(text: str) -> list[str]:
        """
        Identifies known technical skills from text using taxonomy matching.
        """
        if not text:
            return []
        text_lower = text.lower()
        found_skills = set()
        for skill in KNOWN_SKILLS:
            # Match word boundaries or specialized forms
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        return sorted(list(found_skills))

    @staticmethod
    def extract_experience_years(text: str) -> float:
        """
        Extracts total years of experience from text using regex patterns.
        """
        if not text:
            return 0.0
        
        patterns = [
            r'(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)\s+of\s+experience',
            r'experience\s*(?:of|:)?\s*(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)',
            r'(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)\s+experience',
            r'(\d+)\s*(?:-|to)\s*(\d+)\s*years'
        ]
        
        text_lower = text.lower()
        max_exp = 0.0
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if isinstance(match, tuple):
                    # Take the highest number in range e.g. "3 to 5 years" -> 5
                    nums = [float(m) for m in match if m]
                    if nums:
                        max_exp = max(max_exp, max(nums))
                else:
                    try:
                        val = float(match)
                        max_exp = max(max_exp, val)
                    except ValueError:
                        continue
        return max_exp

    @staticmethod
    def extract_education(text: str) -> str:
        """
        Identifies highest education level mentioned in text.
        """
        if not text:
            return "Not Specified"
        text_lower = text.lower()
        if "ph.d" in text_lower or "doctorate" in text_lower:
            return "Ph.D."
        elif "master" in text_lower or "m.sc" in text_lower or "m.tech" in text_lower or "mba" in text_lower:
            return "Master's Degree"
        elif "bachelor" in text_lower or "b.sc" in text_lower or "b.tech" in text_lower or "degree" in text_lower:
            return "Bachelor's Degree"
        elif "diploma" in text_lower or "associate" in text_lower:
            return "Diploma / Associate"
        return "Not Specified"
