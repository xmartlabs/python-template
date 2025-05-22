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
poetry run pytest src
