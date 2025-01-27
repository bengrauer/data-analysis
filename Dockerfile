FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN mkdir -p /application/data_analysis_package/ && \
    mkdir -p /application/data_analysis_script/

RUN apt-get update && \
    apt-get install -y git --no-install-recommends
#    rm -rf /var/lib/apt/lists/*

ARG GITHUB_USER
ARG GITHUB_PAT

ARG GITHUB_BRANCH=feature/20250126_refactor
#ARG GITHUB_BRANCH=main
#ARG PIP_INSTALL_SRC=/app/dist/data_analysis-2025.1.26-py3-none-any.whl
ARG PIP_INSTALL_SRC="git+https://$GITHUB_USER:$GITHUB_PAT@github.com/bengrauer/data-analysis.git@$GITHUB_BRANCH"


# option #1
# standard pip install into the os environment.  Run a python script calling the package
RUN pip install $PIP_INSTALL_SRC
RUN echo "from data_analysis.analysis import generate_analysis" >> /application/data_analysis_package/run_app.py && \
    echo "generate_analysis.run_analysis_routine('/app/data/sample.csv')" >> /application/data_analysis_package/run_app.py

# option #2
# standalone directory install.  
RUN pip install --target /application/data_analysis_script $PIP_INSTALL_SRC --no-dependencies
ENV PYTHONPATH="${PYTHONPATH}:/application/data_analysis/script_run/"


RUN alias ll='ls -fal'

CMD ["/bin/bash"]

# option #1 - run via package w/ driver python script
#CMD ["python", "/application/data_analysis/package_run/run_app.py"]

# option #2 - run via relative path scripts
#CMD ["python", "-m data_analysis /app/data/sample.csv"]