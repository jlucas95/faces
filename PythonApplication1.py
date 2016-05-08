#!/usr/bin/python3.5

from Connector import Connector
from FaceAPI import FaceAPI
from config.config_reader import ConfigReader

settings = ConfigReader().read_config()

print(settings)
connector = Connector(settings["api-key"])
api = FaceAPI(connector)


file = open("test.jpg")
face1 = api.detect(file)[0]["faceId"]
file.close()
print(face1)

file = open("test2.jpg")
face2 = api.detect(file)[0]["faceId"]
file.close()

print(face2)

data = api.verify(face1, face2)
print(data)
