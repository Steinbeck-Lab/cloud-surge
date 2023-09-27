# Build Surge from source code using Nauty
FROM ubuntu:22.04 as build

ENV NAUTY_HOME=/root/nauty27r3

# Install required packages and cleanup
RUN apt-get update && \
    apt-get -y --no-install-recommends install curl gcc make zlib1g-dev && \
    apt-get -y clean && \
    rm -rf \
      /var/lib/apt/lists/* \
      /usr/share/doc \
      /usr/share/doc-base \
      /usr/share/man \
      /usr/share/locale \
      /usr/share/zoneinfo

# Download the latest nauty release and untar
WORKDIR /root
RUN curl -o nauty27r3.tar.gz http://users.cecs.anu.edu.au/~bdm/nauty/nauty27r3.tar.gz \
  && tar xzvf nauty27r3.tar.gz

# Build nauty
WORKDIR $NAUTY_HOME
RUN ./configure && make
RUN ln -s /root/nauty27r3 /root/nauty

# Copy Surge to nauty folder
COPY surge/src/surge.c $NAUTY_HOME
COPY surge/src/Makefile $NAUTY_HOME

RUN make -f Makefile clean ; make -f Makefile surge

# Install required packages
FROM python:3.11

# Install required packages and cleanup
RUN apt-get update && \
    apt-get -y --no-install-recommends install  curl time gnupg zlib1g && \
    apt-get -y clean && \
    rm -rf \
      /var/lib/apt/lists/* \
      /usr/share/doc \
      /usr/share/doc-base \
      /usr/share/man \
      /usr/share/locale \
      /usr/share/zoneinfo

# Set the SHELL option -o pipefail before RUN with a pipe in
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install Google cloud SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update -y &&  \
    apt-get install google-cloud-sdk -y --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
# Install Google cloud storage, google api python client and oauth2client
RUN pip install --upgrade google-cloud-storage
RUN pip install --upgrade google-api-python-client
RUN pip install --upgrade oauth2client

# Install redis client using pip
RUN pip install redis

# Copy surge binary from build image to usr bin folder
COPY --from=build /root/nauty27r3/surge /usr/bin

# Copy scripts to load/process redis queues, export job statistics
COPY ./worker.py /worker.py
COPY ./rediswq.py /rediswq.py

CMD ["python3", "worker.py"]