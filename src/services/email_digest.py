import structlog

from src.services.email import EmailService

logger = structlog.get_logger()

class EmailDigestService:
    @staticmethod
    async def dispatch_batch_digest(
        hr_email: str,
        job_title: str,
        total_screened: int,
        top_candidate: str,
        top_score: float
    ) -> bool:
        """
        Dispatches HR batch screening digest summary email alert.
        """
        logger.info("dispatching_hr_digest", hr_email=hr_email, job_title=job_title, total_screened=total_screened)
        return await EmailService.send_hr_digest(
            hr_email=hr_email,
            job_title=job_title,
            total_screened=total_screened,
            top_candidate=top_candidate,
            top_score=top_score
        )
