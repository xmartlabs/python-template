#!/usr/bin/bash

# Run start commads such as uv sync to keep dependecies updates and in sync with your lock file.

set -xeo pipefail

uv sync --frozen --no-install-project --all-groups
