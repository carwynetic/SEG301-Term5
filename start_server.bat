@echo off
chcp 65001 > nul
title SEG301 Search Engines Exam Portal Server
echo =====================================================================
echo    🚀 Khởi động Hệ Thống Ôn Thi Search Engines (SEG301)
echo    📍 Địa chỉ: http://localhost:8001
echo =====================================================================
echo.
python "%~dp0server.py"
pause
