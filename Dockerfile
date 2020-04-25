FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
            cron \
            rsync \
         && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN mkdir /srv/misp-feedgen
WORKDIR /srv/misp-feedgen
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY generate.py /srv/misp-feedgen/
COPY format /srv/misp-feedgen/

