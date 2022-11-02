FROM python:3.7-slim-buster  as builder

RUN apt-get update && apt-get install -y --no-install-recommends \
                git \
                python3-dev \
                python3-pip \
                python3-wheel \
            && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Build MISP Modules
    RUN mkdir /wheel
    WORKDIR /srv

COPY requirements.txt .
RUN pip3 wheel -r requirements.txt --no-cache-dir -w /wheel/

FROM python:3.7-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
            cron \
            rsync \
            ssh-client \
         && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN mkdir /srv/misp-feedgen
WORKDIR /srv/misp-feedgen
COPY --from=builder /wheel /wheel
RUN pip install /wheel/*.whl

COPY format /srv/misp-feedgen/format
COPY modifier /srv/misp-feedgen/modifier
COPY post-run /srv/misp-feedgen/post-run
COPY lib /srv/misp-feedgen/lib
COPY generate.py /srv/misp-feedgen/
COPY entrypoint_cron.sh /

