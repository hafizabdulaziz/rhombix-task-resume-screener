import re
import structlog

logger = structlog.get_logger()

class ExperienceParser:
    @staticmethod
    def extract_experience_years(text: str) -> float:
        """
        Builds candidate experience duration calculation logic and regex date-range parser.
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
                    nums = [float(m) for m in match if m]
                    if nums:
                        max_exp = max(max_exp, max(nums))
                else:
                    try:
                        val = float(match)
                        max_exp = max(max_exp, val)
                    except ValueError:
                        continue

        logger.info("experience_years_extracted", years=max_exp)
        return max_exp

    @staticmethod
    def calculate_experience_score(required_years: float, candidate_years: float) -> float:
        """
        Calculates experience score based on required vs candidate experience.
        """
        if required_years <= 0.0:
            return 100.0
        if candidate_years >= required_years:
            return 100.0

        ratio = candidate_years / required_years
        score = round(ratio * 100.0, 2)
        logger.info("experience_score_calculated", score=score, required=required_years, candidate=candidate_years)
        return score
