from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import io

from src.db.session import get_db
from src.models.candidate import Candidate
from src.models.job import JobDescription, MatchResult
from src.services.export import ReportExporter
from src.core.exceptions import AppError
import structlog

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/export", tags=["Report Export"])

async def get_job_and_results(job_id: int, db: AsyncSession):
    job_res = await db.execute(select(JobDescription).where(JobDescription.id == job_id))
    job = job_res.scalar_one_or_none()
    if not job:
        raise AppError(f"Job description with ID {job_id} not found.", status_code=404)

    match_res = await db.execute(
        select(MatchResult).options(
            selectinload(MatchResult.candidate),
            selectinload(MatchResult.skill_scores)
        ).where(MatchResult.job_id == job_id).order_by(MatchResult.composite_score.desc())
    )
    match_results = match_res.scalars().all()

    results_list = []
    for mr in match_results:
        results_list.append({
            "candidate_name": mr.candidate.full_name,
            "candidate_email": mr.candidate.email,
            "composite_score": mr.composite_score,
            "skill_match_score": mr.skill_match_score,
            "experience_match_score": mr.experience_match_score,
            "semantic_score": mr.semantic_score,
            "status": mr.candidate.status.value,
            "skill_scores": mr.skill_scores
        })
    return job, results_list

@router.get("/excel/{job_id}", status_code=status.HTTP_200_OK)
async def export_excel(job_id: int, db: AsyncSession = Depends(get_db)):
    """
    Exports styled multi-sheet Excel evaluation report for a specific job screening.
    """
    job, results_list = await get_job_and_results(job_id, db)
    excel_bytes = ReportExporter.generate_excel_report(job.title, results_list)

    headers = {
        'Content-Disposition': f'attachment; filename="evaluation_report_job_{job_id}.xlsx"'
    }
    return StreamingResponse(
        io.BytesIO(excel_bytes),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers=headers
    )

@router.get("/csv/{job_id}", status_code=status.HTTP_200_OK)
async def export_csv(job_id: int, db: AsyncSession = Depends(get_db)):
    """
    Exports lightweight CSV summary report for a specific job screening.
    """
    job, results_list = await get_job_and_results(job_id, db)
    csv_str = ReportExporter.generate_csv_report(results_list)

    headers = {
        'Content-Disposition': f'attachment; filename="summary_report_job_{job_id}.csv"'
    }
    return StreamingResponse(
        io.StringIO(csv_str),
        media_type='text/csv',
        headers=headers
    )
