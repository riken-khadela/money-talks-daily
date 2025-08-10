#!/bin/bash
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Copy collected static files to a public directory Vercel can serve
mkdir -p public/static
cp -r staticfiles/* public/static/
