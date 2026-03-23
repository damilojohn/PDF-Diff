# install.ps1 — Windows installer for pdf-diff
# Run with: powershell -ExecutionPolicy Bypass -File install.ps1

Write-Host "Installing pdf-diff..." -ForegroundColor Cyan

# Install uv if not already present
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv not found. Installing uv..." -ForegroundColor Yellow
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    # Refresh PATH so uv is available in the current session
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "User") + ";" + $env:PATH

    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Write-Host "uv installation failed. Please restart your terminal and re-run this script." -ForegroundColor Red
        exit 1
    }
    Write-Host "uv installed successfully." -ForegroundColor Green
} else {
    Write-Host "uv already installed." -ForegroundColor Green
}

# Install pdf-diff
Write-Host "Installing pdf-diff tool..." -ForegroundColor Cyan
uv tool install git+https://github.com/damilojohn/PDF-Diff.git

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "pdf-diff installed successfully!" -ForegroundColor Green
    Write-Host "Usage: pdf-diff doc_a.pdf doc_b.pdf" -ForegroundColor White
} else {
    Write-Host "Installation failed. Please check the error above." -ForegroundColor Red
    exit 1
}
