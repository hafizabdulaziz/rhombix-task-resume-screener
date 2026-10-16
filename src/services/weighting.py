import structlog

logger = structlog.get_logger()

class WeightingMatrix:
    # Default configurable weights summing to 1.0 (100%)
    DEFAULT_WEIGHTS = {
        "skills_weight": 0.50,
        "experience_weight": 0.30,
        "semantic_weight": 0.20
    }

    @classmethod
    def calculate_composite_score(
        cls,
        skill_score: float,
        experience_score: float,
        semantic_score: float,
        custom_weights: dict | None = None
    ) -> float:
        """
        Calculates composite match score based on weighted factors.
        Scores are expected in range 0.0 to 100.0.
        """
        weights = cls.DEFAULT_WEIGHTS.copy()
        if custom_weights:
            weights.update(custom_weights)

        # Normalize weights if they don't sum to 1.0
        total_w = sum(weights.values())
        if total_w > 0:
            weights = {k: v / total_w for k, v in weights.items()}

        composite = (
            (skill_score * weights["skills_weight"]) +
            (experience_score * weights["experience_weight"]) +
            (semantic_score * weights["semantic_weight"])
        )

        composite = max(0.0, min(100.0, composite))
        logger.info("composite_score_calculated", composite=composite, weights=weights)
        return round(composite, 2)
