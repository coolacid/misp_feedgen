#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import logging

class format_misp:
    def __init__(self, config, output_config):
        self.output_dir =  os.path.join(config['output_dir'], output_config['output_dir'])
        self.output_config = output_config

    def generate(self, events, feed_name):
        logging.info("Exporting feed {} using MISP format to {}".format(feed_name, self.output_dir))
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
            if os.path.isfile(os.path.join(self.output_dir, f'{event["Event"]["uuid"]}.json')):
                with open(os.path.join(self.output_dir, f'{event["Event"]["uuid"]}.json'), 'r') as f:
                    try:
                        original = json.load(f)
                    except:
                        original = ""
            else:
                original = ""
            if original != event:
                with open(os.path.join(self.output_dir, f'{event["Event"]["uuid"]}.json'), 'w') as f:
                    json.dump(event, f, indent=2)
            else:
                logging.debug('Event unchanged')
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
            if os.path.isfile(os.path.join(self.output_dir, 'manifest.json')):
                with open(os.path.join(self.output_dir, 'manifest.json'), 'r') as manifestFile:
                    try:
                        original = json.load(manifestFile)
                    except:
                        original = ""
            else:
                original = ""
            if original != manifest:
                with open(os.path.join(self.output_dir, 'manifest.json'), 'w') as manifestFile:
                    json.dump(manifest, manifestFile)
            else:
                logging.debug('Manifest unchanged')
        except Exception as e:
            logging.error('Could not create the manifest file.', exc_info=True)
