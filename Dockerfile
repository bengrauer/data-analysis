FROM python:3.12-slim

WORKDIR /app

# create app directories w/ package and script.  Create data input/output directories
RUN mkdir -p /app/data_analysis_package/ && \
    mkdir -p /app/data_analysis_script/ && \
    mkdir -p /data/input && \
    mkdir -p /data/output

# copy sample data to data inputs folder
COPY /data/input/* /data/input/

RUN apt-get update && \
    apt-get install -y git --no-install-recommends

# Arguments for github install
ARG GITHUB_USER
ARG GITHUB_PAT
ARG GITHUB_BRANCH=feature/20250126_refactor
#ARG GITHUB_BRANCH=main
#ARG PIP_INSTALL_SRC=/app/dist/data_analysis-2025.1.26-py3-none-any.whl
# Todo: change this to anon after it is public
ARG PIP_INSTALL_SRC="git+https://$GITHUB_USER:$GITHUB_PAT@github.com/bengrauer/data-analysis.git@$GITHUB_BRANCH"


# scenario #1 - Standard pip install w/ python driver script
RUN pip install $PIP_INSTALL_SRC
RUN echo "from data_analysis.analysis import generate_analysis" >> /app/data_analysis_package/run_app.py && \
    echo "generate_analysis.run_analysis_routine(file_or_directory='/data/input/sample_data.csv', output_directory='/data/output/')" >> /app/data_analysis_package/run_app.py

# scneario #2 - Standalone directory install to run as scripts
RUN pip install --target /app/data_analysis_script $PIP_INSTALL_SRC --no-dependencies
ENV PYTHONPATH="${PYTHONPATH}:/app/data_analysis_script/"

RUN alias ll='ls -l'

CMD ["/bin/bash"]

# option #1 - run via package w/ sample driver python script
#CMD ["python", "/app/data_analysis_package/run_app.py"]

# option #2 - run via relative path scripts installed from pip
#CMD ["python", "-m data_analysis --input_file_dir /data/input/sample_data.csv --output_dir /data/output/"]