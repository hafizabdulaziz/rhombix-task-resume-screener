import structlog
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = structlog.get_logger()

class TFIDFMatcher:
    @staticmethod
    def calculate_similarity(job_description: str, resume_text: str) -> float:
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
            score = float(max(0.0, min(1.0, similarity)))
            logger.info("tfidf_similarity_calculated", score=score)
            return score
        except Exception as e:
            logger.error("tfidf_calculation_failed", error=str(e))
            return 0.0
