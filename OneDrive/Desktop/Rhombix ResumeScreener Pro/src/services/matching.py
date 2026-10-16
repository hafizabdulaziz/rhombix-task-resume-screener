import math
import re
from typing import List, Dict, Set, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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

class ResumeMatcher:
    @staticmethod
    def normalize_skills(skills: List[str]) -> Set[str]:
        normalized = set()
        for skill in skills:
            clean = skill.lower().strip()
            resolved = SYNONYM_MAP.get(clean, clean)
            normalized.add(resolved)
        return normalized

    @staticmethod
    def calculate_tfidf_similarity(job_description: str, resume_text: str) -> float:
        """
        Calculates cosine similarity between job description and resume text using TF-IDF.
        Returns a score between 0.0 and 1.0.
        """
        if not job_description or not resume_text:
            return 0.0
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([job_description, resume_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(max(0.0, min(1.0, similarity)))
        except Exception as e:
            logger.error("tfidf_calculation_failed", error=str(e))
            return 0.0

    @staticmethod
    def calculate_skill_match(required_skills: List[str], candidate_skills: List[str]) -> Tuple[float, List[str], List[str]]:
        """
        Calculates exact and synonym skill match percentage.
        Returns (match_percentage_0_to_100, matched_skills, missing_skills).
        """
        if not required_skills:
            return 100.0, [], []

        req_norm = ResumeMatcher.normalize_skills(required_skills)
        cand_norm = ResumeMatcher.normalize_skills(candidate_skills)

        if not req_norm:
            return 100.0, [], []

        matched = req_norm.intersection(cand_norm)
        missing = req_norm - cand_norm

        match_ratio = len(matched) / len(req_norm)
        percentage = round(match_ratio * 100.0, 2)
        return percentage, sorted(list(matched)), sorted(list(missing))

    @staticmethod
    def calculate_experience_score(required_years: float, candidate_years: float) -> float:
        """
        Calculates experience score based on required vs candidate experience.
        If candidate meets or exceeds required years, score is 100%.
        Otherwise, scaled proportionally.
        """
        if required_years <= 0.0:
            return 100.0
        if candidate_years >= required_years:
            return 100.0
        
        ratio = candidate_years / required_years
        return round(ratio * 100.0, 2)

    @staticmethod
    def compute_composite_score(
        job_description: str,
        resume_text: str,
        required_skills: List[str],
        candidate_skills: List[str],
        required_experience_years: float,
        candidate_experience_years: float,
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, any]:
        """
        Computes weighted composite score (0-100%) combining:
        - Skills match (default weight: 0.45)
        - TF-IDF semantic/keyword similarity (default weight: 0.30)
        - Experience match (default weight: 0.25)
        """
        if weights is None:
            weights = {"skills": 0.45, "similarity": 0.30, "experience": 0.25}

        skill_score, matched_skills, missing_skills = ResumeMatcher.calculate_skill_match(required_skills, candidate_skills)
        similarity_score = ResumeMatcher.calculate_tfidf_similarity(job_description, resume_text) * 100.0
        experience_score = ResumeMatcher.calculate_experience_score(required_experience_years, candidate_experience_years)

        w_skills = weights.get("skills", 0.45)
        w_sim = weights.get("similarity", 0.30)
        w_exp = weights.get("experience", 0.25)

        total_weight = w_skills + w_sim + w_exp
        if total_weight <= 0:
            total_weight = 1.0

        composite = (
            (skill_score * w_skills) +
            (similarity_score * w_sim) +
            (experience_score * w_exp)
        ) / total_weight

        composite_rounded = round(max(0.0, min(100.0, composite)), 2)

        return {
            "composite_score": composite_rounded,
            "skill_match_score": skill_score,
            "similarity_score": round(similarity_score, 2),
            "experience_score": experience_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "candidate_experience_years": candidate_experience_years,
            "required_experience_years": required_experience_years
        }
