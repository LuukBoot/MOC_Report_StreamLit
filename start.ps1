# MOC Report Streamlit App - Quick Start Script
# Run this script in PowerShell to set up and test your app

Write-Host "🔒 MOC Report Streamlit App - Quick Start" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    exit 1
}

# Check if pip is available
try {
    pip --version | Out-Null
    Write-Host "✅ pip is available" -ForegroundColor Green
} catch {
    Write-Host "❌ pip not found. Please ensure pip is installed." -ForegroundColor Red
    exit 1
}

Write-Host "`n📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "`n🔧 Running setup script..." -ForegroundColor Yellow
python setup.py

Write-Host "`n🚀 Starting Streamlit app..." -ForegroundColor Yellow
Write-Host "The app will open in your default browser." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the app when you're done." -ForegroundColor Cyan

Start-Sleep -Seconds 2
streamlit run streamlit_app.py
