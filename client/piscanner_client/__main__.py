import argparse

from .scanner import PIScannerClient

START_BUTTON_PIN ="GPIO5"
LED_PIN = "GPIO21"
STEPPER_PINS = ["GPIO6", "GPIO13", "GPIO19", "GPIO26"]


def main(piscanner_server_uri: str):
    scanner = PIScannerClient(
        start_button_pin=START_BUTTON_PIN,
        led_pin=LED_PIN,
        stepper_pins=STEPPER_PINS,
        piscanner_server_uri=piscanner_server_uri,
    )
    scanner.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PIScanner Client")
    _ = parser.add_argument("--server-uri", type=str, default="http://localhost", help="PIScanner server URI")
    args = parser.parse_args()

    main(piscanner_server_uri=args.server_uri)
