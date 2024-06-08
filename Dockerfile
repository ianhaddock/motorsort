# Dockerfile

FROM docker.io/library/python:3.12-slim-bullseye

RUN apt-get update && apt-get install imagemagick -y

RUN apt-get install bc -y

RUN apt-get clean

WORKDIR /racefiles

COPY ./app /racefiles

RUN chmod +x ./start_racefiles.sh

CMD ["./start_racefiles.sh"]
