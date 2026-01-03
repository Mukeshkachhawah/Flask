#!/bin/bash

# Run database migrations
echo "Running migrations..."
flask db upgrade

# Start Gunicorn
echo "Starting Gunicorn on port $PORT..."
gunicorn --bind 0.0.0.0:$PORT wsgi:app --workers 4 --timeout 120
