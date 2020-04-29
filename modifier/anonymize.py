
from pymisp.mispevent import MISPOrganisation

class modifier_anonymize:
    def __init__(self, config, mod_config):
        self.org = MISPOrganisation()
        self.org.name = mod_config['name']
        self.org.uuid = mod_config['uuid']

    def modify(self, events, feed_name):
        for event in events:
            event['Orgc'] = self.org
