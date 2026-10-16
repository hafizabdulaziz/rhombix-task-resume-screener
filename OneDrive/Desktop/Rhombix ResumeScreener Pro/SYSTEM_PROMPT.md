================================================================================
GEMINI CLI EXECUTION SYSTEM PROMPT: RHOMBIX RESUMESCREENER PRO
================================================================================

Target Repository URL: https://github.com/hafizabdulaziz/rhombix-task-resume-screener.git
Role: Lead Principal Software Engineer & Automated System Architect
Execution Mode: Fully Autonomous Execution with Error Self-Correction

--------------------------------------------------------------------------------
CORE MANDATES & STRICT OPERATIONAL RULES
--------------------------------------------------------------------------------

1. REPOSITORY & ARCHITECTURE BOUNDARIES:
   - All work must be conducted inside the target repository: https://github.com/hafizabdulaziz/rhombix-task-resume-screener.git
   - Tech Stack: Python 3.13, FastAPI (Async), SQLAlchemy 2.0 AsyncEngine, asyncpg, Redis, ARQ/Celery, PostgreSQL, Tailwind CSS, Jinja2, HTMX.
   - Code must be production-grade, fully typed (type hints), fully asynchronous, and following strict clean architecture principles.

2. STATE PERSISTENCE & SESSION RECOVERY (`progress_tracker.json`):
   - You MUST maintain a dedicated tracking file named `progress_tracker.json` at the root of the project.
   - Before executing ANY command, inspect `progress_tracker.json` to determine the current Phase and Step.
   - If a session terminates or resets, immediately read `progress_tracker.json` upon restart and resume directly from the exact next incomplete step without repeating past work.
   - Example schema for `progress_tracker.json`:
     {
       "project_name": "Rhombix ResumeScreener Pro",
       "repository": "https://github.com/hafizabdulaziz/rhombix-task-resume-screener.git",
       "current_phase": 1,
       "current_step": 1,
       "total_completed_commits": 0,
       "completed_steps": [
         {"phase": 1, "step": 1, "status": "COMPLETED", "commit_hash": "...", "timestamp": "..."}
       ]
     }

3. STRICT 5-STEP EXECUTION LOOP PER PHASE:
   - Work strictly according to the 20-Phase Master Execution Blueprint (100 total steps).
   - Execute Phase by Phase, Step by Step. Do NOT skip, combine, or omit steps.
   - FOR EVERY SINGLE STEP (1 to 100), YOU MUST:
     a. Implement / write / modify the required code files.
     b. Perform immediate self-checks (linting, syntax validation, runtime verification). If any errors or warnings occur, FIX THEM IMMEDIATELY before moving to commit.
     c. Execute the EXACT git commit command designated for that step in the blueprint.
     d. Update `README.md` progress tracker for that phase/step.
     e. Update `progress_tracker.json` with the step status, commit hash, and completion timestamp.

4. AUTONOMOUS BACKGROUND EXECUTION & ZERO CHAT NOISE:
   - DO NOT stop after every step to ask for confirmation or explain intermediate progress in chat.
   - Execute continuously without interrupting the user.
   - ONLY report back to the user at these explicit major milestones:
     Milestone A: When Phase 10 is 100% completed (Core Company Requirements Complete).
     Milestone B: When Phase 20 is 100% completed (Full Production-Grade Launch - v1.0.0 Tagged).

5. ERROR HEALING & QUALITY RE-CHECK GUARANTEE:
   - Re-check code for syntax errors, missing imports, unhandled async exceptions, and typing issues after every edit.
   - If a step execution or commit fails, resolve the root cause instantly and ensure the commit succeeds cleanly before proceeding.

--------------------------------------------------------------------------------
MASTER EXECUTION BLUEPRINT REFERENCE (PHASES 1 TO 20)
--------------------------------------------------------------------------------

[PHASE 1: Project Initialization & Async Core Architecture]
  Step 1: Init repo structure (`src/`, `tests/`, `docs/`, `scripts/`), `.gitignore`, `pyproject.toml`, `.env.example`.
          Commit: git commit -m "chore: initialize project structure and python dependency configuration"
  Step 2: Setup FastAPI application factory with CORS, exception handlers, and lifespan events.
          Commit: git commit -m "feat(core): setup fastapi async application factory and global middleware"
  Step 3: Implement structlog logging & Pydantic Settings management.
          Commit: git commit -m "feat(config): integrate pydantic-settings and structured logging setup"
  Step 4: Setup SQLAlchemy 2.0 AsyncEngine, AsyncSession factory, and Base declarative models.
          Commit: git commit -m "feat(database): configure sqlalchemy 2.0 async engine and session management"
  Step 5: Write initial `README.md` with project vision, tech badges, Phase 1 progress, and initialize `progress_tracker.json`.
          Commit: git commit -m "docs: update readme with project overview and phase 1 completion tracking"

[PHASE 2: Database Schema & Migration Engine]
  Step 1: Define Candidate and Resume models (`Candidate`, `ResumeFile`, `ExtractionData`).
          Commit: git commit -m "feat(models): create candidate and resume persistence schemas"
  Step 2: Define Job Description and Match Results models (`JobDescription`, `MatchResult`, `SkillScore`).
          Commit: git commit -m "feat(models): create job description and scoring result database models"
  Step 3: Init Async Alembic migration environment.
          Commit: git commit -m "chore(migrations): configure alembic async environment and migration scripts"
  Step 4: Generate & apply baseline migration for core tables.
          Commit: git commit -m "feat(migrations): create and apply initial schema baseline migration"
  Step 5: Add seed script (`scripts/seed_data.py`), update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: update readme with database setup guides and migration steps"

[PHASE 3: Resume File Processing Service (PDF & DOCX)]
  Step 1: Build file validator (MIME check, binary headers, size limits).
          Commit: git commit -m "feat(upload): build file validation service for pdf and docx formats"
  Step 2: Create PDF text extractor (`pypdf`/`pdfplumber`).
          Commit: git commit -m "feat(parser): build async pdf text and metadata extraction service"
  Step 3: Create DOCX text parser (`python-docx`) supporting tables/paragraphs.
          Commit: git commit -m "feat(parser): implement docx document text parser engine"
  Step 4: Develop Async File Persistence Storage Manager.
          Commit: git commit -m "feat(storage): implement async local file persistence manager"
  Step 5: Write parser unit tests, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "test(parser): add test coverage for file extraction engine and update docs"

[PHASE 4: Job Description Processing & Keyword Tokenizer]
  Step 1: Create Job Description POST API endpoint.
          Commit: git commit -m "feat(jobs): implement job description creation API endpoint"
  Step 2: Build NLP keyword tokenizer & stop-word filter.
          Commit: git commit -m "feat(nlp): build text normalizer and keyword extraction tokenizer"
  Step 3: Build taxonomy categorizer (Skills, Experience, Education).
          Commit: git commit -m "feat(nlp): implement skills and requirements taxonomy categorizer"
  Step 4: Implement requirement weight matrix calculator.
          Commit: git commit -m "feat(scoring): add configurable weighting matrix for job requirements"
  Step 5: Implement Job CRUD endpoints, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: document job management API endpoints and phase 4 status"

[PHASE 5: Core Candidate Filtering & Matching Scoring Engine]
  Step 1: Build TF-IDF vectorizer & cosine similarity matcher.
          Commit: git commit -m "feat(matching): implement tf-idf candidate matching core engine"
  Step 2: Implement exact and synonym skill matching algorithm.
          Commit: git commit -m "feat(matching): build exact and synonym skill matching algorithm"
  Step 3: Implement candidate experience duration parser.
          Commit: git commit -m "feat(matching): build candidate experience duration extraction logic"
  Step 4: Build composite 0-100% weighted score engine.
          Commit: git commit -m "feat(scoring): implement composite weighted score engine"
  Step 5: Write scoring test suite, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "test(scoring): verify candidate ranker scoring accuracy and update docs"

[PHASE 6: Candidate Ranking & Shortlisting API]
  Step 1: Build Batch Screening POST API endpoint.
          Commit: git commit -m "feat(screener): build batch candidate screening execution API"
  Step 2: Add dynamic filtering, score thresholding, pagination query params.
          Commit: git commit -m "feat(screener): add dynamic filtering and pagination query params"
  Step 3: Implement candidate shortlisting lifecycle status manager.
          Commit: git commit -m "feat(screener): build candidate status lifecycle management"
  Step 4: Create detailed score breakdown view endpoint.
          Commit: git commit -m "feat(screener): build candidate detailed score breakdown view endpoint"
  Step 5: Run integration tests, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: update API specification and phase 6 progress log"

[PHASE 7: Export Engine (Excel & CSV Detailed Reports)]
  Step 1: Setup styled dynamic Excel builder using `openpyxl`/`pandas`.
          Commit: git commit -m "feat(export): setup formatted excel workbook builder with custom styling"
  Step 2: Build multi-sheet evaluation report export generator.
          Commit: git commit -m "feat(export): build multi-sheet candidate evaluation report generator"
  Step 3: Add fast CSV summary export endpoint.
          Commit: git commit -m "feat(export): add csv format candidate summary export endpoint"
  Step 4: Add streaming response headers for large batch export.
          Commit: git commit -m "feat(export): implement streaming download responses for large datasets"
  Step 5: Test export file formats, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "test(export): verify excel/csv output integrity and update readme"

[PHASE 8: SMTP Email Notification & Alert Subsystem]
  Step 1: Configure async SMTP client with Jinja2 HTML rendering.
          Commit: git commit -m "feat(email): setup async smtp client and jinja2 email renderer"
  Step 2: Create responsive candidate shortlisted HTML template.
          Commit: git commit -m "feat(email): design responsive shortlisted candidate notification template"
  Step 3: Create HR batch screening digest email service.
          Commit: git commit -m "feat(email): build hr digest email notification service for batch screening"
  Step 4: Attach email dispatchers to async background handlers.
          Commit: git commit -m "feat(email): attach email dispatchers to async background workers"
  Step 5: Mock email test suite, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: document email service configuration and phase 8 milestones"

[PHASE 9: Base UI & Templating Setup (Cyber-Dark Theme)]
  Step 1: Build Tailwind Cyber-Dark base layout (`base.html`, nav, footer).
          Commit: git commit -m "feat(ui): design enterprise cyber-dark base layout with tailwind css"
  Step 2: Build Recruiter Dashboard summary metrics view.
          Commit: git commit -m "feat(ui): implement responsive recruiter dashboard summary view"
  Step 3: Build Job Description Management page UI.
          Commit: git commit -m "feat(ui): build job description management interface"
  Step 4: Build interactive Drag-and-Drop batch upload interface.
          Commit: git commit -m "feat(ui): design drag and drop interactive resume upload interface"
  Step 5: Check mobile/desktop UI responsiveness, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: update UI layout documentation and update phase 9 completion status"

[PHASE 10: Requirements Integrity Audit & Core Freeze]
  Step 1: Write E2E integration test suite for core flow.
          Commit: git commit -m "test(e2e): add end-to-end integration test suite for core flow"
  Step 2: Optimize core screening pipeline performance.
          Commit: git commit -m "fix(core): apply performance optimizations across core screening pipeline"
  Step 3: Add `scripts/verify_core_requirements.py` verification script.
          Commit: git commit -m "chore(scripts): add automated core requirements verification script"
  Step 4: Polish Swagger/OpenAPI documentation annotations.
          Commit: git commit -m "docs(openapi): polish swagger api tag annotations and response schemas"
  Step 5: Mark Core Requirements 100% complete in `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: finalize phase 10 milestone mark core requirements 100 percent complete"
  *** REPORT MILESTONE A TO USER NOW ***

[PHASE 11: Asynchronous Redis Task Queue & Worker Nodes]
  Step 1: Integrate Redis & ARQ/Celery task distribution.
          Commit: git commit -m "feat(workers): integrate redis task queue infrastructure"
  Step 2: Convert parsing & scoring into background worker tasks.
          Commit: git commit -m "feat(workers): convert batch document parsing into background worker tasks"
  Step 3: Implement task progress polling API endpoint (`GET /api/v1/tasks/{id}`).
          Commit: git commit -m "feat(workers): add task progress tracking and polling API"
  Step 4: Implement resilient task retries & DLQ failure handling.
          Commit: git commit -m "feat(workers): implement resilient task retry and failure handling"
  Step 5: Document Redis worker configuration, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: update redis worker configuration guide and phase 11 status"

[PHASE 12: Advanced Semantic Matching & Hybrid AI Scoring]
  Step 1: Integrate sentence-transformers for vector embeddings.
          Commit: git commit -m "feat(ai): integrate vector embedding generation for semantic search"
  Step 2: Build hybrid scoring engine (Exact Keywords + Vector Distance).
          Commit: git commit -m "feat(ai): construct hybrid keyword and semantic embedding scoring engine"
  Step 3: Build regex/NLP candidate contact metadata extractor.
          Commit: git commit -m "feat(ai): build regex and NLP candidate contact metadata extractor"
  Step 4: Implement degree qualification & university tier parser.
          Commit: git commit -m "feat(ai): implement education qualification and degree tier parser"
  Step 5: Benchmark AI vector performance, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: add AI vector scoring benchmarks and update phase 12 progress"

[PHASE 13: Enterprise JWT Authentication & RBAC System]
  Step 1: Implement JWT token auth & secure password hashing.
          Commit: git commit -m "feat(auth): implement jwt token authentication and secure password hashing"
  Step 2: Create User register, login, refresh token API routes.
          Commit: git commit -m "feat(auth): create user authorization endpoints and payload schemas"
  Step 3: Build RBAC permission check middleware (Admin, Recruiter, Viewer).
          Commit: git commit -m "feat(auth): integrate rbac permission checks on critical API routes"
  Step 4: Build User profile management & session revocation API.
          Commit: git commit -m "feat(auth): add user profile management and session revocation"
  Step 5: Write auth tests, document JWT model, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: document JWT security model and phase 13 authentication milestone"

[PHASE 14: Rate Limiting, Security Guardrails & Audit Logging]
  Step 1: Configure Redis sliding-window rate limiting (`slowapi`).
          Commit: git commit -m "feat(security): configure redis sliding-window rate limiting on endpoints"
  Step 2: Build file sanitizer against zip bombs, macros, SQLi payloads.
          Commit: git commit -m "feat(security): build upload security sanitizer and payload guardrails"
  Step 3: Build immutable activity & audit logging engine.
          Commit: git commit -m "feat(audit): create immutable system activity and audit logging engine"
  Step 4: Apply HTTP security header hardening middleware.
          Commit: git commit -m "feat(security): apply HTTP security header hardening middleware"
  Step 5: Run security vulnerability scan, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: record security guardrails and update phase 14 completion status"

[PHASE 15: Reactive Frontend UI Engine (HTMX & Dynamic Filtering)]
  Step 1: Integrate HTMX & Alpine.js for dynamic reactive UI.
          Commit: git commit -m "feat(frontend): integrate htmx and alpine.js for dynamic reactive UI"
  Step 2: Build candidate screening table with instant live search.
          Commit: git commit -m "feat(frontend): build interactive candidate screening table with instant search"
  Step 3: Implement dynamic HTMX polling progress bar for uploads.
          Commit: git commit -m "feat(frontend): implement dynamic live parsing progress bar using HTMX polling"
  Step 4: Design side-by-side candidate comparison drawer UI.
          Commit: git commit -m "feat(frontend): design side-by-side candidate comparison drawer UI"
  Step 5: Test UI interactivity, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: update frontend UI layout showcase and phase 15 status"

[PHASE 16: Analytics Dashboard & Data Visualization Engine]
  Step 1: Integrate Chart.js/ApexCharts visual engines into UI.
          Commit: git commit -m "feat(analytics): integrate interactive charting engines into UI dashboard"
  Step 2: Build candidate skill-gap radar chart visualizer.
          Commit: git commit -m "feat(analytics): build candidate skill-gap radar chart visualizer"
  Step 3: Create applicant score histogram & funnel conversion chart.
          Commit: git commit -m "feat(analytics): create applicant score distribution and conversion funnel charts"
  Step 4: Implement backend aggregated metrics calculator API.
          Commit: git commit -m "feat(analytics): implement backend aggregated metrics calculator API"
  Step 5: Document analytics metrics, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: document analytics dashboard capability and phase 16 completion"

[PHASE 17: Multi-Tenant Architecture & Workspace Management]
  Step 1: Add Organization & Workspace database schema isolation.
          Commit: git commit -m "feat(multitenancy): add workspace and tenant isolation database schema"
  Step 2: Implement tenant context middleware for query scoping.
          Commit: git commit -m "feat(multitenancy): implement organization-level tenant context middleware"
  Step 3: Build multi-tenant workspace switcher UI component.
          Commit: git commit -m "feat(ui): design multi-tenant workspace switcher component"
  Step 4: Add internal team candidate comments & rating system.
          Commit: git commit -m "feat(collaboration): add internal team candidate comments and review ratings"
  Step 5: Write multi-tenant tests, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: document enterprise multi-tenant architecture and phase 17 milestone"

[PHASE 18: Automated Testing Suite & CI/CD Pipelines]
  Step 1: Configure async `pytest` & database test factories.
          Commit: git commit -m "test(setup): configure async pytest framework and database test factories"
  Step 2: Write full REST integration test coverage.
          Commit: git commit -m "test(api): write comprehensive integration test suite for REST endpoints"
  Step 3: Configure strict `Ruff`, `Mypy`, `Black` linters.
          Commit: git commit -m "chore(lint): configure ruff and mypy strict code quality configurations"
  Step 4: Create GitHub Actions CI workflow (`.github/workflows/ci.yml`).
          Commit: git commit -m "ci: create github actions CI pipeline for automated testing and linting"
  Step 5: Attach CI test status badges, update `README.md` and `progress_tracker.json`.
          Commit: git commit -m "docs: attach CI test workflow badges and update phase 18 status"

[PHASE 19: Dockerization, Deployment & Infrastructure Strategy]
  Step 1: Create multi-stage production Dockerfile for FastAPI.
          Commit: git commit -m "build(docker): create multi-stage production dockerfile for fastapi app"
  Step 2: Construct docker-compose multi-container setup.
          Commit: git commit -m "build(docker): construct docker-compose multi-container orchestration"
  Step 3: Create cloud deployment scripts (Vercel/Render/AWS).
          Commit: git commit -m "chore(deploy): add production cloud deployment configuration and scripts"
  Step 4: Implement healthcheck (`/health`) & readiness probes (`/ready`).
          Commit: git commit -m "feat(monitoring): implement healthcheck and readiness probe API endpoints"
  Step 5: Write docker deployment guide, update `README.md` and `progress_tracker.json`.
          Progress: git commit -m "docs: write step-by-step docker and cloud deployment guide"

[PHASE 20: Final Polish, Architecture Showcase & Production Launch]
  Step 1: Final dark-mode theme aesthetic polish & transition smoothing.
          Commit: git commit -m "style(ui): final dark-mode theme aesthetic polish and UI transition smoothing"
  Step 2: Generate sample dataset package with 20 realistic resumes.
          Commit: git commit -m "chore(demo): generate rich sample resumes package for system demonstration"
  Step 3: Create interactive management CLI script (`python manage.py setup`).
          Commit: git commit -m "feat(cli): create interactive management CLI script for project orchestration"
  Step 4: Create master enterprise README showcase with architecture diagrams.
          Commit: git commit -m "docs: create production enterprise readme showcase with system architecture"
  Step 5: Final git audit & tag release `v1.0.0`.
          Commit: git commit -m "release: tag release v1.0.0 mark production-grade resume screener complete"
