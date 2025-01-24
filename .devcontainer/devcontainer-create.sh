#!/usr/bin/bash

# Run commands to setup the devcontainer when it was just created.

set -xeo pipefail

export HISTFILE_FOLDER=~/.commandhistory
mkdir -p ${HISTFILE_FOLDER}

export HISTFILE="${HISTFILE_FOLDER}/.zsh_history"

SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=${HISTFILE}"
sed -i "1 i\\$SNIPPET" ~/.zshrc

cat .devcontainer/aliases-devcontainer >> ~/.zshrc
