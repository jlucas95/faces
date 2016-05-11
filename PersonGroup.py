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
        persons, response = self.connector.send_request("GET", url)

        person_list = []
        for person in persons:
            person_list.append(
                Person(self.persongroup_id,
                       person,
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
        url = "persongroups/{}/train".format(self.persongroup_id)

        data, response = self.connector.send_request("POST", url)
        return response

    def train_async(self):
        """
        implements the same function as train, but does not block until the training is complete
        :return:
        """
        raise NotImplementedError

    def update(self):
        """
        Update the display name and description of a group
        """
        raise NotImplementedError

    def remove_person(self, person_id):
        """
        Delete a person from the persongroup
        :param person_id:
        :return:
        """
        url = "persongroups/{}/persons/{}".format(self.persongroup_id, person_id)

        data, response = self.connector.send_request("DELETE", url)
        if response.status == 200:
            self._remove_person(person_id)
            return True
        else:
            return False

    def _remove_person(self, person_id):
        if self._persons is None:
            return

        for person in self._persons:
            if person.person_id == person_id:
                self._persons.remove(person)

    def find_person(self, person_id):
        persons = self.get_persons()
        for person in persons:
            if person.person_id == person_id:
                return person