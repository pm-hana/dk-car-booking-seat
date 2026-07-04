@echo off
REM ===== DK CAR BOOKING 데모 실행 스크립트 =====
REM Korean 경로 + Python 3.14 인코딩 이슈를 자동 처리하고 streamlit 데모를 띄웁니다.
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
".venv\Scripts\python.exe" -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false
pause
