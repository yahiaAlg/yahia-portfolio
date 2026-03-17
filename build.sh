#!/usr/bin/env bash
# Build script for Render.com deployment of Django project

set -o errexit
set -o pipefail


# Install Python dependencies
pip install -r requirements.txt

# Install gunicorn if not in requirements.txt (common for Render)
pip install gunicorn

# Run Django database migrations
python manage.py migrate

# Collect static files for production
python manage.py collectstatic --no-input --clear

echo "Build completed successfully!"

