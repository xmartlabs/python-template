#!/bin/bash

if [ -e "${PWD%/*}/docker-compose.yaml" ]; then
    DOCKER_FILES_PATHS="${PWD%/*}"
    SCRIPTS_PATH="."
elif [ -e "${PWD%}/docker-compose.yaml" ]; then
    DOCKER_FILES_PATHS="${PWD%}"
    SCRIPTS_PATH="./scripts"
else
    echo "docker-compose related files not found"
    exit 1
fi

if command -v docker-compose &> /dev/null; then
    DOCKER_COMMAND="docker-compose"
elif command -v docker compose  &> /dev/null; then
    DOCKER_COMMAND="docker compose"
else
    echo "Neither docker-compose nor docker compose are available."
    exit 1
fi


DOCKER_COMPOSE_BASE_FILE_PATH="${DOCKER_FILES_PATHS}/docker-compose.yaml"
TEST_DOCKER_COMPOSE_FILE_PATH="${DOCKER_FILES_PATHS}/docker-compose.test.yaml"
DOCKER_COMPOSE_TEST_FILES="-f $DOCKER_COMPOSE_BASE_FILE_PATH -f $TEST_DOCKER_COMPOSE_FILE_PATH"


case "$1" in
    format)
        $DOCKER_COMMAND run -T backend bash < "${SCRIPTS_PATH}/format.sh"
        ;;
    makemigrations)
        $DOCKER_COMMAND run -T backend bash < "${SCRIPTS_PATH}/makemigrations.sh"
        ;;
    migrate)
        $DOCKER_COMMAND run -T backend bash < "${SCRIPTS_PATH}/migrate.sh"
        ;;
    bash)
        $DOCKER_COMMAND run backend bash
        ;;
    shell)
        $DOCKER_COMMAND run --entrypoint python backend src/helpers/shell.py
        ;;
    test)
        $DOCKER_COMMAND $DOCKER_COMPOSE_TEST_FILES run --rm -T backend bash < "${SCRIPTS_PATH}/test.sh"
        $DOCKER_COMMAND $DOCKER_COMPOSE_TEST_FILES down
        ;;
    *)
        echo "Usage: $0 {format|makemigrations|migrate|bash|shell|test}"
        exit 1
        ;;
esac
