from src.services.ai_embeddings import AIEmbeddingsEngine


def test_embedding_generation():
    text = "Senior Python Developer with FastAPI and PostgreSQL expertise."
    vec = AIEmbeddingsEngine.get_embedding_vector(text)
    assert isinstance(vec, list)
    assert len(vec) == 16

def test_semantic_similarity_score():
    text1 = "Python FastAPI Developer"
    text2 = "FastAPI Python Backend Engineer"
    score = AIEmbeddingsEngine.compute_semantic_score(text1, text2)
    assert 0.0 <= score <= 100.0
    assert score > 40.0
