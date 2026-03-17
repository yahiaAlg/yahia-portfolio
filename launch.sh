#!/bin/bash
set -e
COMMAND=${1:-run}
VENV=".venv"
PYTHON=python
# Prefer python3 when it actually works (some Windows environments have a python3 App Execution Alias stub)
if python3 --version >/dev/null 2>&1; then
    PYTHON=python3
fi

# Detect OS for venv activation path
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    ACTIVATE="$VENV/Scripts/activate"
else
    ACTIVATE="$VENV/bin/activate"
fi

activate() { source "$ACTIVATE"; }

create_admin() {
    echo "👤 Creating admin user (admin / admin123)..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@portfolio.local', 'admin123')
    print('  Superuser created: admin / admin123')
else:
    print('  Superuser already exists, skipping.')
"
}

case "$COMMAND" in
  setup)
    echo "🔧 Creating virtual environment..."
    $PYTHON -m venv $VENV
    activate
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    [ ! -f .env ] && cp .env.example .env && echo "📋 .env created from .env.example"
    echo "🗄️  Running migrations..."
    python manage.py migrate
    echo "🌱 Seeding portfolio data..."
    python manage.py seed_portfolio
    create_admin
    echo "✅ Setup complete! Run ./launch.sh run"
    ;;
  run)
    activate
    echo "🚀 Starting dev server at http://127.0.0.1:8000"
    python manage.py runserver
    ;;
  migrate)
    activate
    python manage.py makemigrations
    python manage.py migrate
    ;;
  seed)
    activate
    python manage.py seed_portfolio
    ;;
  collect)
    activate
    python manage.py collectstatic --noinput
    ;;
  shell)
    activate
    python manage.py shell
    ;;
  superuser)
    activate
    create_admin
    ;;
  *)
    echo "Usage: ./launch.sh [setup|run|migrate|seed|collect|shell|superuser]"
    ;;
esac
