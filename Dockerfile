# Dockerfile

FROM docker.io/library/python:3.12-slim-bullseye

RUN apt-get update

RUN apt-get install imagemagick -y

RUN apt-get install bc -y

RUN apt-get clean

WORKDIR /motorsort

COPY ./fonts /usr/local/share/fonts

COPY ./app /motorsort

COPY ./config /config

COPY ./media/source_files /mnt/media/source_files

RUN chmod +x ./start_motorsort.sh

CMD ["./start_motorsort.sh"]
