# setup-gh-secrets.ps1
# This script helps set up the necessary secrets for the CI/CD pipeline.
# Usage: ./setup-gh-secrets.ps1
# Prerequisite: gh cli installed and authenticated (gh auth login)

$ErrorActionPreference = "Stop"

Write-Host "Checking GitHub CLI status..." -ForegroundColor Cyan
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI (gh) is not installed or not in PATH."
}

$repo = "kiwerkepro-org/kiw-test-modul"
Write-Host "Target Repo: $repo" -ForegroundColor Cyan

# Check for secrets
$requiredSecrets = @("KIW_SUITE_DISPATCH_TOKEN")

foreach ($secret in $requiredSecrets) {
    Write-Host "Checking secret: $secret ..." -NoNewline
    # Note: gh secret list doesn't show values, just names.
    $exists = gh secret list --repo $repo | Select-String $secret
    
    if ($exists) {
        Write-Host " [FOUND]" -ForegroundColor Green
    } else {
        Write-Host " [MISSING]" -ForegroundColor Red
        Write-Host "Please enter value for $secret:"
        $val = Read-Host -AsSecureString
        $plainVal = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($val))
        
        # Determine if it should be an Org secret or Repo secret.
        # The workflow comment says "Org Secret", but we set it on repo for safety if user is not org admin.
        # Ideally, check if user wants to set it on Org.
        
        Write-Host "Setting $secret on repo $repo..."
        echo $plainVal | gh secret set $secret --repo $repo
        Write-Host "Secret set." -ForegroundColor Green
    }
}

Write-Host "Done. Workflow should now have access to secrets." -ForegroundColor Cyan
