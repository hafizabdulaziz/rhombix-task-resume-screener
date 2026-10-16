import pytest
from src.services.matching import ResumeMatcher

def test_resume_matcher_skills():
    req_skills = ["Python", "FastAPI", "Postgres", "Docker"]
    cand_skills = ["python", "fastapi", "postgresql", "react", "git"]

    score, matched, missing = ResumeMatcher.calculate_skill_match(req_skills, cand_skills)
    assert score == 75.0  # 3 out of 4 matched ("postgres" matches "postgresql" via synonym)
    assert "python" in matched
    assert "fastapi" in matched
    assert "postgresql" in matched
    assert "docker" in missing

def test_experience_score():
    assert ResumeMatcher.calculate_experience_score(5.0, 5.0) == 100.0
    assert ResumeMatcher.calculate_experience_score(5.0, 7.0) == 100.0
    assert ResumeMatcher.calculate_experience_score(5.0, 2.5) == 50.0
    assert ResumeMatcher.calculate_experience_score(0.0, 2.0) == 100.0

def test_tfidf_similarity():
    job_desc = "We are hiring a Senior Python Backend Developer with FastAPI and SQLAlchemy experience."
    resume_text = "Experienced Python developer skilled in FastAPI, SQLAlchemy, PostgreSQL, and Docker."
    sim = ResumeMatcher.calculate_tfidf_similarity(job_desc, resume_text)
    assert sim > 0.2

def test_composite_score():
    job_desc = "Looking for Python and FastAPI developer with 3 years experience."
    resume_text = "Python developer with 3 years of experience in FastAPI and PostgreSQL."
    req_skills = ["Python", "FastAPI"]
    cand_skills = ["python", "fastapi", "postgresql"]

    result = ResumeMatcher.compute_composite_score(
        job_description=job_desc,
        resume_text=resume_text,
        required_skills=req_skills,
        candidate_skills=cand_skills,
        required_experience_years=3.0,
        candidate_experience_years=3.0
    )

    assert "composite_score" in result
    assert result["composite_score"] > 50.0
    assert result["skill_match_score"] == 100.0
    assert result["experience_score"] == 100.0
