#!/bin/bash

# Set Flask App
export FLASK_APP=run.py

# Run database migrations
echo "Running migrations..."
flask db upgrade

# Start Gunicorn
echo "Starting Gunicorn on port $PORT..."
gunicorn --bind 0.0.0.0:$PORT wsgi:app --workers 2 --timeout 120
