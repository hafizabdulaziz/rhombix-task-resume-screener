import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AppError
from src.models.candidate import Candidate, CandidateStatus

logger = structlog.get_logger()

class CandidateLifecycleManager:
    @staticmethod
    async def update_status(db: AsyncSession, candidate_id: int, new_status: CandidateStatus) -> Candidate:
        """
        Updates candidate status (Pending, Shortlisted, Rejected, On-Hold).
        """
        res = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
        candidate = res.scalar_one_or_none()
        if not candidate:
            raise AppError(f"Candidate with ID {candidate_id} not found.", status_code=404)

        old_status = candidate.status
        candidate.status = new_status
        await db.commit()
        await db.refresh(candidate)

        logger.info("candidate_status_updated", candidate_id=candidate_id, old_status=old_status, new_status=new_status)
        return candidate
