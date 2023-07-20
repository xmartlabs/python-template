#!/bin/bash

printf "Runing pycln...\n"
pycln src --exclude __init__.py --all
printf "\nRunning isort...\n"
isort src
printf "\nRunning flake8...\n"
flake8

printf "\nRunning mypy...\n"
mypy src

printf "\nRunning black...\n"
black src --exclude alembic
