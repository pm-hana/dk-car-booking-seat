@echo off
chcp 65001 >nul
title DK CAR BOOKING SEAT
cd /d "%~dp0"

echo ============================================
echo   DK CAR BOOKING SEAT - Starting server...
echo   Browser will open at http://localhost:8501
echo   (Close this window to stop the app)
echo ============================================
echo.

".venv\Scripts\python.exe" -m streamlit run app.py --server.port=8501 --server.headless=false

echo.
echo Server stopped. Press any key to close.
pause >nul
