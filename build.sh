#!/usr/bin/env bash
set -o errexit
set -o pipefail

pip install -r requirements.txt gunicorn

python manage.py migrate

python manage.py collectstatic --no-input --clear

# Only seed if DB is fresh (no projects exist yet)
python manage.py shell -c "
from pages.models import Project
if not Project.objects.exists():
    from django.core.management import call_command
    call_command('seed_portfolio')
    print('Seeded.')
else:
    print('DB already seeded, skipping.')
"

# Same guard for superuser
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@portfolio.local', 'admin123')
    print('Superuser created.')
"

echo "Build completed successfully!"