#!/bin/bash

set -e
pwd
# Ensure test database schema is up-to-date

TEST_DB_NAME="test"
TEST_DB_CONN_STRING="dev:dev@postgres:5432"

setup_test_database()
{
    echo "Setting up test database"
    DATABASE_URL="postgresql://$TEST_DB_CONN_STRING"
    psql $DATABASE_URL -c "DROP DATABASE IF EXISTS $TEST_DB_NAME"
    psql $DATABASE_URL -c "CREATE DATABASE $TEST_DB_NAME"
    psql $DATABASE_URL -c "GRANT ALL PRIVILEGES ON DATABASE $TEST_DB_NAME TO dev"
    DATABASE_URL="$DATABASE_URL/$TEST_DB_NAME" ./scripts/migrate.sh
}

setup_test_database
ASYNC_DATABASE_URL=postgresql+asyncpg://$TEST_DB_CONN_STRING/$TEST_DB_NAME uv run pytest src
