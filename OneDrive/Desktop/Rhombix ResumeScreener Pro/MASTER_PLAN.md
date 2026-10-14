Rhombix ResumeScreener Pro - Master Execution Blueprint
Architecture & UI/UX Standards
Design Theme: Enterprise Cyber-Minimalist Dark Mode (Slate #0f172a, Zinc, Emerald Green #10b981 accents, Deep Glassmorphism).

Backend Framework: FastAPI (Python 3.13) + AsyncEngine + SQLAlchemy 2.0 + PostgreSQL.

Task Engine: Async Background Workers (ARQ / Celery with Redis).

Frontend: Modern Responsive Layout (Tailwind CSS v3 + Inter Font + HTMX / Alpine.js dynamic reactive components).

Part 1: Core Company Requirements (Phases 1 – 10)
Phase 1: Project Initialization & Async Core Architecture
Step 1: Initialize repository structure (src/, tests/, docs/, scripts/) and setup .gitignore, pyproject.toml, and .env.example.
Step 2: Setup FastAPI application factory with CORS middleware, custom exception handlers, and lifetime lifespan events.
Step 3: Implement structured logging (structlog) and centralized environment configuration management via Pydantic Settings.
Step 4: Setup SQLAlchemy 2.0 AsyncEngine, Session local factories, and base database declarative models.
Step 5: Write initial README.md with project vision, tech stack badges, and Phase 1 completion badge.

Phase 2: Database Schema & Migration Engine
Step 1: Define Candidate and Resume database models (Candidate, ResumeFile, ExtractionData).
Step 2: Define Job Description and Match Results database models (JobDescription, MatchResult, SkillScore).
Step 3: Initialize Alembic database migration environment for async PostgreSQL migrations.
Step 4: Generate and execute initial Alembic baseline migration for core tables.
Step 5: Add database seed script (scripts/seed_data.py) for initial test data and update README.md.

Phase 3: Resume File Processing Service (PDF & DOCX)
Step 1: Implement secure multi-format file uploader and validator (mime-type, binary header verification, size limits).
Step 2: Create high-performance PDF text extraction engine using pypdf/pdfplumber.
Step 3: Build DOCX text extraction parser supporting tables, paragraphs, and inline text using python-docx.
Step 4: Develop file storage manager abstraction (Local Storage + Async File I/O handlers).
Step 5: Write unit tests for PDF/DOCX extraction pipelines and update README.md.

Phase 4: Job Description Processing & Keyword Tokenizer
Step 1: Create Job Description ingestion API endpoint (POST /api/v1/jobs/).
Step 2: Build NLP-based keyword tokenizer and stop-word filter using regex and nltk/spaCy.
Step 3: Develop taxonomy categorizer for Hard Skills, Soft Skills, Education level, and Experience years.
Step 4: Implement requirement weight configuration (Skills weight, Experience weight, Keyword overlap).
Step 5: Integrate Job Description CRUD endpoints and document schema in README.md.

Phase 5: Core Candidate Filtering & Matching Scoring Engine
Step 1: Build TF-IDF vectorizer and cosine similarity engine for content matching.
Step 2: Develop deterministic skill-matching algorithm (Exact Match + Synonym Overlap).
Step 3: Implement experience years extraction parser (detecting date ranges and calculated duration).
Step 4: Construct aggregated scoring calculator combining skills, keywords, and experience metrics into a composite 0-100% score.
Step 5: Add automated test suite for scoring matrix accuracy and update README.md.

Phase 6: Candidate Ranking & Shortlisting API
Step 1: Implement Batch Screening execution endpoint (POST /api/v1/screener/rank).
Step 2: Build dynamic filtering API (Filter by score threshold, experience level, skill set).
Step 3: Implement candidate shortlisting status state engine (Pending, Shortlisted, Rejected, On-Hold).
Step 4: Create Candidate ranking detail endpoint returning detailed score breakdown per candidate.
Step 5: Validate candidate ranking pipeline with integration tests and update README.md.

Phase 7: Export Engine (Excel & CSV Detailed Reports)
Step 1: Configure openpyxl / pandas dynamic Excel workbook generator with custom branding styles.
Step 2: Implement candidate ranking list export to multi-sheet Excel report (Summary + Detailed Breakdown).
Step 3: Create lightweight CSV export endpoint for quick data downloads.
Step 4: Add streaming download response handlers for bulk export performance.
Step 5: Write unit tests for export file validation and update README.md.

Phase 8: SMTP Email Notification & Alert Subsystem
Step 1: Setup SMTP email client configuration supporting HTML template rendering (Jinja2).
Step 2: Build "Candidate Shortlisted" branded HTML email notification template.
Step 3: Build "Bulk Candidate Summary Alert" email trigger for HR/Recruiters.
Step 4: Implement background task queue for email dispatch to avoid API blockages.
Step 5: Create mock email server test suite and update README.md.

Phase 9: Base UI & Templating Setup (Cyber-Dark Theme)
Step 1: Setup Jinja2 templates directory with Tailwind CSS layout (base.html, dynamic navigation header, footer).
Step 2: Build Dashboard Homepage with key metrics cards (Total Resumes, Shortlisted, Top Job Posts).
Step 3: Build Job Description Management page (List, Add Job, View Criteria).
Step 4: Implement Drag-and-Drop Batch File Upload UI component with multi-file drag support.
Step 5: Verify full UI layout responsiveness across desktop/mobile views and update README.md.

Phase 10: Requirements Integrity Audit & Core Freeze
Step 1: Conduct full end-to-end integration test of 4 core company requirements.
Step 2: Audit PDF/DOCX multi-file upload, skill matching accuracy, Excel export, and email notification pipelines.
Step 3: Create automated verification script (scripts/verify_core_requirements.py).
Step 4: Write comprehensive API documentation using Swagger/OpenAPI tags and descriptions.
Step 5: Update README.md highlighting 100% Core Requirements Compliance milestone.

Part 2: Next-Level Production-Grade Features (Phases 11 – 20)
Phase 11: Asynchronous Redis Task Queue & Worker Nodes
Step 1: Integrate Redis client and setup ARQ / Celery task distribution engine.
Step 2: Offload resume text parsing and scoring tasks to asynchronous background worker queues.
Step 3: Implement real-time task progress tracker endpoint (GET /api/v1/tasks/{task_id}).
Step 4: Build dead-letter queue (DLQ) retry mechanism for failed file parsing jobs.
Step 5: Update container/environment setup documentation in README.md.

Phase 12: Advanced Semantic Matching & Hybrid AI Scoring
Step 1: Integrate sentence-transformers / Hugging Face embeddings engine for semantic similarity.
Step 2: Build Hybrid Scoring Engine (50% Exact Keyword Match + 50% Semantic Vector Distance).
Step 3: Add Contact Information extraction pipeline (Phone numbers, LinkedIn, GitHub, Email parsing).
Step 4: Implement Education & University Tier ranking algorithm.
Step 5: Benchmarking hybrid scoring speed vs baseline and document results in README.md.

Phase 13: Enterprise JWT Authentication & RBAC System
Step 1: Implement password hashing (bcrypt/argon2) and JWT token generator (Access + Refresh Tokens).
Step 2: Create user registration, login, and refresh token API endpoints.
Step 3: Implement Role-Based Access Control (RBAC) middleware (Admin, Recruiter, Viewer).
Step 4: Build User Profile and Session Management API endpoints.
Step 5: Write authentication test cases and document auth flows in README.md.

Phase 14: Rate Limiting, Security Guardrails & Audit Logging
Step 1: Implement Redis-backed sliding window rate limiter on API endpoints (slowapi).
Step 2: Add File Upload Sanitization against Zip Bomb attacks, Malicious Macros, and SQLi payload filenames.
Step 3: Implement Audit Logging System to record HR actions (Candidate status changes, Export events).
Step 4: Add Security Headers middleware (CSP, HSTS, X-Frame-Options, CORS hardening).
Step 5: Run security vulnerability checks and log findings in README.md.

Phase 15: Reactive Frontend UI Engine (HTMX & Dynamic Filtering)
Step 1: Integrate HTMX & Alpine.js into frontend templates for SPA-like reactive dynamic interactions.
Step 2: Build dynamic Candidate Screening Table with real-time column sorting and Instant Search bar.
Step 3: Create Real-Time Progress Bar for batch resume upload parsing using HTMX polling.
Step 4: Build Candidate Comparison Drawer UI (side-by-side view of candidate resumes).
Step 5: Test UI interactivity and record UI features in README.md.

Phase 16: Analytics Dashboard & Data Visualization Engine
Step 1: Integrate Chart.js / ApexCharts into recruiter analytics dashboard.
Step 2: Build Skill Gap Analysis radar chart comparing required job skills vs applicant pool skills.
Step 3: Create Score Distribution Histogram and Applicant Funnel chart (Uploaded -> Shortlisted -> Hired).
Step 4: Build Analytics Aggregator API (GET /api/v1/analytics/metrics) with cached stats.
Step 5: Update dashboard documentation and charts overview in README.md.

Phase 17: Multi-Tenant Architecture & Workspace Management
Step 1: Enhance database schemas with Tenant/Organization isolation ID fields (Organization, Workspace).
Step 2: Implement multi-tenant data isolation middleware for seamless API query scoping.
Step 3: Build Workspace Switcher UI component for switching between hiring departments.
Step 4: Add Team Collaboration features (Share candidate notes, internal team scoring ratings).
Step 5: Write multi-tenancy test suites and update README.md.

Phase 18: Automated Testing Suite & CI/CD Pipelines
Step 1: Configure pytest, pytest-asyncio, and test database fixture factories (factory_boy).
Step 2: Write full test coverage for API endpoints, auth middleware, and background workers.
Step 3: Configure static code quality checkers (Ruff, Mypy, Black).
Step 4: Build GitHub Actions Workflow (.github/workflows/ci.yml) for automated testing, linting, and building.
Step 5: Add CI status badges to README.md.

Phase 19: Dockerization, Deployment & Infrastructure Strategy
Step 1: Write multi-stage production Dockerfile for FastAPI application.
Step 2: Create docker-compose.yml service orchestration (FastAPI + PostgreSQL + Redis + ARQ Worker).
Step 3: Create deployment setup scripts for cloud environments (Vercel / Render / AWS App Runner).
Step 4: Add production environment healthcheck endpoints (/health, /ready).
Step 5: Document complete local and production setup instructions in README.md.

Phase 20: Final Polish, Architecture Showcase & Production Launch
Step 1: Conduct comprehensive visual and UI polish across all views (dark mode adjustments, loading states).
Step 2: Generate sample data showcase pack with 20 realistic candidate resumes for demonstration.
Step 3: Create interactive CLI setup utility script (python manage.py setup).
Step 4: Write master enterprise-level README.md complete with Architecture Diagrams, Screenshots, API References, and Feature Matrices.
Step 5: Final repository freeze, full git log audit, and 100% completion tag release (v1.0.0).
