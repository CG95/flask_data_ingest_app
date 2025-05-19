#!/usr/bin/env sh
set -e

# Wait for Postgres
echo "Waiting for Postgres at postgres:5432…"
until nc -z postgres 5432; do
  sleep 1
done
echo "Postgres is up."

# Wait for Redis
echo "Waiting for Redis at redis:6379…"
until nc -z redis 6379; do
  sleep 1
done
echo "Redis is up."

# Generate sales CSV if missing
if [ ! -f data/sales_data.csv ] && [ ! -f tests/data/sales_data.csv ]; then
  echo "sales_data.csv not found in data/ or tests/data/, generating it now…"
  python data/generate_csv_data.py
else
  echo "sales_data.csv already exists, skipping generation."
fi

# Start the app
echo "Starting Flask app…"
python run.py
