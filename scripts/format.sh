#!/bin/bash

printf "Runing pycln...\n"
poetry run python -m pycln src --exclude __init__.py --all

printf "\nRunning isort...\n"
poetry run python -m isort src

printf "\nRunning flake8...\n"
poetry run python -m flake8 src

printf "\nRunning mypy...\n"
poetry run python -m mypy src

printf "\nRunning black...\n"
poetry run python -m black src --exclude alembic
