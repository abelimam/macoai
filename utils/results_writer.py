import json


class ResultsWriter:
    """Class to write results to a json file"""
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def write(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)
