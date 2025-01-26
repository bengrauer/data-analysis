FROM python:3.12-slim

WORKDIR /app

#RUN apt-get update && \
#    apt-get install -y git --no-install-recommends && \
#    rm -rf /var/lib/apt/lists/*

ARG GITHUB_REPO
ARG GITHUB_PACKAGE
ARG GITHUB_BRANCH

#RUN git clone --depth 1 -b $GITHUB_BRANCH $GITHUB_REPO /tmp/$GITHUB_PACKAGE
#RUN pip install /tmp/$GITHUB_PACKAGE

#RUN pip install /app/dist/data_analysis-2025.1.26-py3-none-any.whl 

COPY . .

#CMD ["python"]
#CMD ["python", "main.py"]
#ENTRYPOINT ./run_app.sh
CMD ["/bin/bash"]