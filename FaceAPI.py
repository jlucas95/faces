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
            body = {"url":path}
            headers = {"Content-Type": "application/json"}
        else:
            headers = {"Content-Type": "application/octet-stream"}
            try:
                body = image.read()
            except AttributeError as e:
                raise ValueError("image argument must be string or support file like operations")

        faces, response =  self.connector.send_request("POST",
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

    def create_person(self):
        """
        create new person
        """
        raise NotImplementedError

    def get_persongroups(self):
        """
        get all persongroups
        """
        raise NotImplementedError

    def create_persongroup(self, identifier, display_name, description):
        """
        create new persongroup
        """
        body = {"name":display_name,
                "userData": description}
        self.connector.send_request("PUT",
                                    "persongroups",
                                    {"personGroupId":identifier},
                                    body=body)
