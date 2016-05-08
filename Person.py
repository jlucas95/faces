"""
contains Person class
"""


class Person:
    """A person conatained within an persongroup"""

    def __init__(self, persongroup_id, person_id, face_ids, connector):
        self.persongroup_id = persongroup_id
        self.person_id = person_id
        self.face_ids = face_ids
        self.connection = connector


    def get_face(self, face_id):
        """
        returns the face given a face ID
        """

        url = "persongroups/{}/persons{}/persistedFaces/{}".format(self.persongroup_id,
                                                                   self.person_id,
                                                                   face_id)

        response = self.connection.send_request("GET", url)
        return response

    def  add_face(self, path, is_url, description="", target_face=None):
        """
        adds a face to a person
        """

        if is_url:
            body = self.connection.encode_json({"url":path})
        else:
            file = open(path)
            body = file.read()
            file.close()

            url = "persongroups/{}/persons{}/persistedFaces".format(
                self.persongroup_id,
                self.person_id)

        response = self.connection.send_request("POST",
                                                url,
                                                {"userData":description, "targetFace": target_face},
                                                body=body)
        json = response.read()
        face_id = self.connection.decode_json(json)["persistedFaceId"]
        self.face_ids.append(face_id)

    def delete_face(self):
        """
        removes a face from a person
        """
        raise NotImplementedError

    def update_person(self):
        """
        update person info
        """
        raise NotImplementedError

