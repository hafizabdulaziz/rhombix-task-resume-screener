from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any, List

from src.db.session import get_db
from src.models.candidate import Candidate, CandidateStatus
from src.models.job import JobDescription, MatchResult

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics & Reporting"])

@router.get("/metrics", response_model=Dict[str, Any])
async def get_analytics_metrics(db: AsyncSession = Depends(get_db)):
    """
    Returns aggregated recruiter analytics, pipeline conversion funnel counts,
    and score distribution metrics.
    """
    total_cand = (await db.execute(select(func.count(Candidate.id)))).scalar() or 0
    shortlisted = (await db.execute(select(func.count(Candidate.id)).where(Candidate.status == CandidateStatus.SHORTLISTED))).scalar() or 0
    rejected = (await db.execute(select(func.count(Candidate.id)).where(Candidate.status == CandidateStatus.REJECTED))).scalar() or 0
    pending = (await db.execute(select(func.count(Candidate.id)).where(Candidate.status == CandidateStatus.PENDING))).scalar() or 0
    
    total_jobs = (await db.execute(select(func.count(JobDescription.id)))).scalar() or 0

    # Score distribution buckets from MatchResult
    score_res = await db.execute(select(MatchResult.overall_score))
    scores = [s[0] for s in score_res.all() if s[0] is not None]

    buckets = {"0-20": 0, "21-40": 0, "41-60": 0, "61-80": 0, "81-100": 0}
    for sc in scores:
        if sc <= 20: buckets["0-20"] += 1
        elif sc <= 40: buckets["21-40"] += 1
        elif sc <= 60: buckets["41-60"] += 1
        elif sc <= 80: buckets["61-80"] += 1
        else: buckets["81-100"] += 1

    return {
        "funnel": {
            "uploaded": total_cand,
            "screened": len(scores),
            "shortlisted": shortlisted,
            "rejected": rejected,
            "pending": pending
        },
        "score_distribution": buckets,
        "total_jobs": total_jobs,
        "average_score": round(sum(scores) / len(scores), 2) if scores else 0.0
    }
