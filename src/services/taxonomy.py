import structlog
from src.services.nlp import NLPTokenizer, KNOWN_SKILLS

logger = structlog.get_logger()

HARD_SKILLS = KNOWN_SKILLS

SOFT_SKILLS = {
    "communication", "leadership", "teamwork", "problem solving", "analytical",
    "adaptability", "time management", "creativity", "collaboration", "work ethic",
    "attention to detail", "critical thinking", "interpersonal", "organization"
}

class TaxonomyCategorizer:
    @staticmethod
    def categorize_skills(skills_list: list[str]) -> dict:
        """
        Categorizes a list of skills into Hard Skills and Soft Skills.
        """
        hard = []
        soft = []
        for skill in skills_list:
            s_lower = skill.lower().strip()
            if s_lower in SOFT_SKILLS:
                soft.append(skill)
            else:
                hard.append(skill)
        return {
            "hard_skills": sorted(list(set(hard))),
            "soft_skills": sorted(list(set(soft)))
        }

    @staticmethod
    def extract_full_taxonomy(text: str) -> dict:
        """
        Extracts comprehensive taxonomy from text including hard skills, soft skills, education, and experience years.
        """
        all_tokens = NLPTokenizer.tokenize(text)
        all_skills = NLPTokenizer.extract_skills(text)
        
        # Also check soft skills
        text_lower = text.lower()
        found_soft = []
        for soft in SOFT_SKILLS:
            if soft in text_lower:
                found_soft.append(soft)

        categorized = TaxonomyCategorizer.categorize_skills(all_skills + found_soft)
        education = NLPTokenizer.extract_education(text)
        experience = NLPTokenizer.extract_experience_years(text)

        logger.info("taxonomy_extracted", hard_count=len(categorized["hard_skills"]), soft_count=len(categorized["soft_skills"]), experience=experience, education=education)
        return {
            "hard_skills": categorized["hard_skills"],
            "soft_skills": categorized["soft_skills"],
            "education_level": education,
            "experience_years": experience,
            "raw_tokens_count": len(all_tokens)
        }
