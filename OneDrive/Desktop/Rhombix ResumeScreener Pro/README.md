# Rhombix ResumeScreener Pro 🚀

![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)
![Phase 2](https://img.shields.io/badge/Phase%202-Completed-success.svg)

Enterprise-grade AI & Hybrid Resume Screening & Candidate Matching Platform. Designed with an Enterprise Cyber-Minimalist Dark Mode UI, FastAPI async backend, SQLAlchemy 2.0 AsyncEngine, PostgreSQL, and Redis-backed task workers.

---

## 🌟 Project Vision
Rhombix ResumeScreener Pro automates and optimizes the candidate screening lifecycle for enterprise recruiters. By combining deterministic exact keyword matching, TF-IDF vectorizers, and semantic embeddings with robust ATS workflows, recruitment teams can instantly shortlist, rank, and export candidate evaluations.

---

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python 3.13), AsyncEngine, SQLAlchemy 2.0, Pydantic v2, Structlog.
- **Database & Queue:** PostgreSQL (asyncpg), Redis, ARQ/Celery.
- **NLP & AI:** scikit-learn, spaCy, NLTK, Sentence-Transformers.
- **Frontend:** Tailwind CSS v3, HTMX, Alpine.js, Jinja2 Templates.

---

## 📌 Progress Tracking (Phase 2 Complete)
- [x] **Phase 1: Project Initialization & Async Core Architecture** (Steps 1-5 Completed)
- [x] **Phase 2: Database Schema & Migration Engine** (Steps 1-5 Completed)
- [ ] Phase 3: Resume File Processing Service (PDF & DOCX)
- [ ] Phase 4: Job Description Processing & Keyword Tokenizer
- [ ] Phase 5: Core Candidate Filtering & Matching Scoring Engine
- [ ] Phase 6: Candidate Ranking & Shortlisting API
- [ ] Phase 7: Export Engine (Excel & CSV Detailed Reports)
- [ ] Phase 8: SMTP Email Notification & Alert Subsystem
- [ ] Phase 9: Base UI & Templating Setup (Cyber-Dark Theme)
- [ ] Phase 10: Requirements Integrity Audit & Core Freeze

---

## 🗄️ Database Setup & Migrations

1. **Create PostgreSQL Database:**
   ```sql
   CREATE DATABASE rhombix_resume_screener;
   ```

2. **Run Alembic Migrations:**
   ```bash
   alembic upgrade head
   ```

3. **Seed Initial Data:**
   ```bash
   python scripts/seed_data.py
   ```

---

## 🚀 Getting Started

1. **Clone Repository:**
   ```bash
   git clone https://github.com/hafizabdulaziz/rhombix-task-resume-screener.git
   cd Rhombix ResumeScreener Pro
   ```

2. **Configure Environment:**
   ```bash
   cp .env.example .env
   ```

3. **Install Dependencies:**
   ```bash
   pip install .[dev]
   ```

4. **Run Application:**
   ```bash
   uvicorn src.main:app --reload
   ```
