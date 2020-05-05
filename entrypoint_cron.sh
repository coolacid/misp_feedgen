#!/bin/bash

# Build a fifo buffer for the cron logs, 777 so anyone can write to it
if [[ ! -p /tmp/cronlog ]]; then
    mkfifo /tmp/cronlog
fi
chmod 777 /tmp/cronlog

cron -f | tail -f /tmp/cronlog
