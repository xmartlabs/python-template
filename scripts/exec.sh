#!/bin/bash

DOCKER_COMPOSE_FILE_PATH="${PWD%/*}/docker-compose.yaml"
TEST_DOCKER_COMPOSE_FILE_PATH="${PWD%/*}/docker-compose-test.yaml"

case "$1" in
    format)
        docker-compose -f $DOCKER_COMPOSE_FILE_PATH run -T backend bash < format.sh
        ;;
    makemigrations)
        docker-compose -f $DOCKER_COMPOSE_FILE_PATH run -T backend bash < makemigrations.sh
        ;;
    migrate)
        docker-compose -f $DOCKER_COMPOSE_FILE_PATH run -T backend bash < migrate.sh
        ;;
    shell)
        docker-compose -f $DOCKER_COMPOSE_FILE_PATH run backend bash
        ;;
    test)
        docker-compose -f $TEST_DOCKER_COMPOSE_FILE_PATH run --rm -T test-backend bash < test.sh
        docker-compose -f $TEST_DOCKER_COMPOSE_FILE_PATH down
        ;;
    *)
        echo "Usage: $0 {format|makemigrations|migrate|shell|test}"
        exit 1
        ;;
esac
