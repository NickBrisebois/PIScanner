from .scanner import PIScannerClient

START_BUTTON_PIN ="GPIO5"
LED_PIN = "GPIO21"
STEPPER_PINS = ["GPIO6", "GPIO13", "GPIO19", "GPIO26"]


def main():
    scanner = PIScannerClient(
        start_button_pin=START_BUTTON_PIN,
        led_pin=LED_PIN,
        stepper_pins=STEPPER_PINS
    )
    scanner.run()


if __name__ == "__main__":
    main()
