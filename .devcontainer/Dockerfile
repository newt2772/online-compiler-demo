FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

RUN apt-get update && \
    apt-get install -y g++ python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

# For input handling (new dependency)
RUN pip3 install watchdog