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

## Phase 3 Status: COMPLETED - Resume File Processing Service (PDF & DOCX)
- File validation service (`src/services/upload.py`) for format, size, and magic headers.
- PDF parser (`src/services/pdf_parser.py`) via pdfplumber and pypdf fallback.
- DOCX parser (`src/services/docx_parser.py`) via python-docx.
- Local storage manager (`src/services/storage.py`) for secure async file persistence.

## Phase 4 Status: COMPLETED - Job Description Processing & Keyword Tokenizer
- Job Description Ingestion API (`src/routers/jobs.py`) created.
- NLP Keyword Tokenizer (`src/services/nlp.py`) implemented for tokenization and skill extraction.
- Taxonomy Categorizer (`src/services/taxonomy.py`) for Hard Skills, Soft Skills, Education, and Experience.
- Requirement Weight Matrix (`src/services/weighting.py`) for composite score calculations.
- Comprehensive unit tests (`tests/test_jobs.py`) added.

## Phase 5 Status: COMPLETED - Core Candidate Filtering & Matching Scoring Engine
- TF-IDF Matcher Engine (`src/services/tfidf_matcher.py`) for semantic relevance scoring.
- Exact & Synonym Skill Matching Algorithm (`src/services/skill_matcher.py`).
- Experience Duration Extractor & Parser (`src/services/experience_parser.py`).
- Composite Score Engine (`src/services/composite_scorer.py`) for aggregated 0-100% ranking.
- Comprehensive matching test coverage (`tests/test_matching.py`).

## Phase 6 Status: COMPLETED - Candidate Ranking & Shortlisting API
- Batch candidate screening execution API (`POST /api/v1/screener/rank`) in `src/routers/screener.py`.
- Dynamic score filtering and pagination (`GET /api/v1/screener/results/{job_id}`).
- Candidate shortlisting lifecycle manager (`src/services/candidate_lifecycle.py`).
- Detailed candidate score breakdown endpoint (`GET /api/v1/screener/candidate/{id}/breakdown`).
- Integration tests (`tests/test_screener.py`) added.

## Phase 7 Status: COMPLETED - Export Engine (Excel & CSV Detailed Reports)
- Formatted Excel workbook builder (`src/services/export.py`) with custom styling and branding.
- Multi-sheet candidate evaluation report generator (Summary + Skill Breakdown sheets).
- CSV export endpoint (`GET /api/v1/export/csv/{job_id}`) in `src/routers/export.py`.
- Streaming download response handlers for bulk export performance (`GET /api/v1/export/excel/{job_id}`).
- Comprehensive export unit tests (`tests/test_export.py`).

## Phase 8 Status: COMPLETED - SMTP Email Notification & Alert Subsystem
- Async SMTP client (`src/services/email.py`) with Jinja2 HTML template rendering.
- Branded shortlisted candidate notification template (`src/templates/email_shortlisted.html`).
- HR batch screening digest summary email alert service (`src/services/email_digest.py`).
- Async background task email dispatchers attached to candidate shortlisting endpoints.
- Comprehensive mock SMTP test suite (`tests/test_email.py`).

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

## Phase 11 Status: IN PROGRESS (Step 2 Completed) - Asynchronous Redis Task Queue & Worker Nodes
- Integrated Redis client configuration (`redis_url`) in `src/core/config.py`.
- Setup ARQ task queue worker settings (`src/core/worker.py`) for asynchronous background processing.
- Implemented background worker task function (`parse_and_score_resume_task`) for async document parsing and ML candidate scoring.
