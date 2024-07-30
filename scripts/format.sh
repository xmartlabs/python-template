#!/bin/bash

printf "\nRunning mypy...\n"
mypy src

printf "\nRunning ruff check...\n"
ruff check --fix

printf "\nRunning ruff format...\n"
ruff format
