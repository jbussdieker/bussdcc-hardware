try:
    import RPi.GPIO as _GPIO

    HAS_GPIO = True
except ModuleNotFoundError:
    HAS_GPIO = False

from bussdcc.device import Device

from .protocol import GPIOProtocol
from .fake import FakeGPIO


class GPIO(Device):
    kind = "bus"

    def connect(self) -> None:
        if not HAS_GPIO:
            return

        _GPIO.setmode(_GPIO.BCM)
        _GPIO.setwarnings(False)

    def disconnect(self) -> None:
        # Do NOT blanket cleanup; children clean their own pins
        pass

    @property
    def raw(self) -> GPIOProtocol:
        if not HAS_GPIO:
            return FakeGPIO()

        return _GPIO
