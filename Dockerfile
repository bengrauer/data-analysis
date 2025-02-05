FROM python:3.12-slim

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
ARG PIP_INSTALL_SRC="git+https://github.com/bengrauer/data-analysis.git@$GITHUB_BRANCH"

# Pip install packages and install of code to app directory (--target)
RUN pip install $PIP_INSTALL_SRC && \
    pip install --target /app/ $PIP_INSTALL_SRC --no-dependencies
ENV PYTHONPATH="/app/"


# option 1: bash for troubleshooting
# CMD ["/bin/bash"]

# option 2: run by python module
#CMD ["python", "-m", "data_analysis", "--input_file_dir", "/data/input/", "--output_dir", "/data/output/"]

# option 3: run by script
CMD ["python", "run_docker_app.py", "/data/input/", "/data/output/"]