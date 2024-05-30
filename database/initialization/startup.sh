#!/bin/bash
set -e

# Start PostgreSQL in the background
docker-entrypoint.sh postgres &

echo "Waiting for PostgreSQL to start..."
sleep 5  # Giving time for Postgres to start

# Wait for the PostgreSQL server to become available
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "localhost" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is still unavailable - sleeping"
  sleep 5  # Giving time for Postgres to start
done

# Run the initialization script
echo "Postgres is up - executing command"
PGPASSWORD=$POSTGRES_PASSWORD psql -h "localhost" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -a -f /var/lib/postgresql/initialization/init-db.sql

# Do not terminate the PostgreSQL process
wait $!