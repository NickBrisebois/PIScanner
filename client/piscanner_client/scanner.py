from gpiozero import Button, LED
from time import sleep

from hardware.stepper import Stepper28BYJ_48

START_BUTTON_PIN ="23"
LED_PIN = "24"
STEPPER_PINS = ["2", "3", "4", "17"]


class PIScannerClient:
    _button: Button | None = None
    _led: LED | None = None
    _stepper_controller: Stepper28BYJ_48

    _start_button_pin: str | int | None = None
    _led_pin: str | int | None = None
    _stepper_pins: list[str] | None = None

    def __init__(
        self,
        start_button_pin: str = START_BUTTON_PIN,
        led_pin: str = LED_PIN,
        stepper_pins: list[str] = STEPPER_PINS
    ) -> None:
        self._start_button_pin = start_button_pin
        self._led_pin = led_pin
        self._stepper_pins = stepper_pins

        print("GPIO pins initialized successfully!")

    def configure_pins(self):
        self._button = Button(self._start_button_pin, pull_up=False)
        self._led = LED(self._led_pin)
        self._stepper_controller = Stepper28BYJ_48(*self._stepper_pins)


    def run(self):
        print("Press Ctrl+C to exit")
        try:
            while True:
                if self._button.is_pressed:
                    print("Button Pressed!")
                    self._led.on()
                    self._stepper_controller.rotate(50, speed=0.01)
                else:
                    self._led.off()

                sleep(0.1)
        except KeyboardInterrupt:
            print("\nProgram interrupted")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            try:
                self._led.off()
                self._stepper_controller.close()
                print("Cleanup complete")
            except:
                print("Cleanup attempted")


if __name__ == "__main__":
    scanner = PIScannerClient(
        start_button_pin=START_BUTTON_PIN,
        led_pin=LED_PIN,
        stepper_pins=STEPPER_PINS
    )
    scanner.configure_pins()
    scanner.run()
