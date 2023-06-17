from enum import Enum

import requests as r

API_BASE = "https://jsonplaceholder.typicode.com"


class ENDPOINTS(Enum):
    posts = "/posts/"


class API():

    def __init__(self, url: str):
        self.url = url

    def _make_address(self, *args):
        return "".join([API_BASE, *args])

    def get(self, endpoint: str,
            params: dict = None):
        if not params:
            params = {}

        get_address = self._make_address(endpoint)
        return r.get(get_address, params={**params})

    def post(self, endpoint: str, json: dict, params: dict = None):
        if not params:
            params = {}

        post_address = self._make_address(endpoint)
        return r.post(post_address, params={**params}, json=json)

    def delete(self, endpoint: str, id: int):
        delete_address = self._make_address(endpoint, id)
        print(delete_address)
        return r.delete(delete_address)
