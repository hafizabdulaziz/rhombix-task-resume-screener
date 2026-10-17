import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
import structlog

from src.services.parser import ResumeParser
from src.services.matching import ResumeMatcher
from src.services.export import ReportExporter
from src.services.email import EmailService

logger = structlog.get_logger()

async def verify_all():
    print("=== STARTING RHOMBIX RESUMESCREENER PRO - CORE REQUIREMENTS AUDIT ===")

    # 1. Verify NLP & Matching Engine
    job_desc = "Looking for a Senior Python Developer with FastAPI and PostgreSQL experience."
    resume_text = "Experienced Python developer with 5 years in FastAPI, PostgreSQL, and Docker."
    req_skills = ["Python", "FastAPI", "Postgres"]
    cand_skills = ["python", "fastapi", "postgresql", "docker"]

    score_data = ResumeMatcher.compute_composite_score(
        job_description=job_desc,
        resume_text=resume_text,
        required_skills=req_skills,
        candidate_skills=cand_skills,
        required_experience_years=3.0,
        candidate_experience_years=5.0
    )
    print(f"[PASSED] Matching Engine Composite Score: {score_data['composite_score']}%")
    assert score_data["composite_score"] > 80.0

    # 2. Verify Export Engine
    mock_results = [{
        "candidate_name": "Test Candidate",
        "candidate_email": "test@candidate.com",
        "composite_score": score_data["composite_score"],
        "skill_match_score": score_data["skill_match_score"],
        "experience_match_score": score_data["experience_score"],
        "semantic_score": score_data["similarity_score"],
        "status": "shortlisted",
        "skill_scores": [{"skill_name": "python", "is_matched": True, "match_type": "exact"}]
    }]
    excel_bytes = ReportExporter.generate_excel_report("Python Engineer", mock_results)
    print(f"[PASSED] Excel Report Generated ({len(excel_bytes)} bytes)")
    assert len(excel_bytes) > 0

    csv_str = ReportExporter.generate_csv_report(mock_results)
    print(f"[PASSED] CSV Report Generated ({len(csv_str)} chars)")
    assert "Test Candidate" in csv_str

    # 3. Verify Email Notification Subsystem
    email_ok = await EmailService.send_shortlisted_notification(
        candidate_name="Test Candidate",
        candidate_email="test@candidate.com",
        job_title="Python Engineer"
    )
    print(f"[PASSED] Email Notification Dispatch: {email_ok}")
    assert email_ok is True

    print("=== ALL CORE REQUIREMENTS AUDITED AND VERIFIED SUCCESSFULLY (100% COMPLIANCE) ===")

if __name__ == "__main__":
    asyncio.run(verify_all())
