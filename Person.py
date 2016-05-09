"""
contains Person class
"""


class Person:
    """A person contained within an persongroup"""

    def __init__(self, persongroup_id, person, connector):
        self.persongroup_id = persongroup_id
        self.person_id = person["personId"]
        self.face_ids = person["persistedFaceIds"]
        self.connection = connector
        self.description = person["userData"]
        self.name = person["name"]

    def get_face(self, face_id):
        """
        returns the face given a face ID
        """

        url = "persongroups/{}/persons{}/persistedFaces/{}".format(self.persongroup_id,
                                                                   self.person_id,
                                                                   face_id)

        data, response = self.connection.send_request("GET", url)
        return data

    def add_face(self, image, description="", target_face=None):
        """
        adds a face to a person
        """
        try:
            # Tries to read a file-like object.
            image.read
        except AttributeError:
            # Except when the image is a link.
            image = ({"url": image})

        url = "persongroups/{}/persons/{}/persistedFaces".format(
            self.persongroup_id,
            self.person_id)

        headers = {"userdata": description}
        if target_face is not None:
            headers["targetFace"] = target_face

        data, response = self.connection.send_request("POST",
                                                      url,
                                                      headers=headers,
                                                      body=image)
        face_id = data["persistedFaceId"]
        self.face_ids.append(face_id)
        return face_id

    def delete_face(self, face_id):
        """
        removes a face from a person
        """
        url = "persongroups/{}/persons/{}/persistedFaces/{}".format(self.persongroup_id, self.person_id, face_id)

        data, response = self.connection.send_request("DELETE", url)
        if response.status == 200:
            self.face_ids.remove(face_id
                                 )
            return True
        else:
            return False

    def update_person(self, name, description):
        """
        update person info
        """

        url = "persongroups/{}/persons/{}".format(self.persongroup_id, self.person_id)

        body = {"name": name,
                "userData": description}
        data, response = self.connection.send_request("PATCH", url, body=body)

        if response.status == 200:
            return True
        else:
            return False
