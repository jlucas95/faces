__author__ = 'Jan'
from json.decoder import JSONDecoder


class ConfigReader():
    def __init__(self):
        self.file_name = "config/settings.json"

    def _read_file(self):
        file = open(self.file_name)
        content = file.read()
        file.close()
        return content

    def _decode(self, json):
        decoder = JSONDecoder()
        settings = decoder.decode(json)
        return settings

    def read_config(self):
        file = self._read_file()
        settings = self._decode(file)
        return settings





