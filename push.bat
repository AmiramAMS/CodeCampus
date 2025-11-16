@echo off
echo === CodeCampus Git Push ===
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

echo [INFO] Checking git status...
git status

echo.
echo [INFO] Adding all files...
git add .

echo.
echo [INFO] Committing changes...
git commit -m "Update CodeCampus: Modern design, landing page, multi-language support, and code execution improvements"

echo.
echo [INFO] Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo [INFO] Trying to push to current branch...
    for /f "tokens=2" %%b in ('git branch --show-current') do set BRANCH=%%b
    git push -u origin %BRANCH%
)

echo.
echo [SUCCESS] Done!
echo View at: https://github.com/AmiramAMS/CodeCampus
pause

