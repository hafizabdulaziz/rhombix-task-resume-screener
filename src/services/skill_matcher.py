from typing import List, Set, Tuple
import structlog

logger = structlog.get_logger()

SYNONYM_MAP = {
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "postgres": "postgresql",
    "postgre": "postgresql",
    "k8s": "kubernetes",
    "aws": "amazon web services",
    "gcp": "google cloud platform",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "ci/cd": "continuous integration",
    "react.js": "react",
    "node.js": "node"
}

class SkillMatcher:
    @staticmethod
    def normalize_skills(skills: List[str]) -> Set[str]:
        normalized = set()
        for skill in skills:
            clean = skill.lower().strip()
            resolved = SYNONYM_MAP.get(clean, clean)
            normalized.add(resolved)
        return normalized

    @staticmethod
    def calculate_match(required_skills: List[str], candidate_skills: List[str]) -> Tuple[float, List[str], List[str]]:
        """
        Calculates exact and synonym skill match percentage.
        Returns (match_percentage_0_to_100, matched_skills, missing_skills).
        """
        if not required_skills:
            return 100.0, [], []

        req_norm = SkillMatcher.normalize_skills(required_skills)
        cand_norm = SkillMatcher.normalize_skills(candidate_skills)

        if not req_norm:
            return 100.0, [], []

        matched = req_norm.intersection(cand_norm)
        missing = req_norm - cand_norm

        match_ratio = len(matched) / len(req_norm)
        percentage = round(match_ratio * 100.0, 2)
        logger.info("skill_match_calculated", percentage=percentage, matched_count=len(matched), missing_count=len(missing))
        return percentage, sorted(list(matched)), sorted(list(missing))
