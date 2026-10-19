
import structlog
from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AppError
from src.db.session import get_db
from src.models.candidate import Candidate, ExtractionData, ResumeFile
from src.services.nlp import NLPTokenizer
from src.services.parser import ResumeParser
from src.services.storage import StorageManager

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/upload", tags=["Resume Parser & Batch Intake"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_resumes(
    files: list[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Batch uploads resume files (PDF/DOCX), parses text content, extracts skills, experience years, and education using NLP, and stores candidate records.
    """
    uploaded_results = []
    for file in files:
        file_bytes = await file.read()
        filename = file.filename or "resume.pdf"
        mime_type = file.content_type or "application/pdf"

        if len(file_bytes) == 0:
            raise AppError(f"Uploaded file {filename} is empty.", status_code=400)
        if len(file_bytes) > 10 * 1024 * 1024:
            raise AppError(f"File {filename} exceeds 10MB limit.", status_code=400)
        
        file_type = "pdf"
        if filename.endswith(".docx") or "docx" in mime_type:
            file_type = "docx"
        elif filename.endswith(".pdf") or "pdf" in mime_type:
            file_type = "pdf"
        else:
            raise AppError(f"File {filename} format not supported. Only PDF and DOCX are allowed.", status_code=400)

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

        uploaded_results.append({
            "filename": filename,
            "candidate_id": candidate.id,
            "candidate_name": candidate.full_name,
            "skills": skills,
            "experience_years": exp_years
        })

    return {"message": f"Successfully uploaded and parsed {len(uploaded_results)} resumes.", "results": uploaded_results}
