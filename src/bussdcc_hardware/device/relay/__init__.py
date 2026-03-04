from typing import Optional, Any
import time

from bussdcc.device import Device

from ...bus.gpio import GPIO, GPIOProtocol


class Relay(Device):
    kind = "relay"

    def __init__(self, *, id: str, config: Optional[dict[str, Any]] = None):
        super().__init__(id=id, config=config)
        self.gpio_id = self.config["gpio_id"]
        self.pin = int(self.config["pin"])
        self.active_low = self.config.get("active_low", False)
        self._GPIO: GPIOProtocol

    def connect(self) -> None:
        if not self.ctx:
            raise RuntimeError("Device not attached")

        gpio = self.ctx.runtime.get_device(self.gpio_id)
        if not isinstance(gpio, GPIO):
            raise RuntimeError("Failed to find GPIO bus")

        self._GPIO = gpio.raw

        initial = self._GPIO.HIGH if self.active_low else self._GPIO.LOW
        self._GPIO.setup(self.pin, self._GPIO.OUT, initial=initial)

    def disconnect(self) -> None:
        self._GPIO.cleanup(self.pin)

    def set(self, value: bool) -> None:
        level = not value if self.active_low else value
        self._GPIO.output(self.pin, level)

    def get(self) -> bool:
        level = bool(self._GPIO.input(self.pin))
        return not level if self.active_low else level
