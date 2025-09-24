import os
from time import sleep
import time
from gpiozero import Button, LED
from piscanner_client.external.piscanner_server import PIScannerServerAPI

from .hardware.webcam import WebcamController
from .hardware.stepper import Stepper28BYJ_48Controller


class PIScannerClient:
    _button: Button
    _led: LED
    _stepper_controller: Stepper28BYJ_48Controller
    _webcam_controller: WebcamController

    _start_button_pin: str | int
    _led_pin: str | int
    _stepper_pins: list[str]

    _piscanner_api: PIScannerServerAPI

    def __init__(
        self,
        start_button_pin: str,
        led_pin: str,
        stepper_pins: list[str],
        piscanner_server_uri: str,
    ) -> None:
        self._start_button_pin = start_button_pin
        self._led_pin = led_pin
        self._stepper_pins = stepper_pins

        self._button = Button(self._start_button_pin, pull_up=False)
        self._led = LED(self._led_pin)
        self._stepper_controller = Stepper28BYJ_48Controller(*self._stepper_pins)
        self._webcam_controller = WebcamController()
        self._piscanner_api = PIScannerServerAPI(piscanner_server_uri)

        print("GPIO pins initialized successfully!")

    def start_capture(self, num_images: int):
        print("Starting capture...")
        scan_id = time.strftime("%Y%m%d-%H%M%S")
        os.makedirs(scan_id, exist_ok=True)

        degrees_per_image = 360 / num_images

        for i in range(num_images):
            cap_image = self._webcam_controller.capture_image(capture_dir=scan_id)
            self._piscanner_api.post_image(scan_id=scan_id, image=cap_image)
            sleep(1)

            # rotate plate if there are more images to capture
            if i+1 < num_images:
                self._stepper_controller.rotate(degrees_per_image, speed=0.001)

            print("Image captured and stepper rotated")

        print("Capture complete")

    def run(self):
        try:
            while True:
                if self._button.is_pressed:
                    self.start_capture(15)
                sleep(0.1)
        except KeyboardInterrupt:
            print("Quitting...")
        except Exception as e:
            print(f"Unexpected error: {e}")

        try:
            self._led.off()
            self._stepper_controller.close()
            print("Cleanup complete")
        except Exception as e:
            print(f"Cleanup failed: {e}")
