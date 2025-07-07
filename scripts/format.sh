#!/bin/bash

printf "\nRunning pyright...\n"
poetry run pyright src

printf "\nRunning ruff check...\n"
poetry run ruff check --fix

printf "\nRunning ruff format...\n"
poetry run ruff format
