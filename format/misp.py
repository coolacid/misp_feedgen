#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import logging

class format_misp:
    def __init__(self, config, feed_config):
#        self.output_dir =  os.path.join(config['output_dir'], feed_config['output_dir'])
        self.output_dir =  config['output_dir'] + feed_config['output_dir']
        self.feed_config = feed_config

    def generate(self, events, feed_name):
        logging.info("Exporting feed {} using MISP format".format(feed_name))
        manifest = {}
        hashes = []
        for event in events:
            e_feed = event.to_feed(with_meta=True)
            hashes += [[h, event.uuid] for h in e_feed['Event'].pop('_hashes')]
            manifest.update(e_feed['Event'].pop('_manifest'))
            self.saveEvent(e_feed)
        self.saveManifest(manifest)
        self.saveHashes(hashes)

    def saveEvent(self, event):
        try:
            with open(os.path.join(self.output_dir, f'{event["Event"]["uuid"]}.json'), 'w') as f:
                json.dump(event, f, indent=2)
        except Exception as e:
            logging.error('Could not create the event dump.', exc_info=True)

    def saveHashes(self, hashes):
        try:
            with open(os.path.join(self.output_dir, 'hashes.csv'), 'w') as hashFile:
                for element in hashes:
                    hashFile.write('{},{}\n'.format(element[0], element[1]))
        except Exception as e:
            logging.error('Could not create the quick hash lookup file.', exc_info=True)

    def saveManifest(self, manifest):
        try:
            with open(os.path.join(self.output_dir, 'manifest.json'), 'w') as manifestFile:
                json.dump(manifest, manifestFile)
        except Exception as e:
            logging.error('Could not create the manifest file.', exc_info=True)
