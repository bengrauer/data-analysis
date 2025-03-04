FROM python:3.11-slim

# app, input, output directories
RUN mkdir -p /app/ && \
    mkdir -p /data/input && \
    mkdir -p /data/output

WORKDIR /app

# sample data and any local build distributions
COPY ./data/input/ /data/input/
COPY ./dist/ /app/dist/
COPY run_docker_app.py /app/run_docker_app.py

RUN apt-get update && \
    apt-get install -y git --no-install-recommends && \
    alias ll='ls -l'

# Github Args
ARG GITHUB_USER
ARG GITHUB_PAT
ARG GITHUB_BRANCH=main
# local
#ARG PIP_INSTALL_SRC="/app/dist/*.whl"
ARG PIP_INSTALL_SRC="git+https://github.com/bengrauer/data-analysis.git@$GITHUB_BRANCH"

RUN pip install $PIP_INSTALL_SRC
ENV PYTHONPATH="/app/"


# option 1: bash for troubleshooting
# CMD ["/bin/bash"]

# option 2: run by script
CMD ["python", "run_docker_app.py", "/data/input/", "/data/output/"]