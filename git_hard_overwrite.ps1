# ============================================================
# SCRIPT: git_hard_overwrite.ps1
# PURPOSE: Completely overwrite GitHub repository with
#          current local code (DESTROYS ALL REMOTE HISTORY)
# ============================================================

# -------- CONFIGURATION --------
$RepoUrl = "https://github.com/etaxfilingsinfo/payroll_repository.git"
$TargetBranch = "main"
$CommitMessage = "Hard reset: overwrite repository with current local code"

Write-Host "WARNING: This will COMPLETELY OVERWRITE the GitHub repository." -ForegroundColor Yellow
Write-Host "Press CTRL+C now if this is NOT what you want."
Pause

# -------- STEP 1: Ensure Git Repo --------
if (-not (Test-Path ".git")) {
    Write-Host " This directory is not a Git repository." -ForegroundColor Red
    exit 1
}

# -------- STEP 2: Ensure Remote --------
Write-Host " Verifying remote origin..."
git remote remove origin 2>$null
git remote add origin $RepoUrl

# -------- STEP 3: Create Orphan Branch (No History) --------
Write-Host " Creating orphan branch (history wiped)..."
git checkout --orphan temp-reset

# -------- STEP 4: Remove Everything from Git Index --------
Write-Host "Clearing Git index..."
git rm -rf . 2>$null

# -------- STEP 5: Create .gitignore (SAFE DEFAULTS) --------
Write-Host "Creating .gitignore..."
@"
# Secrets
.env

# Python cache
__pycache__/
*.pyc
*.pyo

# Virtual env
venv/
.env/

# OS / Editor
.vscode/
.DS_Store
Thumbs.db
"@ | Out-File -Encoding utf8 .gitignore

# -------- STEP 6: Add ALL Local Files --------
Write-Host " Adding all local files..."
git add .

# -------- STEP 7: Commit --------
Write-Host "Creating new root commit..."
git commit -m "$CommitMessage"

# -------- STEP 8: Force Push to Main --------
Write-Host " Force pushing to '$TargetBranch'..."
git branch -M $TargetBranch
git push origin $TargetBranch --force

# -------- DONE --------
Write-Host "SUCCESS!" -ForegroundColor Green
Write-Host "GitHub repository has been COMPLETELY overwritten with local code."
Write-Host "Branch: $TargetBranch"
