#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from lib.base import baseclass

from columnar import columnar
import dotted

class format_screen(baseclass):
    def __init__(self, config, output_config):
        if 'fields' in output_config:
            self.fields = output_config['fields']
        else:
            self.fields = ["Event.date", "Event.uuid", "Event.info"]
        if 'headers' in output_config:
            self.headers = output_config['headers']
        else:
            self.headers = self.fields

    def generate(self, events, feed_name):
        data = []
        logging.info("Exporting feed {} using screen".format(feed_name))
        for event in events:
            e_feed = event.to_feed(with_meta=True)
            data.extend(self.unroll([ dotted.get(e_feed, x) for x in self.fields]))
        print(columnar(data, self.headers, no_borders=True))
