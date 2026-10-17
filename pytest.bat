@echo off
set PYTHONPATH=.
call .venv\Scripts\python -m pytest %*
