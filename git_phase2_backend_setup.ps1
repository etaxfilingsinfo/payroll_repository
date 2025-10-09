# SCRIPT: git_final_push.ps1
# Cleans Git history of sensitive files, finalizes Phase 1 on 'main', and sets up Phase 2.

# --- Configuration Variables ---
$RepoUrl = "https://github.com/etaxfilingsinfo/payroll_repository.git"
$MainBranch = "main"
$FeatureBranch = "feature/phasee-2-payroll-api"
$FinalCommitMessage = "feat: complete Phase 1 core modules - Secrets removed"

# --- 1. Verify/Set Remote URL ---
Write-Host "1. Verifying GitHub remote URL..."
# Ensure 'origin' is set. Errors are suppressed if it already exists.
if (-not (git remote -v -ErrorAction SilentlyContinue)) {
    Write-Host "   -> Adding remote 'origin'."
    git remote add origin $RepoUrl
} else {
    Write-Host "   -> Remote 'origin' already exists."
}

# --- 2. Clean Commit History (Fixes the Secret Issue) ---
Write-Host "2. Cleaning Git history of deleted files..."
# Tell Git to remove the deleted files/folders from its index for the next commit.
git rm --cached .env 2>&1 | Out-Null
git rm -r --cached phase1_backup_payroll_system 2>&1 | Out-Null

# Stage all changes (the deletions/untracking)
git add .

# Rewrite the last commit to incorporate the cleanup
Write-Host "   -> Rewriting last commit to be clean of secrets."
git commit --amend -m $FinalCommitMessage

# --- 3. Final Push of Clean History to GitHub ---
Write-Host "3. Pushing clean Phase 1 to 'main' branch (Force Required)..."
# Switch to main and force push the cleaned history.
git checkout $MainBranch 2>&1 | Out-Null
git push -u origin $MainBranch --force

# --- 4. Set Up and Push Phase 2 Feature Branch ---
Write-Host "4. Setting up Phase 2 feature branch..."
# Switch back to the development branch
git checkout $FeatureBranch 2>&1 | Out-Null
# Push the feature branch to remote (initial push, force push just to be safe on history)
git push -u origin $FeatureBranch --force

# --- 5. Post-Cleanup Security: Create and Push .gitignore ---
Write-Host "5. Committing .gitignore and finalising setup..."
# Create/Append to .gitignore (safe to run multiple times)
"
# Secret files ignored
.env
phase1_backup_payroll_system/
" | Out-File -FilePath .gitignore -Append

# Commit the .gitignore file to the feature branch
git add .gitignore
git commit -m "chore: Add .gitignore to exclude secrets"
git push
Write-Host "✅ SCRIPT COMPLETE. Your local branch is now '$FeatureBranch' and Phase 1 is saved."