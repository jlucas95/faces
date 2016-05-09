#!/usr/bin/python3.5

from Connector import Connector
from FaceAPI import FaceAPI
from config.config_reader import ConfigReader
from PersonGroup import PersonGroup

settings = ConfigReader().read_config()

try:
    key = settings["api-key"]
except KeyError:
    print("No api-key defined in settings.json!")
    raise


connector = Connector(key)
api = FaceAPI(connector)

