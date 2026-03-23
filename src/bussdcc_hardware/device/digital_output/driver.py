from typing import Literal

from bussdcc import Device

from ...bus.gpio import GPIOInterface

from .config import DigitalOutputConfig


class DigitalOutput(Device[DigitalOutputConfig]):
    kind = "actuator"

    def __init__(self, *, id: str, config: DigitalOutputConfig):
        super().__init__(id=id, config=config)
        self.gpio: GPIOInterface | None = None

    def _level(self, state: bool) -> Literal[0, 1]:
        """Logical -> electrical"""
        if self.config.logic == "active_high":
            return 1 if state else 0
        else:
            return 0 if state else 1

    def _logical(self, level: int) -> bool:
        """Electrical -> logical"""
        if self.config.logic == "active_high":
            return level == 1
        else:
            return level == 0

    @property
    def state(self) -> bool:
        if not self.gpio:
            return False

        level = self.gpio.input(self.config.pin)
        return self._logical(level)

    def connect(self) -> None:
        if not self.ctx:
            raise RuntimeError("Device not attached")

        bus = self.ctx.runtime.devices.get(self.config.bus_id)
        protocol = bus.protocol() if bus and hasattr(bus, "protocol") else None
        if not isinstance(protocol, GPIOInterface):
            raise RuntimeError(
                "DigitalOutput requires a bus that supports GPIOInterface"
            )

        self.gpio = protocol

        self.gpio.setup(
            self.config.pin,
            "out",
            initial=self._level(False),
        )

    def disconnect(self) -> None:
        if not self.gpio:
            return

        if self.config.safe_state == "on":
            self.on()
        else:
            self.off()

    def on(self) -> None:
        if self.gpio:
            self.gpio.output(self.config.pin, self._level(True))

    def off(self) -> None:
        if self.gpio:
            self.gpio.output(self.config.pin, self._level(False))

    def toggle(self) -> None:
        if self.state:
            self.off()
        else:
            self.on()
