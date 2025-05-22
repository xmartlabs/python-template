#!/bin/bash

set -e
pwd
# Ensure test database schema is up-to-date

setup_test_database()
{
    echo "Setting up test database"
    DATABASE_URL=postgresql://dev:dev@postgres:5432
    psql $DATABASE_URL -c 'DROP DATABASE IF EXISTS test'
    psql $DATABASE_URL -c 'CREATE DATABASE test'
    psql $DATABASE_URL -c 'GRANT ALL PRIVILEGES ON DATABASE test TO dev'
    DATABASE_URL="$DATABASE_URL/test" ./scripts/migrate.sh
}

setup_test_database
ASYNC_DATABASE_URL=postgresql+asyncpg://dev:dev@postgres:5432/test poetry run pytest src
