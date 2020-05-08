#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.base import baseclass

import os
import json
import logging
import csv

class format_misp(baseclass):
    def __init__(self, config, output_config):
        self.output_dir =  os.path.join(config['output_dir'], output_config['output_dir'])
        self.output_config = output_config

    def generate(self, events, feed_name):
        logging.info("Exporting feed {} using MISP format to {}".format(feed_name, self.output_dir))
        manifest = {}
        hashes = []
        filelist = []
        for event in events:
            e_feed = event.to_feed(with_meta=True)
            hashes += [[h, event.uuid] for h in e_feed['Event'].pop('_hashes')]
            manifest.update(e_feed['Event'].pop('_manifest'))
            self.saveEvent(e_feed)
            filelist.append(f'{event["uuid"]}.json')
        self.saveManifest(manifest)
        self.saveHashes(hashes)
        filelist.append('manifest.json')
        json_files = [pos_json for pos_json in os.listdir(self.output_dir) if pos_json.endswith('.json')]
        for todelete in list(set(json_files) - set(filelist)):
            logging.info("Removing old file: {}".format(todelete))
            os.remove(os.path.join(self.output_dir, todelete))

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
            if os.path.isfile(os.path.join(self.output_dir, 'hashes.csv')):
                with open(os.path.join(self.output_dir, 'hashes.csv'), 'r') as hashFile:
                    try:
                        original = set(map(tuple,csv.reader(hashFile)))
                    except:
                        original = ""
            else:
                original = ""
            if original != set(map(tuple,hashes)):
                with open(os.path.join(self.output_dir, 'hashes.csv'), 'w') as hashFile:
                    output = csv.writer(hashFile, lineterminator='\n')
                    for element in hashes:
                        output.writerow(element)
            else:
                logging.debug('Hashes unchanged')
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
