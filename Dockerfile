FROM ubuntu:22.04

RUN apt -y update && \
    apt-get install -y python3-dev python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /work

COPY . /work

RUN pip3 install --no-cache-dir -r requirements.txt
