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
        Sends a request to the API.
        """
        # Because having a dictionary as default value is dangerous
        if qs_args is None:

            qs_args = {}
        if headers is None:
            headers = {}

        # Check what content type header to include in the HTTP message
        if hasattr(body, "read"):
            headers["Content-Type"] = "application/octet-stream"
        else:
            body = self.encode_json(body)
            headers["Content-Type"] = "application/json"

        connection = HTTPSConnection(self.host)

        # Format the url
        url = self.base_url.format(url)
        if len(qs_args) > 0:
            url += "?{}".format(urlencode(qs_args))

        # Add api-key to the headers
        apikey_header = {"Ocp-Apim-Subscription-Key": self.key}
        headers = {**headers, **apikey_header}

        # Send the request
        connection.request(method, url, headers=headers, body=body)

        # Read the response and try to decode JSON
        response = connection.getresponse()
        data_bytes = response.read()
        data = data_bytes.decode()
        # TODO: Except data that is not JSON
        if len(data) > 0:
            data = self.decode_json(data)

        return data, response
