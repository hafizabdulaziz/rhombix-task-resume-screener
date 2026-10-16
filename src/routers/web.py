from fastapi import APIRouter, Depends, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from src.db.session import get_db
from src.models.candidate import Candidate, CandidateStatus, ResumeFile, ExtractionData
from src.models.job import JobDescription
from src.services.parser import ResumeParser
from src.services.storage import StorageManager
from src.services.nlp import NLPTokenizer
import structlog

logger = structlog.get_logger()

templates = Jinja2Templates(directory="src/templates")
router = APIRouter(tags=["Web UI"])

@router.get("/", response_class=HTMLResponse)
async def dashboard_view(request: Request, db: AsyncSession = Depends(get_db)):
    cand_count_res = await db.execute(select(func.count(Candidate.id)))
    total_candidates = cand_count_res.scalar() or 0

    shortlisted_res = await db.execute(select(func.count(Candidate.id)).where(Candidate.status == CandidateStatus.SHORTLISTED))
    shortlisted_count = shortlisted_res.scalar() or 0

    jobs_count_res = await db.execute(select(func.count(JobDescription.id)))
    total_jobs = jobs_count_res.scalar() or 0

    return templates.TemplateResponse(request, "dashboard.html", {
        "total_candidates": total_candidates,
        "shortlisted_count": shortlisted_count,
        "total_jobs": total_jobs
    })

@router.get("/jobs", response_class=HTMLResponse)
async def jobs_view(request: Request, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(JobDescription).order_by(JobDescription.created_at.desc()))
    jobs = res.scalars().all()
    return templates.TemplateResponse(request, "jobs.html", {
        "jobs": jobs
    })

@router.post("/jobs", response_class=RedirectResponse)
async def create_job_form(
    title: str = Form(...),
    department: str = Form(None),
    description: str = Form(...),
    required_skills: str = Form(None),
    min_experience_years: float = Form(0.0),
    db: AsyncSession = Depends(get_db)
):
    skills = required_skills
    if not skills or not skills.strip():
        extracted = NLPTokenizer.extract_skills(description)
        skills = ", ".join(extracted)

    db_job = JobDescription(
        title=title,
        department=department,
        description=description,
        required_skills=skills,
        min_experience_years=min_experience_years
    )
    db.add(db_job)
    await db.commit()
    return RedirectResponse(url="/jobs", status_code=303)

@router.get("/upload", response_class=HTMLResponse)
async def upload_view(request: Request):
    return templates.TemplateResponse(request, "upload.html", {})

@router.post("/upload", response_class=RedirectResponse)
async def upload_resumes_form(
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    for file in files:
        file_bytes = await file.read()
        filename = file.filename or "resume.pdf"
        mime_type = file.content_type or "application/pdf"

        # Validate file
        if len(file_bytes) == 0:
            raise AppError("Uploaded file is empty.", status_code=400)
        if len(file_bytes) > 10 * 1024 * 1024:
            raise AppError("File size exceeds 10MB limit.", status_code=400)
        if not (filename.endswith(".pdf") or filename.endswith(".docx")):
            raise AppError("Only PDF and DOCX files are allowed.", status_code=400)

        # Save file
        saved_path = await StorageManager.save_file(file_bytes, filename)

        # Extract text
        if "pdf" in mime_type.lower() or filename.endswith(".pdf"):
            raw_text = ResumeParser.extract_text_from_pdf(file_bytes)
        else:
            raw_text = ResumeParser.extract_text_from_docx(file_bytes)

        skills = NLPTokenizer.extract_skills(raw_text)
        exp_years = NLPTokenizer.extract_experience_years(raw_text)
        edu = NLPTokenizer.extract_education(raw_text)

        # Create candidate or find existing
        email = f"{filename.lower().replace(' ', '_')}@candidate.com"
        cand_res = await db.execute(select(Candidate).where(Candidate.email == email))
        candidate = cand_res.scalar_one_or_none()

        if not candidate:
            candidate = Candidate(full_name=filename.rsplit('.', 1)[0].replace('_', ' ').title(), email=email)
            db.add(candidate)
            await db.flush()

        resume_record = ResumeFile(
            candidate_id=candidate.id,
            file_name=filename,
            file_path=saved_path,
            file_size=len(file_bytes),
            mime_type=mime_type
        )
        db.add(resume_record)
        await db.flush()

        extraction = ExtractionData(
            resume_file_id=resume_record.id,
            raw_text=raw_text,
            parsed_skills=", ".join(skills),
            experience_years=exp_years,
            education_level=edu
        )
        db.add(extraction)
        await db.commit()

    return RedirectResponse(url="/", status_code=303)
