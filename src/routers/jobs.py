from datetime import datetime

import structlog
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AppError
from src.db.session import get_db
from src.models.job import JobDescription
from src.services.nlp import NLPTokenizer

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/jobs", tags=["Jobs & Vacancies Management"])

class JobCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    department: str | None = Field(None, max_length=100)
    description: str = Field(..., min_length=10)
    required_skills: str | None = Field(None, description="Comma-separated skills or JSON")
    min_experience_years: float = Field(0.0, ge=0.0)

class JobResponse(BaseModel):
    id: int
    title: str
    department: str | None
    description: str
    required_skills: str
    min_experience_years: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(job_in: JobCreate, db: AsyncSession = Depends(get_db)):
    """
    Creates a new job description and automatically extracts skills via NLP if not explicitly provided.
    """
    skills = job_in.required_skills
    if not skills or not skills.strip():
        extracted = NLPTokenizer.extract_skills(job_in.description)
        skills = ", ".join(extracted)

    db_job = JobDescription(
        title=job_in.title,
        department=job_in.department,
        description=job_in.description,
        required_skills=skills,
        min_experience_years=job_in.min_experience_years
    )
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    logger.info("job_description_created", job_id=db_job.id, title=db_job.title)
    return db_job

@router.get("/", response_model=list[JobResponse])
async def list_jobs(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieves a list of job descriptions.
    """
    result = await db.execute(select(JobDescription).offset(skip).limit(limit))
    jobs = result.scalars().all()
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieves a specific job description by ID.
    """
    result = await db.execute(select(JobDescription).where(JobDescription.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise AppError(f"Job description with ID {job_id} not found.", status_code=404)
    return job
