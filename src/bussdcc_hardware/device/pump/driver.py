from typing import Optional, Any

import RPi.GPIO as GPIO

from bussdcc.device import Device

from .config import PumpConfig


class Pump(Device[PumpConfig]):
    kind = "actuator"

    def __init__(self, *, id: str, config: PumpConfig):
        super().__init__(id=id, config=config)
        self._state = False

    def connect(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.config.pin, GPIO.OUT)
        GPIO.output(self.config.pin, GPIO.LOW)

    def on(self) -> None:
        GPIO.output(self.config.pin, GPIO.HIGH)
        self._state = True

    def off(self) -> None:
        GPIO.output(self.config.pin, GPIO.LOW)
        self._state = False

    def disconnect(self) -> None:
        self.off()
        GPIO.cleanup(self.config.pin)
