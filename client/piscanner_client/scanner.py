from time import sleep
from gpiozero import Button, LED

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

    def __init__(
        self,
        start_button_pin: str,
        led_pin: str,
        stepper_pins: list[str]
    ) -> None:
        self._start_button_pin = start_button_pin
        self._led_pin = led_pin
        self._stepper_pins = stepper_pins

        self._button = Button(self._start_button_pin, pull_up=False)
        # self._led = LED(self._led_pin)
        self._stepper_controller = Stepper28BYJ_48Controller(*self._stepper_pins)
        self._webcam_controller = WebcamController()
        print("GPIO pins initialized successfully!")

    def start_capture(self, num_images: int):
        print("Starting capture...")

        for _ in range(num_images):
            _ = self._webcam_controller.capture_image()
            self._stepper_controller.rotate(50, speed=0.005)
            print("Image captured and stepper rotated")

        print("Capture complete")

    def run(self):
        try:
            while True:
                if self._button.is_pressed:
                    self.start_capture(10)
                sleep(0.1)
        except Exception as e:
            print(f"Unexpected error: {e}")

        try:
            self._led.off()
            self._stepper_controller.close()
            print("Cleanup complete")
        except Exception as e:
            print(f"Cleanup failed: {e}")
