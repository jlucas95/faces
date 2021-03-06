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
        Detects faces in an images or linked images
        Only accepts files or strings.
        Strings are presumed to be a link to an images.
        """

        if isinstance(image, str):
            image = {"url": image}

        faces, response = self.connector.send_request("POST",
                                                      "detect",
                                                      {"returnFaceId": "true",
                                                      "returnFaceRectangle": "true"},
                                                      body=image)
        return faces

    def identify(self, face_ids, persongroup_id, candidates=1):
        """
        Takes face ids as returned by self.detect and returns possible persons
        Returns a list with dictionaries
        The dicts have the following properties:
        - faceId (str)
        - candidates (List of dicts)
          - personId (str)
          - confidence (float)
        """

        body = {
            "faceIds": face_ids,
            "personGroupId": persongroup_id,
            "maxNumOfCandidatesReturned": candidates
        }

        data, response = self.connector.send_request("POST", "identify", body=body)
        return data

    def verify(self, face_id1, face_id2):
        """
        verify that 2 faces are the same person
        """
        body = {"faceId1": face_id1,
                "faceId2": face_id2}

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
        data, response = self.connector.send_request("POST",
                                                     url,
                                                     body=body
                                                     )
        # This API call only returns the person id
        # So we add the function arguments to the data
        data["name"] = name
        data["userData"] = description
        data["persistedFaceIds"] = []

        return Person(persongroup_id, data, self.connector)

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

        body = {"name": display_name,
                "userData": description}

        self.connector.send_request("PUT",
                                    url,
                                    body=body)
        return PersonGroup(identifier, self.connector)
