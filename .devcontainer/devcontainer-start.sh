#!/usr/bin/bash


# Run start commads such as poetry install to keep dependecies updates and in sync with your lock file.

set -xeo pipefail

export HISTFILE_FOLDER=~/.commandhistory
mkdir -p ${HISTFILE_FOLDER}

export HISTFILE="${HISTFILE_FOLDER}/.zsh_history"

SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=${HISTFILE}"
grep -qxF "$SNIPPET" ~/.zshrc || sed -i "1 i\\$SNIPPET" ~/.zshrc

poetry install --no-ansi --no-root
