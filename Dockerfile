FROM python:3.12-slim

# create app directories w/ package and script.  Create data input/output directories
RUN mkdir -p /app/ && \
    mkdir -p /data/input && \
    mkdir -p /data/output

WORKDIR /app

# copy sample data to data inputs folder
# /dist/ is for local build/develompent.
COPY ./data/input/ /data/input/
COPY ./dist/ /app/dist/
COPY run_docker_app.py /app/run_docker_app.py

RUN apt-get update && \
    apt-get install -y git --no-install-recommends && \
    alias ll='ls -l'

# Github Args
ARG GITHUB_USER
ARG GITHUB_PAT
ARG GITHUB_BRANCH=feature/20250126_refactor
#ARG GITHUB_BRANCH=main
ARG PIP_INSTALL_SRC=/app/dist/data_analysis-2025.1.26-py3-none-any.whl
# Todo: change this to anon after it is public
#ARG PIP_INSTALL_SRC="git+https://$GITHUB_USER:$GITHUB_PAT@github.com/bengrauer/data-analysis.git@$GITHUB_BRANCH"

# Standard pip install to system
RUN pip install $PIP_INSTALL_SRC
#  Standalone scripts install to directory
RUN pip install --target /app/ $PIP_INSTALL_SRC --no-dependencies
ENV PYTHONPATH="/app/"

# option 1: bash for troubleshooting
# CMD ["/bin/bash"]

# option 2: run by python module
#CMD ["python", "-m", "data_analysis", "--input_file_dir", "/data/input/", "--output_dir", "/data/output/"]

# option 3: run by script
CMD ["python", "run_docker_app.py", "/data/input/", "/data/output/"]