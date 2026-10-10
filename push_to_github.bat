@echo off
title Push Master 2APD to GitHub
cls
echo ======================================================================
echo    Link Master 2APD Project to GitHub for Render Deployment
echo ======================================================================
echo.
echo 1. Create a new repository at: https://github.com/new
echo 2. Copy the repository URL (e.g. https://github.com/YOUR_USER/repo.git)
echo.
set /p REPO_URL="Paste your GitHub repository URL here: "

if "%REPO_URL%"=="" (
    echo [ERROR] No URL entered. Process cancelled.
    pause
    exit /b
)

echo.
echo [1/3] Setting branch to main...
git branch -M main

echo [2/3] Configuring remote origin...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo [3/3] Uploading project files to GitHub...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo  SUCCESS! Your project is now on GitHub.
    echo  Next: Go to https://dashboard.render.com -> New + -> Web Service
    echo ======================================================================
) else (
    echo.
    echo [NOTE] If GitHub asked for login or rejected the push, please make sure
    echo you are signed in to GitHub in your browser or Git credentials.
)

pause
