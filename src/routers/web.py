from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional

from src.db.session import get_db
from src.models.candidate import Candidate, CandidateStatus, ResumeFile, ExtractionData
from src.models.job import JobDescription, MatchResult
from src.services.parser import ResumeParser
from src.services.storage import StorageManager
from src.services.nlp import NLPTokenizer
from src.core.exceptions import AppError
import structlog

logger = structlog.get_logger()

templates = Jinja2Templates(directory="src/templates")
router = APIRouter(tags=["Web UI"])

@router.get("/", response_class=HTMLResponse)
async def dashboard_view(
    request: Request,
    success: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    tab: Optional[str] = Query("candidates"),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Metrics
        cand_count_res = await db.execute(select(func.count(Candidate.id)))
        total_candidates = cand_count_res.scalar() or 0

        shortlisted_res = await db.execute(select(func.count(Candidate.id)).where(Candidate.status == CandidateStatus.SHORTLISTED))
        shortlisted_count = shortlisted_res.scalar() or 0

        jobs_count_res = await db.execute(select(func.count(JobDescription.id)))
        total_jobs = jobs_count_res.scalar() or 0

        # Jobs list
        jobs_res = await db.execute(select(JobDescription).order_by(JobDescription.created_at.desc()))
        jobs = jobs_res.scalars().all()

        # Candidates list with resumes & extractions
        cand_res = await db.execute(
            select(Candidate).options(
                selectinload(Candidate.resumes).selectinload(ResumeFile.extraction)
            ).order_by(Candidate.created_at.desc())
        )
        candidates = cand_res.scalars().all()

    except Exception as e:
        logger.error("dashboard_view_error", error=str(e))
        total_candidates = 0
        shortlisted_count = 0
        total_jobs = 0
        jobs = []
        candidates = []

    return templates.TemplateResponse(request, "dashboard.html", {
        "total_candidates": total_candidates,
        "shortlisted_count": shortlisted_count,
        "total_jobs": total_jobs,
        "jobs": jobs,
        "candidates": candidates,
        "success_message": success,
        "error_message": error,
        "active_tab": tab
    })

@router.get("/jobs", response_class=RedirectResponse)
async def jobs_redirect():
    return RedirectResponse(url="/?tab=jobs", status_code=303)

@router.post("/jobs", response_class=RedirectResponse)
async def create_job_form(
    title: str = Form(...),
    department: str = Form(None),
    description: str = Form(...),
    required_skills: str = Form(None),
    min_experience_years: float = Form(0.0),
    db: AsyncSession = Depends(get_db)
):
    try:
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
        logger.info("web_job_created", title=title)
        return RedirectResponse(url="/?tab=jobs&success=Job+description+created+successfully", status_code=303)
    except Exception as e:
        logger.error("web_job_create_error", error=str(e))
        return RedirectResponse(url="/?tab=jobs&error=Failed+to+create+job+description", status_code=303)

@router.get("/upload", response_class=RedirectResponse)
async def upload_redirect():
    return RedirectResponse(url="/?tab=upload", status_code=303)

@router.post("/upload", response_class=RedirectResponse)
async def upload_resumes_form(
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    uploaded_count = 0
    try:
        for file in files:
            file_bytes = await file.read()
            filename = file.filename or "resume.pdf"
            mime_type = file.content_type or "application/pdf"

            if len(file_bytes) == 0:
                continue
            if len(file_bytes) > 10 * 1024 * 1024:
                continue
            
            file_type = "pdf"
            if filename.endswith(".docx") or "docx" in mime_type:
                file_type = "docx"
            elif filename.endswith(".pdf") or "pdf" in mime_type:
                file_type = "pdf"
            else:
                continue

            saved_path = await StorageManager.save_file(file_bytes, filename)
            parsed_data = await ResumeParser.parse_document(file_type, file_bytes)
            raw_text = parsed_data["text"]

            skills = NLPTokenizer.extract_skills(raw_text)
            exp_years = NLPTokenizer.extract_experience_years(raw_text)
            edu = NLPTokenizer.extract_education(raw_text)

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
            uploaded_count += 1

        return RedirectResponse(url=f"/?tab=candidates&success={uploaded_count}+resumes+successfully+uploaded+and+parsed", status_code=303)
    except Exception as e:
        logger.error("web_upload_error", error=str(e))
        return RedirectResponse(url="/?tab=upload&error=Failed+to+upload+resumes", status_code=303)
