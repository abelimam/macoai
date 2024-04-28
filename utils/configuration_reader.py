import json


class ConfigurationReader:
    """Class to read a configuration file"""
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.data = json.load(f)

    def get(self, key):
        if not key in self.data:
            return None
        return self.data[key]
