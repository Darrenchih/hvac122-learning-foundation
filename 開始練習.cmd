@echo off
setlocal
title HVAC-122 Review
if not exist "%~dp0Start.ps1" (
    echo Start.ps1 was not found. Extract the complete ZIP before starting.
    pause
    exit /b 1
)
if not exist "%~dp0app\index.html" (
    echo The app folder was not found. Extract the complete ZIP before starting.
    pause
    exit /b 1
)
echo Starting HVAC-122 Review...
echo Keep this window open while studying. Close it when finished.
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File "%~dp0Start.ps1"
if errorlevel 1 (
    echo.
    echo Could not start. If already running, open http://127.0.0.1:8122/
    echo Otherwise, check the error above.
    pause
    exit /b 1
)
endlocal
