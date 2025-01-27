#!/bin/bash

# script takes one argument: build, run, delete
# requires os env vars "$GITHUB_USER" and "$GITHUB_PAT" set before hand

operation_arg=$1
echo "Operation Input: $operation_arg"

set -e

# Set commands
BUILD_COMMAND="docker build -t data-analysis -f Dockerfile . \
  --build-arg GITHUB_USER=$GITHUB_USER \
  --build-arg GITHUB_PAT=$GITHUB_PAT"
RUN_COMMAND="docker run -it --name data-analysis --net=host data-analysis"
DELETE_CONTAINER_COMMAND="docker container rm data-analysis"
DELETE_IMAGE_COMMAND="docker image rm data-analysis"

# no parameter - build, run and delete all in sequence
if [ -z $operation_arg ]; then
  cd ..
  eval "$BUILD_COMMAND"
  eval "$RUN_COMMAND"
  eval "$DELETE_CONTAINER_COMMAND"
  eval "$DELETE_IMAGE_COMMAND"  
fi

# singular options
if [ $operation_arg = "build" ]; then
  cd ..
  eval "$BUILD_COMMAND"
elif [ $operation_arg = "run" ]; then
  eval "$RUN_COMMAND"
elif [ $operation_arg = "delete" ]; then
  eval "$DELETE_CONTAINER_COMMAND"
  eval "$DELETE_IMAGE_COMMAND"
else
  echo "Invalid operation: $operation_arg"
  exit 1
fi


