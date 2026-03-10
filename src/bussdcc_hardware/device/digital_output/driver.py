from bussdcc.device import Device

from ...bus.gpio import GPIOBus
from ...bus.gpio.protocol import GPIOProtocol

from .config import DigitalOutputConfig


class DigitalOutput(Device[DigitalOutputConfig]):
    kind = "actuator"

    def __init__(self, *, id: str, config: DigitalOutputConfig):
        super().__init__(id=id, config=config)
        self.gpio: GPIOProtocol | None = None
        self._state = False

    @property
    def state(self) -> bool:
        return self._state

    def connect(self) -> None:
        if not self.ctx:
            raise RuntimeError("Device not attached")

        bus = self.ctx.runtime.devices.get(self.config.bus_id)

        if not isinstance(bus, GPIOBus):
            raise RuntimeError("DigitalOutput requires GPIOBus")

        self.gpio = bus.protocol()

        self.gpio.setup(
            self.config.pin,
            "out",
            initial=0,
        )

    def on(self) -> None:
        if self.gpio:
            self.gpio.output(self.config.pin, 1)
            self._state = True

    def off(self) -> None:
        if self.gpio:
            self.gpio.output(self.config.pin, 0)
            self._state = False

    def disconnect(self) -> None:
        self.off()
