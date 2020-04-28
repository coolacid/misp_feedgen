
from pymisp.mispevent import MISPOrganisation

class modifier_anonymize:
    def __init__(self, config, mod_config):
        self.org = MISPOrganisation()
        self.org.name = mod_config['name']
        self.org.uuid = mod_config['uuid']
        print(self.org._to_feed())

    def modify(self, events, feed_name):
        for event in events:
            print (event['Orgc']._to_feed())
            event['Orgc'] = self.org
            print (event['Orgc']._to_feed())
