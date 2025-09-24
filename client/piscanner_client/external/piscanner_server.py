import requests


class PIScannerServerAPI:
    _server_uri: str

    def __init__(self, server_uri: str):
        self._server_uri = server_uri

    def post_image(self, scan_id: str, image: bytes):
        url = f"{self._server_uri}/image/{scan_id}"
        response = requests.post(url, data=image)
        response.raise_for_status()
