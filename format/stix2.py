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
        filelist = []
        logging.info("Exporting feed {} using STIX format to {}".format(feed_name, self.directory))
        for event in events:
            e_feed = event.to_feed(with_meta=True)
            self.parser.parse_misp_event(event)
            data = self.parser.bundle.serialize()

            manifest[self.parser.bundle['id']] = list(e_feed['Event'].pop('_manifest').values())[0]
            manifest[self.parser.bundle['id']]['hash'] = hashlib.sha256(data.encode()).hexdigest()

            filename = os.path.join(self.directory, self.parser.bundle['id'] + '.json')
            filelist.append(self.parser.bundle['id'] + '.json')
            with open(filename, 'w', newline='') as outputfile:
                outputfile.write(data)
            filename = os.path.join(self.directory, 'manifest.json')
            with open(filename, 'w', newline='') as outputfile:
                outputfile.write(json.dumps(manifest))

        filelist.append('manifest.json')
        json_files = [pos_json for pos_json in os.listdir(self.directory) if pos_json.endswith('.json')]
        for todelete in list(set(json_files) - set(filelist)):
            logging.info("Removing old file: {}".format(todelete))
            os.remove(os.path.join(self.directory, todelete))