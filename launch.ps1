param([string]$Command = "run")

$VENV = ".venv"

# Detect OS — PowerShell runs on Windows, Linux, and macOS
if ($IsWindows -or ($PSVersionTable.PSVersion -eq $null) -or [System.Runtime.InteropServices.RuntimeInformation]::IsOSPlatform([System.Runtime.InteropServices.OSPlatform]::Windows)) {
    $ActivateScript = "$VENV\Scripts\Activate.ps1"
    $PythonExe      = "$VENV\Scripts\python.exe"
    $PipExe         = "$VENV\Scripts\pip.exe"
} else {
    $ActivateScript = "$VENV/bin/Activate.ps1"
    $PythonExe      = "$VENV/bin/python"
    $PipExe         = "$VENV/bin/pip"
}

function Activate-Venv {
    if (Test-Path $ActivateScript) { & $ActivateScript }
}

function Create-Admin {
    Write-Host "👤 Creating admin user (admin / admin123)..." -ForegroundColor Cyan
    & $PythonExe manage.py shell -c @"
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@portfolio.local', 'admin123')
    print('  Superuser created: admin / admin123')
else:
    print('  Superuser already exists, skipping.')
"@
}

switch ($Command) {
    "setup" {
        Write-Host "🔧 Creating virtual environment..." -ForegroundColor Cyan
        python -m venv $VENV
        Activate-Venv
        Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
        & $PipExe install -r requirements.txt
        if (-not (Test-Path ".env")) {
            Copy-Item ".env.example" ".env"
            Write-Host "📋 .env created from .env.example" -ForegroundColor Cyan
        }
        Write-Host "🗄️  Running migrations..." -ForegroundColor Cyan
        & $PythonExe manage.py migrate
        Write-Host "🌱 Seeding portfolio data..." -ForegroundColor Cyan
        & $PythonExe manage.py seed_portfolio
        Create-Admin
        Write-Host "✅ Setup complete! Run .\launch.ps1 run" -ForegroundColor Green
    }
    "run" {
        Activate-Venv
        Write-Host "🚀 Starting dev server at http://127.0.0.1:8000" -ForegroundColor Green
        & $PythonExe manage.py runserver
    }
    "migrate" {
        Activate-Venv
        & $PythonExe manage.py makemigrations
        & $PythonExe manage.py migrate
    }
    "seed"      { Activate-Venv; & $PythonExe manage.py seed_portfolio }
    "collect"   { Activate-Venv; & $PythonExe manage.py collectstatic --noinput }
    "shell"     { Activate-Venv; & $PythonExe manage.py shell }
    "superuser" { Activate-Venv; Create-Admin }
    default     { Write-Host "Usage: .\launch.ps1 [setup|run|migrate|seed|collect|shell|superuser]" -ForegroundColor Yellow }
}
