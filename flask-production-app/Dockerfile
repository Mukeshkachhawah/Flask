FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Expose port (Render uses dynamic $PORT)
EXPOSE 10000

# Copy and set permissions for entrypoint script
# Note: we use root temporarily to set permissions
USER root
RUN chmod +x entrypoint.sh
USER appuser

# Environment variable for port (default to 10000)
ENV PORT=10000

# Run entrypoint script
CMD ["./entrypoint.sh"]