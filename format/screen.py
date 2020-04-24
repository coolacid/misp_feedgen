#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from columnar import columnar

class format_screen:
    def __init__(self, config, output_config):
        pass

    def generate(self, events, feed_name):
        headers = ['date', 'uuid', 'info']
        data = []
        logging.info("Exporting feed {} using screen".format(feed_name))
        for event in events:
            e_feed = event.to_feed(with_meta=True)
            data.append([
                    e_feed['Event']['date'], 
                    e_feed['Event']['uuid'],
                    e_feed['Event']['info'],
            ])
        print(columnar(data, headers, no_borders=True))