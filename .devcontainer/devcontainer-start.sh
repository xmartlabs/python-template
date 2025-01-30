#!/usr/bin/bash

# Run start commads such as poetry install to keep dependecies updates and in sync with your lock file.

set -xeo pipefail

poetry install --no-ansi --no-root
