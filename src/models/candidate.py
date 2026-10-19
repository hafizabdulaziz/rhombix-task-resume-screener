import enum
from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class CandidateStatus(str, enum.Enum):
    PENDING = "pending"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    ON_HOLD = "on_hold"

class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[CandidateStatus] = mapped_column(SQLEnum(CandidateStatus), default=CandidateStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    resumes: Mapped[list["ResumeFile"]] = relationship("ResumeFile", back_populates="candidate", cascade="all, delete-orphan")
    match_results: Mapped[list["MatchResult"]] = relationship("MatchResult", back_populates="candidate", cascade="all, delete-orphan")

class ResumeFile(Base):
    __tablename__ = "resume_files"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"))
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(512))
    file_size: Mapped[int] = mapped_column(Integer)
    mime_type: Mapped[str] = mapped_column(String(100))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))

    candidate: Mapped["Candidate"] = relationship("Candidate", back_populates="resumes")
    extraction: Mapped["ExtractionData | None"] = relationship("ExtractionData", back_populates="resume", uselist=False, cascade="all, delete-orphan")

class ExtractionData(Base):
    __tablename__ = "extraction_data"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resume_file_id: Mapped[int] = mapped_column(ForeignKey("resume_files.id", ondelete="CASCADE"))
    raw_text: Mapped[str] = mapped_column(Text)
    parsed_skills: Mapped[str | None] = mapped_column(Text, nullable=True) # JSON or comma-separated
    experience_years: Mapped[float] = mapped_column(Float, default=0.0)
    education_level: Mapped[str | None] = mapped_column(String(100), nullable=True)
    extracted_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))

    resume: Mapped["ResumeFile"] = relationship("ResumeFile", back_populates="extraction")
