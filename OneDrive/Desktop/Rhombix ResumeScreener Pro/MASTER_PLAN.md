# Rhombix ResumeScreener Pro - Master Plan

## Architecture Overview
- **Backend:** FastAPI (Async), SQLAlchemy 2.0 (AsyncIOSqlite / AsyncPG), Pydantic v2.
- **Parsing:** PyPDF2 / pdfplumber for PDFs, python-docx for Word documents.
- **Matching & Scoring:** TF-IDF Cosine Similarity + Exact/Synonym Skill Matching + Experience Duration Parser (0-100% composite score).
- **Export:** openpyxl / pandas for styled Excel multi-sheet workbooks and CSV downloads.
- **Notifications:** Async SMTP client with Jinja2 HTML responsive email templates.
- **UI:** Tailwind Cyber-Dark recuiter dashboard & drag-and-drop resume upload.

## Execution Phases (Phases 1 - 10)
- **Phase 1:** Project Initialization & Async Core Architecture (COMPLETED)
- **Phase 2:** Database Schema & Migration Engine
- **Phase 3:** Resume File Processing Service (PDF & DOCX)
- **Phase 4:** Job Description Processing & Keyword Tokenizer
- **Phase 5:** Core Candidate Filtering & Matching Scoring Engine
- **Phase 6:** Candidate Ranking & Shortlisting API
- **Phase 7:** Export Engine (Excel & CSV Detailed Reports)
- **Phase 8:** SMTP Email Notification & Alert Subsystem
- **Phase 9:** Base UI & Templating Setup (Cyber-Dark Theme)
- **Phase 10:** Requirements Integrity Audit & Core Freeze
