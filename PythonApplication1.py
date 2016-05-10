#!/usr/bin/python3.5

from Connector import Connector
from FaceAPI import FaceAPI
from config.config_reader import ConfigReader
from Person import Person
from PersonGroup import PersonGroup

from PIL import Image, ImageDraw

from io import BytesIO

settings = ConfigReader().read_config()
# TODO store some data locally to avoid having to call the API for everything.
# Doing this will avoid being rate-limited
try:
    key = settings["api-key"]
except KeyError:
    print("No api-key defined in settings.json!")
    raise

connector = Connector(key)
api = FaceAPI(connector)


def recognize(image, persongroup_id):
    """
    Opens a file and returns identities
    :param image:
    :return:
    """
    # Detect faces

    faces = api.detect(image)

    face_ids = [face["faceId"] for face in faces]
    # Find known faces

    result = api.identify(face_ids, persongroup_id)

    # Separate known from unknown faces

    unknown_faces = []
    known_faces = []
    for face in result:
        for detected_face in faces:
            if detected_face["faceId"] == face["faceId"]:
                face["faceRectangle"] = detected_face["faceRectangle"]

        if len(face["candidates"]) == 0:
            unknown_faces.append(face)
        else:
            known_faces.append(face)

    return known_faces, unknown_faces

def draw_face_rectangles(image, rectangle):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    x0 = rectangle["left"]
    y0 = rectangle["top"]

    x1 = rectangle["left"] + rectangle["width"]
    y1 = rectangle["top"] + rectangle["height"]

    # Coordinates for the box
    # x0, y0, x1, y1
    xy = [x0, y0, x1, y1]
    draw.rectangle(xy)
    im.show()


if __name__ == "__main__":
    file_name = "images/identify.jpg"
    file = open(file_name, "rb")
    image = file.read()
    file.close()

    group = PersonGroup("testgroup", connector)

    known, uknown = recognize(image, "testgroup")
    print("==== known faces ====")
    for face in known:
        person = group.find_person(face["candidates"][0]["personId"])
        print(person.name)
        print("face_id: {}".format(face["faceId"]))
        print(face["candidates"][0]["confidence"])
    print("==== unknown faces ====")
    for face in uknown:
        print(face["faceId"])
        print(face["faceRectangle"])
        draw_face_rectangles(BytesIO(image), face["faceRectangle"])
