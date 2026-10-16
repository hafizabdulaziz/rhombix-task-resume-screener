from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    required_skills: Mapped[str] = mapped_column(Text) # JSON list or comma-separated
    min_experience_years: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    match_results: Mapped[list["MatchResult"]] = relationship("MatchResult", back_populates="job", cascade="all, delete-orphan")

class MatchResult(Base):
    __tablename__ = "match_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job_descriptions.id", ondelete="CASCADE"))
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"))
    composite_score: Mapped[float] = mapped_column(Float, default=0.0) # 0-100%
    skill_match_score: Mapped[float] = mapped_column(Float, default=0.0)
    experience_match_score: Mapped[float] = mapped_column(Float, default=0.0)
    semantic_score: Mapped[float] = mapped_column(Float, default=0.0)
    summary_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    job: Mapped["JobDescription"] = relationship("JobDescription", back_populates="match_results")
    candidate: Mapped["Candidate"] = relationship("Candidate", back_populates="match_results")
    skill_scores: Mapped[list["SkillScore"]] = relationship("SkillScore", back_populates="match_result", cascade="all, delete-orphan")

class SkillScore(Base):
    __tablename__ = "skill_scores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    match_result_id: Mapped[int] = mapped_column(ForeignKey("match_results.id", ondelete="CASCADE"))
    skill_name: Mapped[str] = mapped_column(String(100))
    is_matched: Mapped[bool] = mapped_column(default=False)
    match_type: Mapped[str] = mapped_column(String(50), default="exact") # exact, synonym, missing

    match_result: Mapped["MatchResult"] = relationship("MatchResult", back_populates="skill_scores")
