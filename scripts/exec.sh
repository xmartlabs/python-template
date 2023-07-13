#!/bin/bash

DOCKER_COMPOSE_FILE_PATH="${PWD%/*}/docker-compose.yaml"
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
esac
