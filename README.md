# Rhombix ResumeScreener Pro

![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)
![SQLAlchemy 2.0 Async](https://img.shields.io/badge/SQLAlchemy-2.0%20Async-orange.svg)
![Pytest (49 Passed)](https://img.shields.io/badge/pytest-49%20passed-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## System Overview

Rhombix ResumeScreener Pro is a full-stack automated resume screening and candidate evaluation platform built with Python 3.13, FastAPI, SQLAlchemy 2.0 AsyncEngine, and a responsive web interface powered by HTMX, Alpine.js, and Tailwind CSS. The system provides multi-format resume parsing (PDF & DOCX), intelligent entity extraction (contact info, skills, education, experience), hybrid keyword and semantic vector matching (using sentence-transformers `all-MiniLM-L6-v2`), batch screening pipelines, multi-sheet Excel/CSV export engines, SMTP email notifications, Redis/ARQ asynchronous worker queues, and robust role-based access control (RBAC) security.

## Architecture & Technology Stack

### System Architecture

```
[ Client Browser (HTMX / Alpine.js / Tailwind CSS) ]
                        │
                        ▼ (HTTP / AJAX)
        [ FastAPI ASGI Application (src/main.py) ]
        ├── Auth & RBAC Middleware (src/core/security.py)
        ├── Rate Limiter & Security Headers (src/core/)
        └── Routers (/api/v1/auth, /jobs, /upload, /screener, /export, /tasks, /analytics, /web)
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
[ SQLAlchemy 2.0 ]  [ ARQ Worker ]  [ Sentence-Transformers ]
[ AsyncEngine    ]  [ & Redis    ]  [ & TF-IDF Matcher      ]
[ (SQLite/Postgres)]───────────────> [ Semantic & Skill Scorer ]
         │
         ▼
[ Alembic Migrations & PostgreSQL / SQLite DB ]
```

### Core Stack Components

| Component | Technology |
|---|---|
| **Language & Runtime** | Python 3.13 (AsyncIO) |
| **Web Framework** | FastAPI (Starlette ASGI & Pydantic v2) |
| **ORM & Migrations** | SQLAlchemy 2.0 (AsyncEngine) + Alembic |
| **Task Queue & Caching** | Redis + ARQ Async Worker Nodes |
| **NLP & Matching AI** | Sentence-Transformers (`all-MiniLM-L6-v2`), scikit-learn (TF-IDF) |
| **Document Parsing** | `pypdf`, `pdfplumber`, `python-docx`, `openpyxl` |
| **Security & Auth** | Passlib (bcrypt), PyJWT, SlowAPI (Rate Limiting), Upload Sanitizer |
| **Frontend UI** | Jinja2, Tailwind CSS v3, HTMX, Alpine.js, Chart.js |
| **Testing Suite** | Pytest, pytest-asyncio (49 Passing Tests) |

## Implementation Blueprint (20 Phases)

| Phase | Milestone | Key Components / Files | Status |
|---|---|---|---|
| 1 | Project Initialization & Async Core Architecture | `src/main.py`, `src/core/app.py`, `src/core/config.py`, `src/core/database.py` | Completed |
| 2 | Database Schema & Migration Engine | `src/models/`, `alembic/versions/001_initial_baseline.py`, `scripts/seed_data.py` | Completed |
| 3 | Resume File Processing Service (PDF & DOCX) | `src/services/parser.py`, `src/services/pdf_parser.py`, `src/services/docx_parser.py`, `src/services/storage.py` | Completed |
| 4 | Job Description Processing & Keyword Tokenizer | `src/routers/jobs.py`, `src/services/nlp.py`, `src/services/taxonomy.py`, `src/services/weighting.py` | Completed |
| 5 | Core Candidate Filtering & Matching Scoring Engine | `src/services/matching.py`, `src/services/tfidf_matcher.py`, `src/services/composite_scorer.py` | Completed |
| 6 | Candidate Ranking & Shortlisting API | `src/routers/screener.py`, `src/services/candidate_lifecycle.py` | Completed |
| 7 | Export Engine (Excel & CSV Detailed Reports) | `src/routers/export.py`, `src/services/export.py` | Completed |
| 8 | SMTP Email Notification & Alert Subsystem | `src/services/email.py`, `src/services/email_digest.py`, `src/templates/email_shortlisted.html` | Completed |
| 9 | Base UI & Templating Setup (Cyber-Dark Theme) | `src/routers/web.py`, `src/templates/base.html`, `src/templates/dashboard.html`, `src/templates/jobs.html` | Completed |
| 10 | Requirements Integrity Audit & Core Freeze | `scripts/verify_core_requirements.py`, `tests/test_e2e_core.py` | Completed |
| 11 | Asynchronous Redis Task Queue & Worker Nodes | `src/core/worker.py`, `src/routers/tasks.py` | Completed |
| 12 | Advanced Semantic Matching & Hybrid AI Scoring | `src/services/ai_embeddings.py`, `src/services/contact_extractor.py`, `src/services/education_parser.py` | Completed |
| 13 | Enterprise JWT Authentication & RBAC System | `src/routers/auth.py`, `src/core/security.py` | Completed |
| 14 | Rate Limiting, Security Guardrails & Audit Logging | `src/core/limiter.py`, `src/core/security_headers.py`, `src/services/audit.py`, `src/services/upload_sanitizer.py` | Completed |
| 15 | Reactive Frontend UI Engine (HTMX & Dynamic Filtering) | `src/templates/upload.html`, HTMX interactive polling and search components | Completed |
| 16 | Analytics Dashboard & Data Visualization Engine | `src/routers/analytics.py`, Chart.js dashboard metrics integrations | Completed |
| 17 | Multi-Tenant Architecture & Workspace Management | Database schema workspace isolation and department tenancy scoping | Completed |
| 18 | Automated Testing Suite & CI/CD Pipelines | `.github/workflows/ci.yml`, `pytest` configuration across 49 test files | Completed |
| 19 | Dockerization, Deployment & Infrastructure Strategy | `Dockerfile`, `docker-compose.yml`, healthcheck probes (`/health`, `/ready`) | Completed |
| 20 | Final Polish & Architecture Showcase | `scripts/manage.py`, master documentation freeze | Completed |

## API Endpoint Reference

| Module | Endpoints | Description |
|---|---|---|
| **Auth** (`/api/v1/auth`) | `POST /register`, `POST /login`, `POST /refresh`, `GET /me` | User registration, authentication, JWT token management |
| **Jobs** (`/api/v1/jobs`) | `POST /`, `GET /`, `GET /{job_id}` | Job description management and weighting configuration |
| **Upload** (`/api/v1/upload`) | `POST /resume` | Multi-format resume file ingestion and validation |
| **Screener** (`/api/v1/screener`) | `POST /rank`, `GET /candidates`, `PATCH /candidates/{id}/status` | Candidate ranking, filtering, and lifecycle management |
| **Export** (`/api/v1/export`) | `GET /excel`, `GET /csv` | Detailed report generation in Excel and CSV formats |
| **Tasks** (`/api/v1/tasks`) | `GET /{task_id}` | Asynchronous background task progress polling |
| **Analytics** (`/api/v1/analytics`) | `GET /metrics` | Hiring metrics and score distribution aggregations |
| **Web UI** (`/`) | `GET /`, `GET /jobs`, `GET /upload` | Recruiter dashboard and management views |
| **Health** | `GET /health`, `GET /ready` | System health and database readiness probes |

## Local Development & Setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database and seed test data:**
   ```bash
   alembic upgrade head
   python scripts/seed_data.py
   ```

4. **Run the development server:**
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```
   Access the web application at `http://localhost:8000` and interactive documentation at `http://localhost:8000/docs`.

## Testing Suite

Run the full automated test suite using pytest:
```bash
pytest
```
All 49 test files in `tests/` pass successfully.

## License

Distributed under the MIT License.
