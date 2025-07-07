#!/bin/bash

printf "\nRunning pyright...\n"
uv run pyright src

printf "\nRunning ruff check...\n"
uv run ruff check --fix

printf "\nRunning ruff format...\n"
uv run ruff format
