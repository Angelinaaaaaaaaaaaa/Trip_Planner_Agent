Param(
    [int]$BackendPort = 5000,
    [int]$FrontendPort = 8080
)

# Change to repository root (where this script resides)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "=== Trip Planner Web App Starter (Windows) ===" -ForegroundColor Cyan

# Ensure dependencies are installed (root requirements covers backend too)
if (Test-Path "$scriptDir\requirements.txt") {
    Write-Host "Installing Python dependencies from requirements.txt..." -ForegroundColor Yellow
    pip install -r "$scriptDir\requirements.txt"
} else {
    Write-Host "requirements.txt not found, skipping install." -ForegroundColor DarkYellow
}

# Export PORT for backend
$env:PORT = "$BackendPort"

# Start backend (Flask) in background
Write-Host "Starting backend API on http://localhost:$BackendPort ..." -ForegroundColor Green
Start-Process -FilePath "python" -ArgumentList "web_app\backend\app.py" -WorkingDirectory $scriptDir -WindowStyle Minimized

# Start frontend (static server) in background
Write-Host "Starting frontend on http://localhost:$FrontendPort ..." -ForegroundColor Green
Start-Process -FilePath "python" -ArgumentList "-m http.server $FrontendPort" -WorkingDirectory "$scriptDir\web_app\frontend\public" -WindowStyle Minimized

# Open browser
Start-Process "http://localhost:$FrontendPort"

Write-Host "\nAll set!" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:$FrontendPort" -ForegroundColor Cyan
Write-Host "Backend : http://localhost:$BackendPort" -ForegroundColor Cyan
