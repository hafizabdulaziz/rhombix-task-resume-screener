
import structlog

from src.services.experience_parser import ExperienceParser
from src.services.skill_matcher import SkillMatcher
from src.services.tfidf_matcher import TFIDFMatcher

logger = structlog.get_logger()

class CompositeScorer:
    @staticmethod
    def compute_score(
        job_description: str,
        resume_text: str,
        required_skills: list[str],
        candidate_skills: list[str],
        required_experience_years: float,
        candidate_experience_years: float,
        weights: dict[str, float] | None = None
    ) -> dict[str, any]:
        """
        Computes aggregated composite 0-100% scoring calculator combining:
        - Skills match score
        - Experience match score
        - TF-IDF similarity score
        Using weighted matrix.
        """
        if weights is None:
            weights = {"skills": 0.45, "similarity": 0.30, "experience": 0.25}

        skill_score, matched_skills, missing_skills = SkillMatcher.calculate_match(required_skills, candidate_skills)
        similarity_score = TFIDFMatcher.calculate_similarity(job_description, resume_text) * 100.0
        experience_score = ExperienceParser.calculate_experience_score(required_experience_years, candidate_experience_years)

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

        logger.info("composite_score_computed", composite=composite_rounded)
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

    @staticmethod
    def compute_hybrid_score(
        job_description: str,
        resume_text: str,
        required_skills: list[str],
        candidate_skills: list[str],
        required_experience_years: float,
        candidate_experience_years: float,
        weights: dict[str, float] | None = None
    ) -> dict[str, any]:
        """
        Hybrid Scoring Engine combining exact keyword/skill matching & traditional metrics with AI semantic vector embeddings.
        """
        from src.services.ai_embeddings import AIEmbeddingsEngine

        base_result = CompositeScorer.compute_score(
            job_description=job_description,
            resume_text=resume_text,
            required_skills=required_skills,
            candidate_skills=candidate_skills,
            required_experience_years=required_experience_years,
            candidate_experience_years=candidate_experience_years,
            weights=weights
        )

        semantic_score = AIEmbeddingsEngine.compute_semantic_score(job_description, resume_text)
        hybrid_score = round((base_result["composite_score"] * 0.5) + (semantic_score * 0.5), 2)

        base_result["semantic_score"] = semantic_score
        base_result["hybrid_score"] = hybrid_score
        base_result["composite_score"] = hybrid_score
        return base_result
