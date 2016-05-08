"""
contains the face class
"""
class Face:
    """description of class"""
    def __init__(self, face_id, user_data):
        self.identifier = face_id
        self.user_data = user_data

    def update(self, user_data):
        """
        updates the description of a face
        """
        raise NotImplementedError


        