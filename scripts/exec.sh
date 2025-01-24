#!/bin/bash

# List of allowed commands
ALLOWED_COMMANDS="format makemigrations migrate bash shell test"

# Container name (adjust if necessary)
CONTAINER="python-template_devcontainer-devcontainer-1"


function dev-exec() {
    docker exec -it \
        --user $USER \
        -w=/opt/app/$PROJECT_NAME \
        $CONTAINER \
        "${COMMAND[@]}"
}

# Check if an argument was passed
if [ $# -eq 0 ]; then
  echo "You must specify a command. Available commands are: $ALLOWED_COMMANDS"
  exit 1
fi

# Check if the command is in the list of allowed commands
if echo "$ALLOWED_COMMANDS" | grep -w -q "$1"; then
  if [[ "$1" == "bash" ]]; then
    COMMAND=("zsh")
  else
    COMMAND=("zsh" "-ic" "$1")
  fi
  dev-exec
else
  echo "Unrecognized command. Available commands are: $ALLOWED_COMMANDS"
  exit 1
fi
