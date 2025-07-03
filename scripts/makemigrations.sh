#!/bin/bash

cd src
uv run alembic revision --autogenerate
