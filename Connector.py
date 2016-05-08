"""
Standard connector
All requests to the face API should go through here
"""

from http.client import HTTPSConnection
from urllib.parse import urlencode
from json.encoder import JSONEncoder
from json.decoder import JSONDecoder


class Connector:
    """description of class"""

    def __init__(self, api_key):
        self.key = api_key
        self.host = "api.projectoxford.ai"
        self.base_url = "/face/v1.0/{}"
        self.encoder = JSONEncoder()
        self.decoder = JSONDecoder()

    def encode_json(self, dictionary):
        """
        encodes dictionaries to json to send to API
        """
        return self.encoder.encode(dictionary)

    def decode_json(self, json):
        """
        decodes json to a dictionary
        """
        return self.decoder.decode(json)


    def send_request(self, method, url, qs_args=None, headers=None, body=None):
        """
        Sends a request to the API
        """
        if isinstance(body, dict):
            body = self.encode_json(body)

        # Because having a dictionary as default value is dangerous
        if qs_args is None:
            qs_args = {}

        if headers is None:
            headers = {}



        connection = HTTPSConnection(self.host)
        url = self.base_url.format(url)
        url += "?{}".format(urlencode(qs_args))
        apikey_header = {"Ocp-Apim-Subscription-Key": self.key}

        # NOT AN ERROR
        # Valid python 3.5 syntax. ** unpacks a dictionary
        headers = {**headers, **apikey_header}
        print(url)
        print(type(body))
        connection.request(method, url, headers=headers, body=body)
        response = connection.getresponse()
        data_bytes = response.read()
        data = data_bytes.decode()
        data = self.decode_json(data)
        return data, response



