#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import yaml
import argparse
import logging
import pymisp
import importlib

class misp_feed:
    def __init__(self, configfile):
        self.load_config(configfile)
        if not self.config['verify_ssl']:
            import urllib3
            urllib3.disable_warnings()
#            logging.warning('InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings')
        try:
            self.misp = pymisp.ExpandedPyMISP(self.config['url'], self.config['key'], self.config['verify_ssl'])
#        except TimeoutError:
#            logging.error("Timeout error connecting to MISP instance")
#            sys.exit(1)
#        except OSError as e:
#            print(e)
        except pymisp.exceptions.PyMISPError as e:
            logging.error(e)
            sys.exit(1)

    def load_config(self, configfile):
        with open(configfile, 'r') as stream:
            try:
                self.config = yaml.safe_load(stream)
                self.feeds = self.config['feeds']
                del self.config['feeds']
            except yaml.YAMLError as exc:
                print(exc)

    def generate_single(self, feed_name):
        for feed in self.feeds:
            if feed['name'] == feed_name:
                self.generate(feed)
                return
        logging.error("Feed {} not found".format(feed_name))

    def generate_all(self):
        for feed in self.feeds:
            self.generate(feed)

    def generate(self, feed):
        logging.info("Processing feed {}".format(feed['name']))
        valid_attribute_distributions = [int(v) for v in feed['valid_attribute_distribution_levels']]
        events = self.processFeed(feed['entries'], feed['filters'], valid_attribute_distributions)
        if len(events) > 0:
            if "modifiers" in feed:
                for modifier in feed['modifiers']:
                    local_class = importlib.import_module("modifier.{}".format(modifier['type']))
                    modifier = getattr(local_class, "modifier_{}".format(modifier['type']))(self.config, modifier)
                    modifier.modify(events, feed['name'])
            for output in feed['outputs']:
                local_class = importlib.import_module("format.{}".format(output['type']))
                formater = getattr(local_class, "format_{}".format(output['type']))(self.config, output)
                formater.generate(events, feed['name'])
            logging.info("Exported {} events from feed: {}.".format(len(events), feed['name']))
            if "hooks" in feed:
                for hook in feed['hooks']:
                    local_class = importlib.import_module("post-run.{}".format(hook['type']))
                    modifier = getattr(local_class, "postrun_{}".format(hook['type']))(self.config, hook, feed['name'])
                    modifier.hook()

    def processFeed(self, entries, filters, valid_attribute_distributions):
        events = []
        try:
            misp_events = self.misp.search(metadata=True, limit=entries, **filters, pythonify=True)
        except Exception:
            logging.error("Invalid response received from MISP.", exc_info=True)
            return []
        if len(misp_events) == 0:
            logging.info("No events returned.")
            return []
        for event in misp_events:
            try:
                e = self.misp.get_event(event.uuid, pythonify=True)
                e_feed = e.to_feed(valid_distributions=valid_attribute_distributions)
            except Exception:
                logging.error(event.uuid, exc_info=True)
                continue
            # We use the to_feed to filter out events without valid distributions
            if e_feed:
                events.append(e)
        return events

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="The configuration file to run")
    parser.add_argument("--debug", help="Debug output", action="store_true")

    # Allow either all, or a list of feeds
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--all", help="Process all feeds", action="store_true")
    group.add_argument("-f", "--feeds", help="Comma list of case sensitive feeds")

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
    else :
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    misp = misp_feed(args.config)
    if args.all:
        misp.generate_all()
    else:
        feeds = args.feeds.split(",")
        for feed in feeds:
            misp.generate_single(feed)
