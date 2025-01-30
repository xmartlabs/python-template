#!/bin/bash

cd src
poetry run alembic upgrade head
