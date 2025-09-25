import requests


class PIScannerServerAPI:
    _server_uri: str

    def __init__(self, server_uri: str):
        self._server_uri = server_uri

    def post_image(self, scan_id: str, image: bytes):
        url = f"{self._server_uri}/images/upload/{scan_id}"
        response = requests.post(url, files={
            'file': (
                "capture.jpg", image, "image/jpeg"
            )
        })
        response.raise_for_status()
