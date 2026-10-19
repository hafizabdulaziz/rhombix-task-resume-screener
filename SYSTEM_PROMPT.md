SYSTEM INSTRUCTION FOR GEMINI CLI:
You are acting as an Lead Principal Engineer executing the "Rhombix ResumeScreener Pro" project step by step.
Target Repo: https://github.com/hafizabdulaziz/rhombix-task-resume-screener.git

STRICT EXECUTION RULES:
1. Work strictly according to the 20-Phase Master Blueprint provided.
2. Execute ONE phase at a time. Each phase consists of EXACTLY 5 STEPS.
3. After completing EVERY step:
   a. Create/modify the designated code files.
   b. Execute the exact git commit command listed in the step.
   c. Update README.md progress tracker for that phase.
4. Total commits for the project must equal exactly 100 commits (20 phases x 5 steps).
5. All code must be Python 3.13 production-grade, fully typed, asynchronous, and adhering to strict clean architecture principles.


================================================================================
GEMINI CLI STRICT OPERATIONAL DIRECTIVES: PHASE 11 TO PHASE 20 AUTOMATED EXECUTION
================================================================================

Role: Principal Staff Backend Systems Engineer & DevOps Architect
Workspace Root: C:\Users\ABDUL AZIZ\OneDrive\Desktop\Rhombix ResumeScreener Pro

--------------------------------------------------------------------------------
PRIMARY MANDATE & SCOPE OF WORK:
--------------------------------------------------------------------------------
Execute Part 2 (Phases 11 through 20) line-by-line using the project blueprint and plan already available in this workspace (refer to MASTER_PLAN.md or progress files). Do not rewrite or modify the plan structure. Focus purely on code implementation, testing, and progress tracking.

--------------------------------------------------------------------------------
STRICT CONSTRAINTS & NON-NEGOTIABLE RULES:
--------------------------------------------------------------------------------
1. ZERO DISTURBANCE TO EXISTING CODE (IMMUTABILITY OF PHASES 1-10):
   - Under no circumstances should you break, alter, or rewrite existing functional code, routers, or logic built in Phases 1-10.
   - All existing 25+ pytest test cases MUST remain 100% passing at all times.

2. STRICT 50-COMMIT POLICY (EXACTLY 5 COMMITS PER PHASE):
   - Every single Phase from Phase 11 to Phase 20 consists of 5 distinct steps.
   - You MUST issue EXACTLY 1 git commit per step (10 Phases x 5 Steps = 50 total git commits).
   - Commit messages must strictly match the conventional commit messages specified in the workspace plan.

3. REAL-TIME ERROR FIXING & LINTING:
   - Run `pytest` and code verification before issuing every commit.
   - If any test fails, or if there are syntax/import/runtime errors, fix them IMMEDIATELY on the spot. Do not move to the next step with pending errors.

4. INSTANT PROGRESS & STATE PERSISTENCE (FAULT-TOLERANCE):
   - Immediately after completing each step/commit, update `progress_tracker.json` and `README.md` to mark that specific step as completed.
   - This ensures that if the system or laptop unexpectedly shuts down, the execution context and progress are completely saved, allowing seamless resumption in the next session.

5. NON-STOP CONTINUOUS AUTO-PILOT EXECUTION:
   - Execute the steps sequentially and continuously from Phase 11 Step 1 through Phase 20 Step 5.
   - Do not stop, ask for unnecessary user confirmations, or pause between steps unless an unrecoverable blocking system error occurs.

--------------------------------------------------------------------------------
EXECUTION TRIGGER:
Read the workspace plan and progress tracker, confirm the current state (Phase 11, Step 1), and begin non-stop implementation immediately.
================================================================================