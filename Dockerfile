### Dockerfile

# Container registry labels

LABEL org.opencontainers.image.source=https://github.com/ianhaddock/motorsort

LABEL org.opencontainers.image.description="Organize motorsport videos and create custom poster images."

LABEL org.opencontainers.image.licenses=MIT

# Base image

FROM docker.io/library/python:3.12-slim-bullseye

RUN apt-get update

# Tooling Installs

RUN apt-get install imagemagick -y

RUN apt-get install bc -y

RUN apt-get clean

# Setup environment

WORKDIR /motorsort

COPY ./fonts /usr/local/share/fonts

COPY ./app /motorsort

COPY ./config /config

# Demo content, overwritten when /mnt/media is set as a mount point

COPY ./media/source_files /mnt/media/source_files

# start & stop motorsort

RUN chmod +x ./start_motorsort.sh

CMD ["./start_motorsort.sh"]
