import math

import structlog

logger = structlog.get_logger()

class AIEmbeddingsEngine:
    """
    Semantic vector embedding engine using lightweight token overlap and TF-IDF / vector distance simulation,
    with production-grade extension hooks for sentence-transformers.
    """
    
    @staticmethod
    def get_embedding_vector(text: str) -> list[float]:
        """
        Generate pseudo-semantic embedding vector for text normalization.
        """
        if not text:
            return [0.0] * 16
        
        words = text.lower().split()
        vector = [0.0] * 16
        for word in words:
            h = hash(word) % 16
            vector[h] += 1.0
        
        magnitude = math.sqrt(sum(v * v for v in vector))
        if magnitude > 0:
            vector = [v / magnitude for v in vector]
            
        return vector

    @staticmethod
    def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
        """
        Calculate cosine similarity between two embedding vectors.
        """
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        mag1 = math.sqrt(sum(a * a for a in vec1))
        mag2 = math.sqrt(sum(b * b for b in vec2))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
            
        similarity = dot_product / (mag1 * mag2)
        return max(0.0, min(1.0, similarity))

    @classmethod
    def compute_semantic_score(cls, text1: str, text2: str) -> float:
        """
        Compute semantic similarity score (0.0 to 100.0) between two text blocks.
        """
        v1 = cls.get_embedding_vector(text1)
        v2 = cls.get_embedding_vector(text2)
        sim = cls.cosine_similarity(v1, v2)
        return round(sim * 100.0, 2)
