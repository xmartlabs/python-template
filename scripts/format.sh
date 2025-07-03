#!/bin/bash

printf "\nRunning mypy...\n"
uv run python -m mypy src

printf "\nRunning ruff check...\n"
ruff check --fix

printf "\nRunning ruff format...\n"
ruff format
