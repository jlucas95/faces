__author__ = 'Jan'
from json.decoder import JSONDecoder


class ConfigReader():
    def __init__(self):
        self.file_name = "config/settings.json"

    def _read_file(self):
        try:
            file = open(self.file_name)
        except FileNotFoundError:
            file = self._make_file()
            key = input("enter api key")
            file.write("{{\"api-key\": \"{}\" }}")
            file.close()

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

    def _make_file(self):
        file = open("config/settings", "w")
        return file


