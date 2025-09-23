import cv2
import os
import time


class WebcamHandlerException(Exception):
    ...


class WebcamController:
    _cam: cv2.VideoCapture
    _capture_base_dir: str

    def __init__(self, capture_dir: str = "/tmp/piscanner/captures") -> None:
        self._cam = cv2.VideoCapture(0)
        _ = self._cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        _ = self._cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self._capture_base_dir = capture_dir
        os.makedirs(self._capture_base_dir, exist_ok=True)


    def capture_image(self, capture_dir: str):
        capture_dir = os.path.join(self._capture_base_dir, capture_dir)
        os.makedirs(capture_dir, exist_ok=True)

        ret, frame = self._cam.read()
        if not ret:
            raise WebcamHandlerException("Failed to capture image")

        file_name = f"{capture_dir}/cap_{int(time.time())}.jpg"
        _ = cv2.imwrite(file_name, frame)

        print(f"Image saved to {file_name}")
        return file_name
