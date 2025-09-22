import cv2
import os
import time


class WebcamHandlerException(Exception):
    ...


class WebcamController:
    _cam: cv2.VideoCapture
    _capture_dir: str

    def __init__(self, capture_dir: str = "/tmp/piscanner/captures") -> None:
        self._cam = cv2.VideoCapture(0)
        self._capture_dir = capture_dir
        os.makedirs(self._capture_dir, exist_ok=True)


    def capture_image(self):
        ret, frame = self._cam.read()
        if not ret:
            raise WebcamHandlerException("Failed to capture image")

        file_name = f"{self._capture_dir}/cap_{int(time.time())}.jpg"
        _ = cv2.imwrite(file_name, frame)

        return file_name
