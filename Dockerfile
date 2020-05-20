FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
            cron \
            rsync \
            ssh-client \
         && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN mkdir /srv/misp-feedgen
WORKDIR /srv/misp-feedgen
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY format /srv/misp-feedgen/format
COPY modifier /srv/misp-feedgen/modifier
COPY post-run /srv/misp-feedgen/post-run
COPY lib /srv/misp-feedgen/lib
COPY generate.py /srv/misp-feedgen/
COPY entrypoint_cron.sh /

