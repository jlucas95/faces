from Person import Person
from PersonGroup import PersonGroup
"""
general face API functions
"""


class FaceAPI:
    """
    contains the general functions of the face API
    """

    def __init__(self, connector):
        self.connector = connector

    def detect(self, image):
        """
        Detects faces in an image or linked image
        Only accepts files or strings.
        Strings are presumed to be a link to an image.
        """
        
        if isinstance(image, str):
            body = {"url":image}
            headers = {"Content-Type": "application/json"}
        else:
            headers = {"Content-Type": "application/octet-stream"}
            try:
                body = image.read()
            except AttributeError as e:
                raise ValueError("image argument must be string or support file like operations")

        faces, response = self.connector.send_request("POST",
                                                      "detect",
                                                      {"returnFaceId":"true"},
                                                      headers=headers,
                                                      body=body)
        return faces

    def identify(self):
        """
        identify unknown faces
        """
        raise NotImplementedError

    def verify(self, face_id1, face_id2):
        """
        verify that 2 faces are the same person
        """
        body = {"faceId1":face_id1, "faceId2":face_id2}

        data, response = self.connector.send_request("POST", "verify", body=body)
        return data

    def create_person(self, persongroup_id, name, description):
        """
        Create new person
        """

        body = {"name": name,
                "userData": description}

        url = "persongroups/{}/persons".format(persongroup_id)
        print(url)
        data, response = self.connector.send_request("PUT",
                                    url,
                                    body=body
                                    )
        print(data)
        person_id = data["personId"]
        return Person(persongroup_id, person_id, [], self.connector)

    def get_persongroups(self):
        """
        Returns a list of persongroups
        """

        # Returns a list of dicts
        group_list, response = self.connector.send_request("GET", "persongroups")
        persongroup_list = []
        for item in group_list:
            group = PersonGroup(item["personGroupId"], self.connector)
            persongroup_list.append(group)
        return persongroup_list

    def create_persongroup(self, identifier, display_name, description):
        """
        create new persongroup
        """
        url = "persongroups/{}".format(identifier)

        body = {"name":display_name,
                "userData": description}


        self.connector.send_request("PUT",
                                    url,
                                    body=body)


        return PersonGroup(identifier, self.connector)

