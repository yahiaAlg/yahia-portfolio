#!/usr/bin/env bash
# Build script for Render.com deployment of Django project

set -o errexit
set -o pipefail


# Install Python dependencies
pip install -r requirements.txt

# Install gunicorn if not in requirements.txt (common for Render)
pip install gunicorn

# Flush database and reapply migrations (fresh deploy)
# python manage.py flush --no-input
python manage.py migrate

# Collect static files for production
python manage.py collectstatic --no-input --clear

echo "Creating admin superuser..."
python manage.py create_admin

echo "Seeding portfolio data..."
python manage.py seed_portfolio

echo "Build completed successfully!"

