#!/usr/bin/env bash
# build.sh — Render build script for WPC Map (Django)
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
