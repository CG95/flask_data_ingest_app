# ./Dockerfile
FROM python:3.11-slim

# install netcat-openbsd for healthchecks
RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only what we need and fix permissions
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh


# Copy application code
COPY . .


# Default command is in entrypoint.sh
CMD []
