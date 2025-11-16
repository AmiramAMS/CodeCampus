# Script to push CodeCampus to GitHub
Write-Host "=== CodeCampus Git Push Script ===" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $null = git --version 2>&1
    Write-Host "[OK] Git is installed" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/" -ForegroundColor Yellow
    exit 1
}

# Check if we're in a git repository
if (-not (Test-Path .git)) {
    Write-Host "[INFO] Initializing new git repository..." -ForegroundColor Yellow
    git init
}

# Check current branch
$currentBranch = git branch --show-current 2>$null
if (-not $currentBranch) {
    Write-Host "[INFO] No branch found, creating main branch..." -ForegroundColor Yellow
    git checkout -b main 2>$null
    $currentBranch = "main"
} else {
    Write-Host "[INFO] Current branch: $currentBranch" -ForegroundColor Cyan
}

# Check remote
$remoteExists = git remote | Select-String -Pattern "origin"
if (-not $remoteExists) {
    Write-Host "[INFO] Adding remote origin..." -ForegroundColor Yellow
    git remote add origin https://github.com/AmiramAMS/CodeCampus.git
} else {
    Write-Host "[INFO] Remote origin exists" -ForegroundColor Green
    git remote set-url origin https://github.com/AmiramAMS/CodeCampus.git
}

# Fetch to see if remote exists
Write-Host "[INFO] Fetching from remote..." -ForegroundColor Yellow
git fetch origin 2>&1 | Out-Null

# Check if main branch exists on remote
$remoteMainExists = git ls-remote --heads origin main 2>$null
if ($remoteMainExists) {
    Write-Host "[INFO] Remote main branch exists" -ForegroundColor Green
    # Try to merge or rebase
    Write-Host "[INFO] Pulling latest changes..." -ForegroundColor Yellow
    git pull origin main --no-rebase 2>&1 | Out-Null
} else {
    Write-Host "[INFO] No remote main branch found, will create new one" -ForegroundColor Yellow
}

# Add all files
Write-Host "[INFO] Adding all files..." -ForegroundColor Yellow
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "[INFO] Changes detected, committing..." -ForegroundColor Yellow
    $commitMessage = "Update CodeCampus: Modern design, landing page, multi-language support, and code execution improvements"
    git commit -m $commitMessage
    
    Write-Host "[INFO] Pushing to GitHub..." -ForegroundColor Yellow
    git push -u origin $currentBranch
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[SUCCESS] All changes pushed successfully!" -ForegroundColor Green
        Write-Host "View at: https://github.com/AmiramAMS/CodeCampus" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "[ERROR] Push failed. You may need to:" -ForegroundColor Red
        Write-Host "  1. Set up authentication (Personal Access Token)" -ForegroundColor Yellow
        Write-Host "  2. Or use: git push -u origin $currentBranch --force (if you're sure)" -ForegroundColor Yellow
    }
} else {
    Write-Host "[INFO] No changes to commit" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan
