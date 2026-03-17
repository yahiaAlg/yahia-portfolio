# Yahia Lakhfif — Portfolio Web App

Django 4.2 · Bootstrap 5 · Lucide Icons · WhiteNoise

## Quick Start

### Windows (PowerShell)
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\launch.ps1 setup
.\launch.ps1 run
```

### Linux / macOS
```
chmod +x launch.sh
./launch.sh setup
./launch.sh run
```

Visit: http://127.0.0.1:8000
Admin: http://127.0.0.1:8000/admin

## Commands
| Command | Description |
|---|---|
| setup | Create venv, install deps, migrate, seed, create superuser |
| run | Start dev server |
| migrate | makemigrations + migrate |
| seed | Re-run seed_portfolio |
| collect | collectstatic for production |
| shell | Django shell |

## Models (pages app)
- **Project** — title, slug, category, client, description, tech_stack, image, live_url, github_url, featured, order
- **SkillCategory** + **Skill** — grouped skills with Lucide icon names
- **Experience** — work / teaching / education timeline
- **Certification** — awards and certificates

## Adding Project Images
Admin → Projects → upload image. Recommended: 1200×700px WebP/JPG.

## Lucide Icons Reference
https://lucide.dev/icons/
Examples: code-2, monitor, brain, database, git-branch, award, pen-tool

## Production
1. Set DEBUG=False and SECRET_KEY in .env
2. python manage.py collectstatic
3. gunicorn portfolio.wsgi:application --bind 0.0.0.0:8000 --workers 3
