import asyncio
import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import AsyncSessionLocal
from src.models import Candidate, JobDescription, CandidateStatus

logger = structlog.get_logger()

async def seed_database():
    logger.info("seeding_database_start")
    async with AsyncSessionLocal() as session:
        # Check if jobs exist
        from sqlalchemy import select
        existing_job = await session.execute(select(JobDescription))
        if existing_job.scalars().first():
            logger.info("database_already_seeded")
            return

        # Create sample job
        job = JobDescription(
            title="Senior Python & AI Engineer",
            department="Engineering",
            description="Looking for an experienced Python Engineer with FastAPI, SQLAlchemy, and AI/NLP experience.",
            required_skills="Python,FastAPI,SQLAlchemy,PostgreSQL,Docker,Machine Learning",
            min_experience_years=3.5
        )
        session.add(job)

        # Create sample candidates
        c1 = Candidate(
            full_name="Alice Smith",
            email="alice.smith@example.com",
            phone="+1-555-0199",
            status=CandidateStatus.PENDING
        )
        c2 = Candidate(
            full_name="Bob Jones",
            email="bob.jones@example.com",
            phone="+1-555-0142",
            status=CandidateStatus.SHORTLISTED
        )
        session.add_all([c1, c2])
        await session.commit()
        logger.info("seeding_database_complete", job_id=job.id)

if __name__ == "__main__":
    asyncio.run(seed_database())
