# Dockerfile

FROM docker.io/library/python:3.12-bullseye

RUN apt-get update && apt-get install imagemagick -y

WORKDIR /racefiles

COPY ./app /racefiles

RUN chmod +x ./start_racefiles.sh

CMD ["./start_racefiles.sh"]
