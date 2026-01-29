# Prüfen, ob der UI-UX-Pro CLI installiert ist
if (!(Get-Command uipro -ErrorAction SilentlyContinue)) {
    Write-Host "📦 UI-UX-Pro CLI wird installiert..." -ForegroundColor Cyan
    npm install -g uipro-cli
}
else {
    Write-Host "✅ UI-UX-Pro CLI ist bereits installiert." -ForegroundColor Green
}

# Initialisierung für Antigravity
Write-Host "🚀 Initialisiere Design-Intelligenz für Antigravity..." -ForegroundColor Cyan
uipro init --ai antigravity

Write-Host "✨ Fertig! Antigravity ist nun bereit für professionelles UI/UX." -ForegroundColor Gold