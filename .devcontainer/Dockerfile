# Use an official Ubuntu-based dev container
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Install C++ compiler (g++) and Python
RUN apt-get update && \
    apt-get install -y g++ python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*