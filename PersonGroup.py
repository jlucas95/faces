"""
contains the persongroup class
"""
from Person import Person

class PersonGroup:
    """description of class"""

    def __init__(self, persongroup_id, connector):
        self.persongroup_id = persongroup_id
        self._persons = None
        self.connector = connector

    def _retrieve_persons(self):
        url = "persongroups/{}/persons".format(self.persongroup_id)
        data, response = self.connector.send_request("GET", url)
        persons = self.connector.decode_json(data.read())

        person_list = []
        for person in persons:
            person_list.append(
                Person(self.persongroup_id,
                       person["personId"],
                       person["PersistedFaceIds"],
                       self.connector
                      )
                )
        return person_list

    def get_persons(self):
        """
        returns the persons in a personlist
        """
        if self._persons is None:
            self._persons = self._retrieve_persons()
        return self._persons

    def train(self):
        """
        Train a persongroup
        """
        raise NotImplementedError

    def update(self):
        """
        Update the display name and description of a group
        """
        raise NotImplementedError


