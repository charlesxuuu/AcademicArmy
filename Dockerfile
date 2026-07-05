FROM ubuntu:24.04

SHELL ["/bin/bash", "-lc"]

RUN apt-get update && apt-get install -y curl ca-certificates git \
    && rm -rf /var/lib/apt/lists/*
