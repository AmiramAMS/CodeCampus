@echo off
echo === CodeCampus Git Sync ^& Push ===
echo.

echo [INFO] Fetching latest changes...
git fetch origin

echo.
echo [INFO] Pulling and merging remote changes...
git pull origin main --no-rebase

if errorlevel 1 (
    echo.
    echo [WARNING] Pull had conflicts or errors.
    echo [INFO] You may need to resolve conflicts manually.
    echo.
    pause
    exit /b 1
)

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
    echo [ERROR] Push failed.
    echo [INFO] Current branch:
    git branch --show-current
    echo.
    echo [INFO] Try pushing to current branch:
    for /f "tokens=2" %%b in ('git branch --show-current') do git push -u origin %%b
)

echo.
echo [SUCCESS] Done!
echo View at: https://github.com/AmiramAMS/CodeCampus
pause

