from src.services.composite_scorer import CompositeScorer
from src.services.experience_parser import ExperienceParser
from src.services.matching import ResumeMatcher
from src.services.skill_matcher import SkillMatcher
from src.services.tfidf_matcher import TFIDFMatcher


def test_skill_matcher():
    req = ["Python", "FastAPI", "Postgres"]
    cand = ["python", "fastapi", "postgresql", "docker"]
    score, matched, missing = SkillMatcher.calculate_match(req, cand)
    assert score == 100.0
    assert "postgresql" in matched

def test_experience_parser():
    text = "Over 4.5 years of experience in software engineering."
    years = ExperienceParser.extract_experience_years(text)
    assert years == 4.5
    assert ExperienceParser.calculate_experience_score(5.0, 4.0) == 80.0

def test_tfidf_matcher():
    job = "Backend Python Engineer FastAPI"
    resume = "Python engineer with FastAPI experience"
    sim = TFIDFMatcher.calculate_similarity(job, resume)
    assert sim > 0.1

def test_composite_scorer():
    job = "Python FastAPI 3 years"
    resume = "Python FastAPI 3 years"
    result = CompositeScorer.compute_score(
        job_description=job,
        resume_text=resume,
        required_skills=["Python", "FastAPI"],
        candidate_skills=["python", "fastapi"],
        required_experience_years=3.0,
        candidate_experience_years=3.0
    )
    assert result["composite_score"] > 80.0

def test_resume_matcher_legacy():
    req_skills = ["Python", "FastAPI", "Postgres", "Docker"]
    cand_skills = ["python", "fastapi", "postgresql", "react", "git"]
    score, matched, missing = ResumeMatcher.calculate_skill_match(req_skills, cand_skills)
    assert score == 75.0
    assert "docker" in missing
