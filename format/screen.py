#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from dotty_dict import dotty
from columnar import columnar

class format_screen:
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
            e_feed = dotty(event.to_feed(with_meta=True))
            data.append([ e_feed[x] for x in self.fields])
        print(columnar(data, self.headers, no_borders=True))