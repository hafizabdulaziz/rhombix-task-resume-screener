@echo off
TITLE Rhombix ResumeScreener Pro - Enterprise Control Panel
COLOR 0A

:MENU
cls
echo ===================================================
echo   RHOMBIX RESUMESCREENER PRO - CONTROL PANEL
echo ===================================================
echo 1. Run All Tests (pytest)
echo 2. Start Application Server (Uvicorn FastAPI)
echo 3. Run Core Requirements Verification Script
echo 4. Exit
echo ===================================================

set /p choice=Enter your choice (1-4): 

if "%choice%"=="1" goto RUN_TESTS
if "%choice%"=="2" goto RUN_SERVER
if "%choice%"=="3" goto RUN_VERIFY
if "%choice%"=="4" goto EXIT

goto MENU

:RUN_TESTS
echo [INFO] Running pytest test suite...
set PYTHONPATH=.
call .venv\Scripts\python -m pytest
pause
goto MENU

:RUN_SERVER
echo [INFO] Starting Rhombix ResumeScreener Pro server at http://127.0.0.1:8000...
set PYTHONPATH=.
call .venv\Scripts\python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
pause
goto MENU

:RUN_VERIFY
echo [INFO] Running core requirements verification script...
set PYTHONPATH=.
call .venv\Scripts\python scripts\verify_core_requirements.py
pause
goto MENU

:EXIT
exit
