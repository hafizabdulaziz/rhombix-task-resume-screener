from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, timezone

from src.db.session import get_db
from src.models.candidate import Candidate, CandidateStatus, ResumeFile, ExtractionData
from src.models.job import JobDescription, MatchResult, SkillScore
from src.services.matching import ResumeMatcher
from src.services.candidate_lifecycle import CandidateLifecycleManager
from src.core.exceptions import AppError
import structlog

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/screener", tags=["Screener & Ranking"])

class RankRequest(BaseModel):
    job_id: int
    candidate_ids: Optional[List[int]] = Field(None, description="Optional list of candidate IDs to rank. If omitted, ranks all candidates.")

class SkillScoreResponse(BaseModel):
    skill_name: str
    is_matched: bool
    match_type: str

    model_config = ConfigDict(from_attributes=True)

class MatchResultResponse(BaseModel):
    id: int
    job_id: int
    candidate_id: int
    candidate_name: str
    candidate_email: str
    composite_score: float
    skill_match_score: float
    experience_match_score: float
    semantic_score: float
    summary_notes: Optional[str]
    skill_scores: List[SkillScoreResponse]
    evaluated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class StatusUpdateRequest(BaseModel):
    status: CandidateStatus

@router.post("/rank", response_model=List[MatchResultResponse], status_code=status.HTTP_200_OK)
async def rank_candidates(rank_req: RankRequest, db: AsyncSession = Depends(get_db)):
    """
    Executes batch candidate screening and scoring against a specified Job Description.
    """
    job_res = await db.execute(select(JobDescription).where(JobDescription.id == rank_req.job_id))
    job = job_res.scalar_one_or_none()
    if not job:
        raise AppError(f"Job description with ID {rank_req.job_id} not found.", status_code=404)

    req_skills = [s.strip() for s in job.required_skills.split(",") if s.strip()]

    query = select(Candidate).options(
        selectinload(Candidate.resumes).selectinload(ResumeFile.extraction)
    )
    if rank_req.candidate_ids:
        query = query.where(Candidate.id.in_(rank_req.candidate_ids))

    cand_res = await db.execute(query)
    candidates = cand_res.scalars().all()

    if not candidates:
        return []

    results = []

    for candidate in candidates:
        latest_extraction = None
        for resume in candidate.resumes:
            if resume.extraction:
                latest_extraction = resume.extraction
                break

        resume_text = latest_extraction.raw_text if latest_extraction else ""
        cand_skills = [s.strip() for s in latest_extraction.parsed_skills.split(",") if s.strip()] if (latest_extraction and latest_extraction.parsed_skills) else []
        cand_exp = latest_extraction.experience_years if latest_extraction else 0.0

        score_data = ResumeMatcher.compute_composite_score(
            job_description=job.description,
            resume_text=resume_text,
            required_skills=req_skills,
            candidate_skills=cand_skills,
            required_experience_years=job.min_experience_years,
            candidate_experience_years=cand_exp
        )

        existing_match_res = await db.execute(
            select(MatchResult).options(selectinload(MatchResult.skill_scores)).where(
                MatchResult.job_id == job.id,
                MatchResult.candidate_id == candidate.id
            )
        )
        match_result = existing_match_res.scalar_one_or_none()

        if match_result:
            match_result.composite_score = score_data["composite_score"]
            match_result.skill_match_score = score_data["skill_match_score"]
            match_result.experience_match_score = score_data["experience_score"]
            match_result.semantic_score = score_data["similarity_score"]
            match_result.summary_notes = f"Matched {len(score_data['matched_skills'])} skills out of {len(req_skills)}."
            match_result.evaluated_at = datetime.now(timezone.utc)
            for ss in match_result.skill_scores:
                await db.delete(ss)
            match_result.skill_scores = []
        else:
            match_result = MatchResult(
                job_id=job.id,
                candidate_id=candidate.id,
                composite_score=score_data["composite_score"],
                skill_match_score=score_data["skill_match_score"],
                experience_match_score=score_data["experience_score"],
                semantic_score=score_data["similarity_score"],
                summary_notes=f"Matched {len(score_data['matched_skills'])} skills out of {len(req_skills)}."
            )
            db.add(match_result)
            await db.flush()

        all_skills_set = set(req_skills).union(set(score_data["matched_skills"]))
        for skill in all_skills_set:
            is_matched = skill in score_data["matched_skills"]
            match_type = "exact" if is_matched else "missing"
            skill_score = SkillScore(
                match_result_id=match_result.id,
                skill_name=skill,
                is_matched=is_matched,
                match_type=match_type
            )
            db.add(skill_score)

        await db.commit()
        await db.refresh(match_result)

        results.append({
            "id": match_result.id,
            "job_id": match_result.job_id,
            "candidate_id": candidate.id,
            "candidate_name": candidate.full_name,
            "candidate_email": candidate.email,
            "composite_score": match_result.composite_score,
            "skill_match_score": match_result.skill_match_score,
            "experience_match_score": match_result.experience_match_score,
            "semantic_score": match_result.semantic_score,
            "summary_notes": match_result.summary_notes,
            "skill_scores": match_result.skill_scores,
            "evaluated_at": match_result.evaluated_at
        })

    results.sort(key=lambda x: x["composite_score"], reverse=True)
    logger.info("candidates_ranked", job_id=job.id, total_screened=len(results))
    return results

@router.get("/results/{job_id}", response_model=List[MatchResultResponse])
async def get_job_rankings(
    job_id: int,
    min_score: float = Query(0.0, ge=0.0, le=100.0),
    status_filter: Optional[CandidateStatus] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves ranked candidate results for a specific job with dynamic score and status filtering.
    """
    query = select(MatchResult).options(
        selectinload(MatchResult.candidate),
        selectinload(MatchResult.skill_scores)
    ).where(
        MatchResult.job_id == job_id,
        MatchResult.composite_score >= min_score
    )

    if status_filter:
        query = query.join(Candidate).where(Candidate.status == status_filter)

    query = query.order_by(MatchResult.composite_score.desc()).offset(skip).limit(limit)
    res = await db.execute(query)
    match_results = res.scalars().all()

    response_items = []
    for mr in match_results:
        response_items.append({
            "id": mr.id,
            "job_id": mr.job_id,
            "candidate_id": mr.candidate.id,
            "candidate_name": mr.candidate.full_name,
            "candidate_email": mr.candidate.email,
            "composite_score": mr.composite_score,
            "skill_match_score": mr.skill_match_score,
            "experience_match_score": mr.experience_match_score,
            "semantic_score": mr.semantic_score,
            "summary_notes": mr.summary_notes,
            "skill_scores": mr.skill_scores,
            "evaluated_at": mr.evaluated_at
        })

    return response_items

@router.get("/candidate/{candidate_id}/breakdown", status_code=status.HTTP_200_OK)
async def get_candidate_score_breakdown(candidate_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieves detailed score breakdown for a specific candidate across all applied/matched jobs.
    """
    res = await db.execute(
        select(MatchResult).options(
            selectinload(MatchResult.job),
            selectinload(MatchResult.skill_scores)
        ).where(MatchResult.candidate_id == candidate_id)
    )
    matches = res.scalars().all()
    if not matches:
        raise AppError(f"No match results found for candidate ID {candidate_id}.", status_code=404)

    breakdowns = []
    for m in matches:
        breakdowns.append({
            "match_id": m.id,
            "job_id": m.job_id,
            "job_title": m.job.title,
            "composite_score": m.composite_score,
            "skill_match_score": m.skill_match_score,
            "experience_match_score": m.experience_match_score,
            "semantic_score": m.semantic_score,
            "summary_notes": m.summary_notes,
            "skill_scores": [
                {
                    "skill_name": ss.skill_name,
                    "is_matched": ss.is_matched,
                    "match_type": ss.match_type
                } for ss in m.skill_scores
            ],
            "evaluated_at": m.evaluated_at
        })
    return {"candidate_id": candidate_id, "breakdowns": breakdowns}

@router.patch("/candidates/{candidate_id}/status", status_code=status.HTTP_200_OK)
async def update_candidate_status(candidate_id: int, status_req: StatusUpdateRequest, db: AsyncSession = Depends(get_db)):
    """
    Updates the shortlisting status lifecycle of a candidate using CandidateLifecycleManager.
    """
    candidate = await CandidateLifecycleManager.update_status(db, candidate_id, status_req.status)
    return {"message": "Candidate status updated successfully", "candidate_id": candidate.id, "status": candidate.status}
