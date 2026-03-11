from typing import Literal

import RPi.GPIO as GPIO

from bussdcc import Device

from .config import GPIOBusConfig, PinMode
from .interface import GPIOInterface, PinDirection, Pull, Level

GPIOMode = Literal[10, 11]
GPIODirection = Literal[0, 1]


class GPIOBus(Device[GPIOBusConfig], GPIOInterface):
    kind = "bus"

    MODE_MAP: dict[PinMode, GPIOMode] = {
        "BCM": GPIO.BCM,
        "BOARD": GPIO.BOARD,
    }

    DIR_MAP: dict[PinDirection, GPIODirection] = {
        "in": GPIO.IN,
        "out": GPIO.OUT,
    }

    PULL_MAP: dict[Pull, int] = {
        "off": GPIO.PUD_OFF,
        "up": GPIO.PUD_UP,
        "down": GPIO.PUD_DOWN,
    }

    def connect(self) -> None:
        GPIO.setmode(self.MODE_MAP[self.config.mode])
        GPIO.setwarnings(self.config.warnings)

    def disconnect(self) -> None:
        GPIO.cleanup()

    def protocol(self) -> GPIOInterface:
        return self

    def setup(
        self,
        pin: int,
        direction: PinDirection,
        *,
        pull: Pull = "off",
        initial: Level | None = None,
    ) -> None:

        kwargs = {
            "pull_up_down": self.PULL_MAP[pull],
        }

        if initial is not None:
            kwargs["initial"] = GPIO.HIGH if initial else GPIO.LOW

        GPIO.setup(pin, self.DIR_MAP[direction], **kwargs)

    def input(self, pin: int) -> Level:
        return 1 if GPIO.input(pin) else 0

    def output(self, pin: int, value: Level) -> None:
        GPIO.output(pin, GPIO.HIGH if value else GPIO.LOW)
