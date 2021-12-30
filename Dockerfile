FROM ubuntu:21.04

RUN apt-get update && \
    apt-get -y install curl gcc make zlib1g-dev && \
    apt-get -y clean && \
    rm -rf \
      /var/lib/apt/lists/* \
      /usr/share/doc \
      /usr/share/doc-base \
      /usr/share/man \
      /usr/share/locale \
      /usr/share/zoneinfo
WORKDIR /root
RUN curl -o nauty27r3.tar.gz http://users.cecs.anu.edu.au/~bdm/nauty/nauty27r3.tar.gz \
  && tar xzvf nauty27r3.tar.gz \
  && cd nauty27r3 \
  && ./configure && make
ENV NAUTY_HOME=/root/nauty27r3
COPY surge/src/surge.c $NAUTY_HOME
COPY surge/src/Makefile /root
WORKDIR $NAUTY_HOME
RUN ln -s /root/nauty27r3 /root/nauty
RUN make -f ../Makefile clean ; make -f ../Makefile surge

FROM python

RUN apt-get update && \
    apt-get -y install  curl time gnupg zlib1g && \
    apt-get -y clean && \
    rm -rf \
      /var/lib/apt/lists/* \
      /usr/share/doc \
      /usr/share/doc-base \
      /usr/share/man \
      /usr/share/locale \
      /usr/share/zoneinfo
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y

RUN pip install redis
RUN pip install --upgrade google-cloud-storage
RUN pip install --upgrade google-api-python-client
RUN pip install --upgrade oauth2client

COPY --from=0 /root/nauty27r3/surge /usr/bin
      
COPY ./worker.py /worker.py
COPY ./rediswq.py /rediswq.py

CMD  python3 worker.py