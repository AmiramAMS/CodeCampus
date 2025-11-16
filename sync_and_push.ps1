# Script to sync and push CodeCampus to GitHub
Write-Host "=== CodeCampus Git Sync & Push ===" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $null = git --version 2>&1
    Write-Host "[OK] Git is installed" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git is not installed" -ForegroundColor Red
    exit 1
}

# Check current branch
$currentBranch = git branch --show-current 2>$null
if (-not $currentBranch) {
    Write-Host "[INFO] Creating main branch..." -ForegroundColor Yellow
    git checkout -b main 2>$null
    $currentBranch = "main"
} else {
    Write-Host "[INFO] Current branch: $currentBranch" -ForegroundColor Cyan
}

# Ensure remote is set
$remoteExists = git remote | Select-String -Pattern "origin"
if (-not $remoteExists) {
    Write-Host "[INFO] Adding remote origin..." -ForegroundColor Yellow
    git remote add origin https://github.com/AmiramAMS/CodeCampus.git
} else {
    Write-Host "[INFO] Remote origin exists" -ForegroundColor Green
    git remote set-url origin https://github.com/AmiramAMS/CodeCampus.git
}

# Fetch latest changes
Write-Host "[INFO] Fetching latest changes from remote..." -ForegroundColor Yellow
git fetch origin

# Check if there are remote changes
$localCommit = git rev-parse HEAD 2>$null
$remoteCommit = git rev-parse origin/$currentBranch 2>$null

if ($remoteCommit -and $localCommit -ne $remoteCommit) {
    Write-Host "[INFO] Remote has changes. Pulling and merging..." -ForegroundColor Yellow
    Write-Host "[INFO] This will merge remote changes with local changes" -ForegroundColor Yellow
    
    # Try to pull with merge
    git pull origin $currentBranch --no-rebase
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[WARNING] Pull had conflicts. You may need to resolve them manually." -ForegroundColor Yellow
        Write-Host "[INFO] After resolving conflicts, run:" -ForegroundColor Yellow
        Write-Host "  git add ." -ForegroundColor Cyan
        Write-Host "  git commit -m 'Merge remote changes'" -ForegroundColor Cyan
        Write-Host "  git push -u origin $currentBranch" -ForegroundColor Cyan
        exit 1
    }
    Write-Host "[OK] Successfully merged remote changes" -ForegroundColor Green
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
} else {
    Write-Host "[INFO] No new changes to commit" -ForegroundColor Yellow
}

# Push to GitHub
Write-Host "[INFO] Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin $currentBranch

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[SUCCESS] All changes pushed successfully!" -ForegroundColor Green
    Write-Host "View at: https://github.com/AmiramAMS/CodeCampus" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "[ERROR] Push failed. You may need to:" -ForegroundColor Red
    Write-Host "  1. Resolve any merge conflicts" -ForegroundColor Yellow
    Write-Host "  2. Or use: git push -u origin $currentBranch --force (only if you're sure!)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan

