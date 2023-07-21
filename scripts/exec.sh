#!/bin/bash

DOCKER_COMPOSE_BASE_FILE_PATH="${PWD%/*}/docker-compose.yaml"
TEST_DOCKER_COMPOSE_FILE_PATH="${PWD%/*}/docker-compose.test.yaml"
DOCKER_COMPOSE_TEST_FILES="-f $DOCKER_COMPOSE_BASE_FILE_PATH -f $TEST_DOCKER_COMPOSE_FILE_PATH"


case "$1" in
    format)
        docker-compose run -T backend bash < format.sh
        ;;
    makemigrations)
        docker-compose run -T backend bash < makemigrations.sh
        ;;
    migrate)
        docker-compose run -T backend bash < migrate.sh
        ;;
    shell)
        docker-compose run backend bash
        ;;
    test)
        docker-compose $DOCKER_COMPOSE_TEST_FILES run --rm -T backend bash < test.sh
        docker-compose $DOCKER_COMPOSE_TEST_FILES down
        ;;
    *)
        echo "Usage: $0 {format|makemigrations|migrate|shell|test}"
        exit 1
        ;;
esac
