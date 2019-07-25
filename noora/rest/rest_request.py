from requests import post
from requests import get
import json


class RestRequest:

    @staticmethod
    def get(headers, url, message=None, certificate=None, proxies=None):
        # retrieve the file locations of the crt and key.
        cert = None
        if certificate:
            cert = (certificate['crt'], certificate['key'])

        if not message:
            message = dict()

        response = get(url,
                       params=message,
                       headers=headers,
                       cert=cert,
                       proxies=proxies
                       )

        return response

    @staticmethod
    def post(headers, url, message=None, certificate=None, proxies=None):

        # retrieve the file locations of the crt and key.
        cert = None
        if certificate:
            cert = (certificate['crt'], certificate['key'])

        if not message:
            message = dict()

        response = post(url, json.dumps(message), headers=headers, cert=cert, proxies=proxies)
        return response
