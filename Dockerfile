FROM ubuntu:22.04

RUN apt -y update
RUN apt -y install python3

ENV TZ Asia/Tokyo
