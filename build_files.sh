#!/bin/bash
set -e

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput
