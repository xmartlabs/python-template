#!/bin/bash

printf "\nRunning pyright...\n"
poetry run pyright src

printf "\nRunning ruff check...\n"
ruff check --fix

printf "\nRunning ruff format...\n"
ruff format
