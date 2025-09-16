from typing import Literal
from gpiozero import OutputDevice
from time import sleep

class Stepper28BYJ_48:
    """Simple stepper motor control for 28BYJ-48"""

    def __init__(self,
        pin1: int | str = 18,
        pin2: int | str = 19,
        pin3: int | str = 20,
        pin4: int | str = 21
    ):
        self.pins: list[OutputDevice] = [OutputDevice(pin1), OutputDevice(pin2),
                    OutputDevice(pin3), OutputDevice(pin4)]

        # Half-step sequence for smooth operation
        self.sequence = [
            [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0],
            [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1]
        ]

        self.position = 0
        self.steps_per_revolution = 4096

    def step(self, clockwise: bool = True, delay: float = 0.001):
        """Move one step"""
        direction = 1 if clockwise else -1
        self.position = (self.position + direction) % len(self.sequence)

        for i, pin in enumerate(self.pins):
            pin.value = self.sequence[self.position][i]

        sleep(delay)

    def rotate(self, degrees: float, speed: float = 0.001):
        """Rotate by degrees (positive=CW, negative=CCW)"""
        steps = int(abs(degrees) * self.steps_per_revolution / 360)
        clockwise = True if degrees > 0 else False

        for _ in range(steps):
            self.step(clockwise, speed)

    def stop(self):
        for pin in self.pins:
            pin.off()

    def close(self):
        self.stop()
        for pin in self.pins:
            pin.close()
