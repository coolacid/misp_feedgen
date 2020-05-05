FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
            cron \
            rsync \
         && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN mkdir /srv/misp-feedgen
WORKDIR /srv/misp-feedgen
COPY requirements.txt .
RUN pip3 install -r requirements.txt

ADD format /srv/misp-feedgen/format
ADD modifier /srv/misp-feedgen/modifier
ADD lib /srv/misp-feedgen/lib
ADD generate.py /srv/misp-feedgen/
ADD entrypoint_cron.sh /

