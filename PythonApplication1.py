#!/usr/bin/python3.5

from Connector import Connector
from FaceAPI import FaceAPI
from config.config_reader import ConfigReader

settings = ConfigReader().read_config()

try:
    key = settings["api-key"]
except KeyError:
    print("No api-key defined in settings.json!")
    raise


connector = Connector(key)
api = FaceAPI(connector)

print("Creating persongroup")
group = api.create_persongroup("testgroup", "test_group", "")


print("Creating person Jan")
person = api.create_person("testgroup", "Jan", "")

print("Adding face to Jan")
file = open("images/Jan1.jpg")
face_id = person.add_face(file)
file.close()

file = open("images/Jan2.jpg")
faces = api.detect(file)
file.close()

face_id2 = faces[0]["faceId"]

print(face_id)
print(face_id2)
print("verifying faces")
data = api.verify(face_id, face_id2)

print(data)


"""
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
"""