#!/bin/bash

cd src
poetry run alembic revision --autogenerate
