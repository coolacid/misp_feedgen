#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import json
import hashlib
from lib.base import baseclass

class format_stix2(baseclass):
    def __init__(self, config, output_config):
        if "format" in output_config and output_config['format'] == "20":
            from misp_stix_converter import MISPtoSTIX20Parser
            self.parser = MISPtoSTIX20Parser()
            self.spec_version = '2.0'
        else:
            from misp_stix_converter import MISPtoSTIX21Parser
            self.parser = MISPtoSTIX21Parser()
            self.spec_version = '2.1'
        self.directory = os.path.join(config['output_dir'], output_config['output_dir'])


    def generate(self, events, feed_name):
        manifest = {}
        for event in events:
            e_feed = event.to_feed(with_meta=True)
            self.parser.parse_misp_event(event)
            data = self.parser.bundle.serialize()

            manifest[self.parser.bundle['id']] = list(e_feed['Event'].pop('_manifest').values())[0]
            manifest[self.parser.bundle['id']]['hash'] = hashlib.sha256(data.encode()).hexdigest()

            filename = os.path.join(self.directory, self.parser.bundle['id'] + '.json')
            with open(filename, 'w', newline='') as outputfile:
                outputfile.write(data)
            filename = os.path.join(self.directory, 'manifest.json')
            with open(filename, 'w', newline='') as outputfile:
                outputfile.write(json.dumps(manifest))
