from typing import Optional, Any
from bussdcc.device import Device

try:
    import RPi.GPIO as GPIO

    AVAILABLE = True
except ModuleNotFoundError:
    AVAILABLE = False


class Pump(Device):
    kind = "actuator"

    def __init__(self, *, id: str, config: Optional[dict[str, Any]] = None):
        super().__init__(id=id, config=config)
        self.pin = int(self.config["pin"])
        self._state = False

    @property
    def available(self) -> bool:
        return AVAILABLE

    def connect(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def on(self) -> None:
        GPIO.output(self.pin, GPIO.HIGH)
        self._state = True

    def off(self) -> None:
        GPIO.output(self.pin, GPIO.LOW)
        self._state = False

    def disconnect(self) -> None:
        self.off()
        GPIO.cleanup(self.pin)
