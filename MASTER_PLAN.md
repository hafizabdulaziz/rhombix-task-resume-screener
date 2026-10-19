Rhombix ResumeScreener Pro - Master Execution Blueprint
Architecture & UI/UX Standards
Design Theme: Enterprise Cyber-Minimalist Dark Mode (Slate #0f172a, Zinc, Emerald Green #10b981 accents, Deep Glassmorphism).

Backend Framework: FastAPI (Python 3.13) + AsyncEngine + SQLAlchemy 2.0 + PostgreSQL.

Task Engine: Async Background Workers (ARQ / Celery with Redis).

Frontend: Modern Responsive Layout (Tailwind CSS v3 + Inter Font + HTMX / Alpine.js dynamic reactive components).

Part 1: Core Company Requirements (Phases 1 – 10)
Phase 1: Project Initialization & Async Core Architecture
Step 1: Initialize repository structure (src/, tests/, docs/, scripts/) and setup .gitignore, pyproject.toml, and .env.example.

Commit: git commit -m "chore: initialize project structure and python dependency configuration"

Step 2: Setup FastAPI application factory with CORS middleware, custom exception handlers, and lifetime lifespan events.

Commit: git commit -m "feat(core): setup fastapi async application factory and global middleware"

Step 3: Implement structured logging (structlog) and centralized environment configuration management via Pydantic Settings.

Commit: git commit -m "feat(config): integrate pydantic-settings and structured logging setup"

Step 4: Setup SQLAlchemy 2.0 AsyncEngine, Session local factories, and base database declarative models.

Commit: git commit -m "feat(database): configure sqlalchemy 2.0 async engine and session management"

Step 5: Write initial README.md with project vision, tech stack badges, and Phase 1 completion badge.

Commit: git commit -m "docs: update readme with project overview and phase 1 completion tracking"

Phase 2: Database Schema & Migration Engine
Step 1: Define Candidate and Resume database models (Candidate, ResumeFile, ExtractionData).

Commit: git commit -m "feat(models): create candidate and resume persistence schemas"

Step 2: Define Job Description and Match Results database models (JobDescription, MatchResult, SkillScore).

Commit: git commit -m "feat(models): create job description and scoring result database models"

Step 3: Initialize Alembic database migration environment for async PostgreSQL migrations.

Commit: git commit -m "chore(migrations): configure alembic async environment and migration scripts"

Step 4: Generate and execute initial Alembic baseline migration for core tables.

Commit: git commit -m "feat(migrations): create and apply initial schema baseline migration"

Step 5: Add database seed script (scripts/seed_data.py) for initial test data and update README.md.

Commit: git commit -m "docs: update readme with database setup guides and migration steps"

Phase 3: Resume File Processing Service (PDF & DOCX)
Step 1: Implement secure multi-format file uploader and validator (mime-type, binary header verification, size limits).

Commit: git commit -m "feat(upload): build file validation service for pdf and docx formats"

Step 2: Create high-performance PDF text extraction engine using pypdf/pdfplumber.

Commit: git commit -m "feat(parser): build async pdf text and metadata extraction service"

Step 3: Build DOCX text extraction parser supporting tables, paragraphs, and inline text using python-docx.

Commit: git commit -m "feat(parser): implement docx document text parser engine"

Step 4: Develop file storage manager abstraction (Local Storage + Async File I/O handlers).

Commit: git commit -m "feat(storage): implement async local file persistence manager"

Step 5: Write unit tests for PDF/DOCX extraction pipelines and update README.md.

Commit: git commit -m "test(parser): add test coverage for file extraction engine and update docs"

Phase 4: Job Description Processing & Keyword Tokenizer
Step 1: Create Job Description ingestion API endpoint (POST /api/v1/jobs/).

Commit: git commit -m "feat(jobs): implement job description creation API endpoint"

Step 2: Build NLP-based keyword tokenizer and stop-word filter using regex and nltk/spaCy.

Commit: git commit -m "feat(nlp): build text normalizer and keyword extraction tokenizer"

Step 3: Develop taxonomy categorizer for Hard Skills, Soft Skills, Education level, and Experience years.

Commit: git commit -m "feat(nlp): implement skills and requirements taxonomy categorizer"

Step 4: Implement requirement weight configuration (Skills weight, Experience weight, Keyword overlap).

Commit: git commit -m "feat(scoring): add configurable weighting matrix for job requirements"

Step 5: Integrate Job Description CRUD endpoints and document schema in README.md.

Commit: git commit -m "docs: document job management API endpoints and phase 4 status"

Phase 5: Core Candidate Filtering & Matching Scoring Engine
Step 1: Build TF-IDF vectorizer and cosine similarity engine for content matching.

Commit: git commit -m "feat(matching): implement tf-idf candidate matching core engine"

Step 2: Develop deterministic skill-matching algorithm (Exact Match + Synonym Overlap).

Commit: git commit -m "feat(matching): build exact and synonym skill matching algorithm"

Step 3: Implement experience years extraction parser (detecting date ranges and calculated duration).

Commit: git commit -m "feat(matching): build candidate experience duration extraction logic"

Step 4: Construct aggregated scoring calculator combining skills, keywords, and experience metrics into a composite 0-100% score.

Commit: git commit -m "feat(scoring): implement composite weighted score engine"

Step 5: Add automated test suite for scoring matrix accuracy and update README.md.

Commit: git commit -m "test(scoring): verify candidate ranker scoring accuracy and update docs"

Phase 6: Candidate Ranking & Shortlisting API
Step 1: Implement Batch Screening execution endpoint (POST /api/v1/screener/rank).

Commit: git commit -m "feat(screener): build batch candidate screening execution API"

Step 2: Build dynamic filtering API (Filter by score threshold, experience level, skill set).

Commit: git commit -m "feat(screener): add dynamic filtering and pagination query params"

Step 3: Implement candidate shortlisting status state engine (Pending, Shortlisted, Rejected, On-Hold).

Commit: git commit -m "feat(screener): build candidate status lifecycle management"

Step 4: Create Candidate ranking detail endpoint returning detailed score breakdown per candidate.

Commit: git commit -m "feat(screener): build candidate detailed score breakdown view endpoint"

Step 5: Validate candidate ranking pipeline with integration tests and update README.md.

Commit: git commit -m "docs: update API specification and phase 6 progress log"

Phase 7: Export Engine (Excel & CSV Detailed Reports)
Step 1: Configure openpyxl / pandas dynamic Excel workbook generator with custom branding styles.

Commit: git commit -m "feat(export): setup formatted excel workbook builder with custom styling"

Step 2: Implement candidate ranking list export to multi-sheet Excel report (Summary + Detailed Breakdown).

Commit: git commit -m "feat(export): build multi-sheet candidate evaluation report generator"

Step 3: Create lightweight CSV export endpoint for quick data downloads.

Commit: git commit -m "feat(export): add csv format candidate summary export endpoint"

Step 4: Add streaming download response handlers for bulk export performance.

Commit: git commit -m "feat(export): implement streaming download responses for large datasets"

Step 5: Write unit tests for export file validation and update README.md.

Commit: git commit -m "test(export): verify excel/csv output integrity and update readme"

Phase 8: SMTP Email Notification & Alert Subsystem
Step 1: Setup SMTP email client configuration supporting HTML template rendering (Jinja2).

Commit: git commit -m "feat(email): setup async smtp client and jinja2 email renderer"

Step 2: Build "Candidate Shortlisted" branded HTML email notification template.

Commit: git commit -m "feat(email): design responsive shortlisted candidate notification template"

Step 3: Build "Bulk Candidate Summary Alert" email trigger for HR/Recruiters.

Commit: git commit -m "feat(email): build hr digest email notification service for batch screening"

Step 4: Implement background task queue for email dispatch to avoid API blockages.

Commit: git commit -m "feat(email): attach email dispatchers to async background workers"

Step 5: Create mock email server test suite and update README.md.

Commit: git commit -m "docs: document email service configuration and phase 8 milestones"

Phase 9: Base UI & Templating Setup (Cyber-Dark Theme)
Step 1: Setup Jinja2 templates directory with Tailwind CSS layout (base.html, dynamic navigation header, footer).

Commit: git commit -m "feat(ui): design enterprise cyber-dark base layout with tailwind css"

Step 2: Build Dashboard Homepage with key metrics cards (Total Resumes, Shortlisted, Top Job Posts).

Commit: git commit -m "feat(ui): implement responsive recruiter dashboard summary view"

Step 3: Build Job Description Management page (List, Add Job, View Criteria).

Commit: git commit -m "feat(ui): build job description management interface"

Step 4: Implement Drag-and-Drop Batch File Upload UI component with multi-file drag support.

Commit: git commit -m "feat(ui): design drag and drop interactive resume upload interface"

Step 5: Verify full UI layout responsiveness across desktop/mobile views and update README.md.

Commit: git commit -m "docs: update UI layout documentation and update phase 9 completion status"

Phase 10: Requirements Integrity Audit & Core Freeze
Step 1: Conduct full end-to-end integration test of 4 core company requirements.

Commit: git commit -m "test(e2e): add end-to-end integration test suite for core flow"

Step 2: Audit PDF/DOCX multi-file upload, skill matching accuracy, Excel export, and email notification pipelines.

Commit: git commit -m "fix(core): apply performance optimizations across core screening pipeline"

Step 3: Create automated verification script (scripts/verify_core_requirements.py).

Commit: git commit -m "chore(scripts): add automated core requirements verification script"

Step 4: Write comprehensive API documentation using Swagger/OpenAPI tags and descriptions.

Commit: git commit -m "docs(openapi): polish swagger api tag annotations and response schemas"

Step 5: Update README.md highlighting 100% Core Requirements Compliance milestone.

Commit: git commit -m "docs: finalize phase 10 milestone mark core requirements 100 percent complete"

Part 2: Next-Level Production-Grade Features (Phases 11 – 20)
Phase 11: Asynchronous Redis Task Queue & Worker Nodes
Step 1: Integrate Redis client and setup ARQ / Celery task distribution engine.

Commit: git commit -m "feat(workers): integrate redis task queue infrastructure"

Step 2: Offload resume text parsing and scoring tasks to asynchronous background worker queues.

Commit: git commit -m "feat(workers): convert batch document parsing into background worker tasks"

Step 3: Implement real-time task progress tracker endpoint (GET /api/v1/tasks/{task_id}).

Commit: git commit -m "feat(workers): add task progress tracking and polling API"

Step 4: Build dead-letter queue (DLQ) retry mechanism for failed file parsing jobs.

Commit: git commit -m "feat(workers): implement resilient task retry and failure handling"

Step 5: Update container/environment setup documentation in README.md.

Commit: git commit -m "docs: update redis worker configuration guide and phase 11 status"

Phase 12: Advanced Semantic Matching & Hybrid AI Scoring
Step 1: Integrate sentence-transformers / Hugging Face embeddings engine for semantic similarity.

Commit: git commit -m "feat(ai): integrate vector embedding generation for semantic search"

Step 2: Build Hybrid Scoring Engine (50% Exact Keyword Match + 50% Semantic Vector Distance).

Commit: git commit -m "feat(ai): construct hybrid keyword and semantic embedding scoring engine"

Step 3: Add Contact Information extraction pipeline (Phone numbers, LinkedIn, GitHub, Email parsing).

Commit: git commit -m "feat(ai): build regex and NLP candidate contact metadata extractor"

Step 4: Implement Education & University Tier ranking algorithm.

Commit: git commit -m "feat(ai): implement education qualification and degree tier parser"

Step 5: Benchmarking hybrid scoring speed vs baseline and document results in README.md.

Commit: git commit -m "docs: add AI vector scoring benchmarks and update phase 12 progress"

Phase 13: Enterprise JWT Authentication & RBAC System
Step 1: Implement password hashing (bcrypt/argon2) and JWT token generator (Access + Refresh Tokens).

Commit: git commit -m "feat(auth): implement jwt token authentication and secure password hashing"

Step 2: Create user registration, login, and refresh token API endpoints.

Commit: git commit -m "feat(auth): create user authorization endpoints and payload schemas"

Step 3: Implement Role-Based Access Control (RBAC) middleware (Admin, Recruiter, Viewer).

Commit: git commit -m "feat(auth): integrate rbac permission checks on critical API routes"

Step 4: Build User Profile and Session Management API endpoints.

Commit: git commit -m "feat(auth): add user profile management and session revocation"

Step 5: Write authentication test cases and document auth flows in README.md.

Commit: git commit -m "docs: document JWT security model and phase 13 authentication milestone"

Phase 14: Rate Limiting, Security Guardrails & Audit Logging
Step 1: Implement Redis-backed sliding window rate limiter on API endpoints (slowapi).

Commit: git commit -m "feat(security): configure redis sliding-window rate limiting on endpoints"

Step 2: Add File Upload Sanitization against Zip Bomb attacks, Malicious Macros, and SQLi payload filenames.

Commit: git commit -m "feat(security): build upload security sanitizer and payload guardrails"

Step 3: Implement Audit Logging System to record HR actions (Candidate status changes, Export events).

Commit: git commit -m "feat(audit): create immutable system activity and audit logging engine"

Step 4: Add Security Headers middleware (CSP, HSTS, X-Frame-Options, CORS hardening).

Commit: git commit -m "feat(security): apply HTTP security header hardening middleware"

Step 5: Run security vulnerability checks and log findings in README.md.

Commit: git commit -m "docs: record security guardrails and update phase 14 completion status"

Phase 15: Reactive Frontend UI Engine (HTMX & Dynamic Filtering)
Step 1: Integrate HTMX & Alpine.js into frontend templates for SPA-like reactive dynamic interactions.

Commit: git commit -m "feat(frontend): integrate htmx and alpine.js for dynamic reactive UI"

Step 2: Build dynamic Candidate Screening Table with real-time column sorting and Instant Search bar.

Commit: git commit -m "feat(frontend): build interactive candidate screening table with instant search"

Step 3: Create Real-Time Progress Bar for batch resume upload parsing using HTMX polling.

Commit: git commit -m "feat(frontend): implement dynamic live parsing progress bar using HTMX polling"

Step 4: Build Candidate Comparison Drawer UI (side-by-side view of candidate resumes).

Commit: git commit -m "feat(frontend): design side-by-side candidate comparison drawer UI"

Step 5: Test UI interactivity and record UI features in README.md.

Commit: git commit -m "docs: update frontend UI layout showcase and phase 15 status"

Phase 16: Analytics Dashboard & Data Visualization Engine
Step 1: Integrate Chart.js / ApexCharts into recruiter analytics dashboard.

Commit: git commit -m "feat(analytics): integrate interactive charting engines into UI dashboard"

Step 2: Build Skill Gap Analysis radar chart comparing required job skills vs applicant pool skills.

Commit: git commit -m "feat(analytics): build candidate skill-gap radar chart visualizer"

Step 3: Create Score Distribution Histogram and Applicant Funnel chart (Uploaded -> Shortlisted -> Hired).

Commit: git commit -m "feat(analytics): create applicant score distribution and conversion funnel charts"

Step 4: Build Analytics Aggregator API (GET /api/v1/analytics/metrics) with cached stats.

Commit: git commit -m "feat(analytics): implement backend aggregated metrics calculator API"

Step 5: Update dashboard documentation and charts overview in README.md.

Commit: git commit -m "docs: document analytics dashboard capability and phase 16 completion"

Phase 17: Multi-Tenant Architecture & Workspace Management
Step 1: Enhance database schemas with Tenant/Organization isolation ID fields (Organization, Workspace).

Commit: git commit -m "feat(multitenancy): add workspace and tenant isolation database schema"

Step 2: Implement multi-tenant data isolation middleware for seamless API query scoping.

Commit: git commit -m "feat(multitenancy): implement organization-level tenant context middleware"

Step 3: Build Workspace Switcher UI component for switching between hiring departments.

Commit: git commit -m "feat(ui): design multi-tenant workspace switcher component"

Step 4: Add Team Collaboration features (Share candidate notes, internal team scoring ratings).

Commit: git commit -m "feat(collaboration): add internal team candidate comments and review ratings"

Step 5: Write multi-tenancy test suites and update README.md.

Commit: git commit -m "docs: document enterprise multi-tenant architecture and phase 17 milestone"

Phase 18: Automated Testing Suite & CI/CD Pipelines
Step 1: Configure pytest, pytest-asyncio, and test database fixture factories (factory_boy).

Commit: git commit -m "test(setup): configure async pytest framework and database test factories"

Step 2: Write full test coverage for API endpoints, auth middleware, and background workers.

Commit: git commit -m "test(api): write comprehensive integration test suite for REST endpoints"

Step 3: Configure static code quality checkers (Ruff, Mypy, Black).

Commit: git commit -m "chore(lint): configure ruff and mypy strict code quality configurations"

Step 4: Build GitHub Actions Workflow (.github/workflows/ci.yml) for automated testing, linting, and building.

Commit: git commit -m "ci: create github actions CI pipeline for automated testing and linting"

Step 5: Add CI status badges to README.md.

Commit: git commit -m "docs: attach CI test workflow badges and update phase 18 status"

Phase 19: Dockerization, Deployment & Infrastructure Strategy
Step 1: Write multi-stage production Dockerfile for FastAPI application.

Commit: git commit -m "build(docker): create multi-stage production dockerfile for fastapi app"

Step 2: Create docker-compose.yml service orchestration (FastAPI + PostgreSQL + Redis + ARQ Worker).

Commit: git commit -m "build(docker): construct docker-compose multi-container orchestration"

Step 3: Create deployment setup scripts for cloud environments (Vercel / Render / AWS App Runner).

Commit: git commit -m "chore(deploy): add production cloud deployment configuration and scripts"

Step 4: Add production environment healthcheck endpoints (/health, /ready).

Commit: git commit -m "feat(monitoring): implement healthcheck and readiness probe API endpoints"

Step 5: Document complete local and production setup instructions in README.md.

Commit: git commit -m "docs: write step-by-step docker and cloud deployment guide"

Phase 20: Final Polish, Architecture Showcase & Production Launch
Step 1: Conduct comprehensive visual and UI polish across all views (dark mode adjustments, loading states).

Commit: git commit -m "style(ui): final dark-mode theme aesthetic polish and UI transition smoothing"

Step 2: Generate sample data showcase pack with 20 realistic candidate resumes for demonstration.

Commit: git commit -m "chore(demo): generate rich sample resumes package for system demonstration"

Step 3: Create interactive CLI setup utility script (python manage.py setup).

Commit: git commit -m "feat(cli): create interactive management CLI script for project orchestration"

Step 4: Write master enterprise-level README.md complete with Architecture Diagrams, Screenshots, API References, and Feature Matrices.

Commit: git commit -m "docs: create production enterprise readme showcase with system architecture"

Step 5: Final repository freeze, full git log audit, and 100% completion tag release (v1.0.0).

Commit: git commit -m "release: tag release v1.0.0 mark production-grade resume screener complete"
