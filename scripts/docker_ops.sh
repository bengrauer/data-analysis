#!/bin/bash

# script takes one argument: build, run, delete, all, help
# maps volume to (project)/data/, which is the code directory

operation_arg=$1
echo "Input Parameter: $operation_arg"

cd ..

set -e

# Set commands
BUILD_COMMAND="docker build --no-cache -t data-analysis -f Dockerfile . \
  --build-arg GITHUB_USER=$GITHUB_USER \
  --build-arg GITHUB_PAT=$GITHUB_PAT"
RUN_COMMAND="docker run -it --name data-analysis --net=host data-analysis"
RUN_COMMAND="docker run --name data-analysis-local --mount type=bind,src=$(pwd)/data/,dst=\"/data/\" data-analysis python run_docker_app.py \"/data/input/\" \"/data/output/\""
DELETE_CONTAINER_COMMAND="docker container rm data-analysis-local"
DELETE_IMAGE_COMMAND="docker image rm data-analysis"

# singular options
if [ -z $operation_arg ] || [ $operation_arg = "help" ]; then
  echo "Possible inputs are 'build', 'run', 'delete', or 'all' to run all commands in sequence."
elif [ $operation_arg = "all" ]; then
  eval "$BUILD_COMMAND"
  eval "$RUN_COMMAND"
  eval "$DELETE_CONTAINER_COMMAND"
  eval "$DELETE_IMAGE_COMMAND"  
elif [ $operation_arg = "build" ]; then

  eval "$BUILD_COMMAND"
elif [ $operation_arg = "run" ]; then
  eval "$RUN_COMMAND"
elif [ $operation_arg = "delete" ]; then
  eval "$DELETE_CONTAINER_COMMAND"
  eval "$DELETE_IMAGE_COMMAND"
else
  echo "Invalid operation: '$operation_arg'.  Possible inputs are 'build', 'run', 'delete', or 'all' to run all commands in sequence."
  exit 1
fi


