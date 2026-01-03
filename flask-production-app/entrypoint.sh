#!/bin/bash

# Set Flask App
export FLASK_APP=run.py

# Wait for DB (optional but helpful)
sleep 2

# Run database migrations
echo "Running migrations..."
if ! flask db upgrade; then
    echo "Migrations failed, trying to create tables directly..."
    python -c "from run import app; from app.utils.database import db; with app.app_context(): db.create_all()"
fi

# Start Gunicorn
echo "Starting Gunicorn on port $PORT..."
gunicorn --bind 0.0.0.0:$PORT wsgi:app --workers 2 --timeout 120
