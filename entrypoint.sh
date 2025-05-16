#!/usr/bin/env sh
set -e

# Wait for Postgres
echo "🔌 Waiting for Postgres at db:5432…"
until nc -z db 5432; do
  sleep 1
done
echo "✅ Postgres is up."

# Wait for Redis
echo "🔌 Waiting for Redis at redis:6379…"
until nc -z redis 6379; do
  sleep 1
done
echo "✅ Redis is up."

# Now run your Flask startup script (run.py)
echo "🚀 Starting Flask app…"
python run.py
