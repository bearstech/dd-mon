import diamond.collector
from ddmon import DD


class DDCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(DDCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        config = super(DDCollector, self).get_default_config()
        config.update({
            'url': 'http://192.168.11.1',
            'user': 'admin',
            'password': 'password'
        })
        return config

    def collect(self):
        dd = DD(self.config['url'], self.config['user'], self.config['password'])
        dd.refresh('Status_Wireless')
        for mac, values in dd.wireless_clients():
            self.publish("ddwrt.wireless.client.%s.quality" % mac, values['quality'])
