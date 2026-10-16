import pytest
from src.services.email import EmailService

@pytest.mark.asyncio
async def test_email_service():
    success_shortlist = await EmailService.send_shortlisted_notification(
        candidate_name="Alice Smith",
        candidate_email="alice@example.com",
        job_title="Senior Python Developer"
    )
    assert success_shortlist is True

    success_digest = await EmailService.send_hr_digest(
        hr_email="hr@rhombix.com",
        job_title="Senior Python Developer",
        total_screened=10,
        top_candidate="Alice Smith",
        top_score=95.5
    )
    assert success_digest is True
