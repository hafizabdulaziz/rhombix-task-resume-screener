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
