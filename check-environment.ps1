# KI-WERKE Master Preflight Check
# Verifies Project Integrity according to architecture.md and master.md

$projectRoot = Get-Location
Write-Host "🚀 Starting KI-WERKE Master Preflight..." -ForegroundColor Cyan

$checks = @(
    @{ Name = "Path Check (design-system/master.md)"; Path = "design-system/master.md"; Type = "File" },
    @{ Name = "Path Check (design-system/architecture.md)"; Path = "design-system/architecture.md"; Type = "File" },
    @{ Name = "View Engine (plugin/admin-dashboard.php)"; Path = "plugin/admin-dashboard.php"; Type = "File" }
)

$allPassed = $true

# 1. Path & Integrity Checks
foreach ($check in $checks) {
    if (Test-Path $check.Path) {
        Write-Host "[OK] $($check.Name)" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $($check.Name) missing!" -ForegroundColor Red
        $allPassed = $false
    }
}

# 2. Tailwind DNA & Icon Check (Security & Standards)
Write-Host "`n🔍 Analyzing Code Standards..." -ForegroundColor Cyan

$dashboardPath = "plugin/admin-dashboard.php"
if (Test-Path $dashboardPath) {
    $content = Get-Content $dashboardPath
    
    # Tailwind Check
    if ($content -match "tailwindcss.com") {
        Write-Host "[OK] Tailwind DNA detected." -ForegroundColor Green
    } else {
        Write-Host "[WARN] Tailwind CDN missing in dashboard!" -ForegroundColor Yellow
    }

    # Lucide Icon Check
    if ($content -match "data-lucide" -or $content -match "lucide.createIcons") {
        Write-Host "[OK] Lucide-Icon Integration verified." -ForegroundColor Green
    } else {
        Write-Host "[FAIL] No Lucide-Icons found (Violation of architecture.md)!" -ForegroundColor Red
        $allPassed = $false
    }

    # Security Scan (Generic PHP)
    if ($content -match "esc_html__" -and $content -match "defined\('ABSPATH'\)") {
        Write-Host "[OK] Security Standards (Escaping & Path Protection) verified." -ForegroundColor Green
    } else {
        Write-Host "[FAIL] Security risks detected in dashboard!" -ForegroundColor Red
        $allPassed = $false
    }
}

Write-Host "`n==============================================="
if ($allPassed) {
    Write-Host "✅ PREFLIGHT SUCCESSFUL: Module is ready for development." -ForegroundColor Green
} else {
    Write-Host "❌ PREFLIGHT FAILED: Please fix the issues above." -ForegroundColor Red
}
Write-Host "==============================================="
