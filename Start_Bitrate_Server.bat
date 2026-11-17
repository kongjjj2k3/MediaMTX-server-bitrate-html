@echo off
chcp 65001 >nul
title OBS Bitrate Overlay HTTP Server

REM Change to the folder containing this BAT file
cd /d "%~dp0"

echo ==========================================
echo       OBS Bitrate Overlay HTTP Server
echo ==========================================
echo.
echo Folder: %CD%
echo URL:    http://127.0.0.1:8080/Bitrate.html
echo.
echo Keep this window open while using OBS.
echo Press Ctrl+C to stop the server.
echo.

REM Check that Python is available
where py >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python launcher "py" was not found.
    echo Install Python, or edit this BAT to use "python" instead.
    echo.
    pause
    exit /b 1
)

py -m http.server 8080 --bind 127.0.0.1

echo.
echo HTTP Server has stopped.
pause
