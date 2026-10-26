# Rhombix ResumeScreener Pro

Enterprise-grade AI & Hybrid Resume Screening & Candidate Matching Platform built with FastAPI, SQLAlchemy 2.0 (Async), and Modern Python.

## Phase 1 Status: COMPLETED
- Project structure (`src/`, `tests/`, `docs/`, `scripts/`) initialized.
- FastAPI async application factory & global exception middleware configured.
- Pydantic Settings & structured logging (`structlog`) integrated.
- SQLAlchemy 2.0 AsyncEngine and session management configured.
- Comprehensive test suite & core requirements verified (100% passing).

## Phase 2 Status: COMPLETED - Database Schema & Migration Engine Setup
- Candidate & Resume persistence models (`Candidate`, `ResumeFile`, `ExtractionData`) created (`src/models/candidate.py`).
- Job Description & Scoring result models (`JobDescription`, `MatchResult`, `SkillScore`) created (`src/models/job.py`).
- Alembic async environment and configuration configured (`alembic.ini`, `alembic/env.py`).
- Initial baseline migration created and applied (`alembic/versions/001_initial_baseline.py`).
- Database seeding script (`scripts/seed_data.py`) implemented for initial job and candidate records.

### Database Setup & Migration Guide
1. Configure `.env` with `DATABASE_URL` (SQLite or PostgreSQL async URL).
2. Run migrations:
   ```bash
   alembic upgrade head
   ```
3. Run seed script:
   ```bash
   python scripts/seed_data.py
   ```
