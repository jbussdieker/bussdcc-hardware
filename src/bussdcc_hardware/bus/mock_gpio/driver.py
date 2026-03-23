from bussdcc import Device

from ..gpio.config import PinMode
from ..gpio.interface import GPIOInterface, PinDirection, Pull, Level
from .config import MockGPIOBusConfig


class MockGPIOBus(Device[MockGPIOBusConfig], GPIOInterface):
    kind = "bus"

    def __init__(self, *, id: str, config: MockGPIOBusConfig):
        super().__init__(id=id, config=config)
        self._configured: dict[int, dict[str, object]] = {}
        self._levels: dict[int, Level] = {}

    def connect(self) -> None:
        self.set_online()

    def disconnect(self) -> None:
        self._configured.clear()
        self._levels.clear()

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
        self._configured[pin] = {
            "direction": direction,
            "pull": pull,
        }

        if initial is not None:
            self._levels[pin] = initial
        elif pin not in self._levels:
            self._levels[pin] = 0

    def input(self, pin: int) -> Level:
        if pin not in self._configured:
            raise RuntimeError(f"Pin {pin} has not been configured")

        value = self._levels.get(pin, 0)
        return 1 if value else 0

    def output(self, pin: int, value: Level) -> None:
        cfg = self._configured.get(pin)
        if cfg is None:
            raise RuntimeError(f"Pin {pin} has not been configured")

        if cfg["direction"] != "out":
            raise RuntimeError(f"Pin {pin} is not configured as output")

        self._levels[pin] = 1 if value else 0

    def get_pin_state(self, pin: int) -> dict[str, object] | None:
        cfg = self._configured.get(pin)
        if cfg is None:
            return None

        return {
            "pin": pin,
            "direction": cfg["direction"],
            "pull": cfg["pull"],
            "level": self._levels.get(pin, 0),
        }

    def set_input_level(self, pin: int, value: Level) -> None:
        cfg = self._configured.get(pin)
        if cfg is None:
            raise RuntimeError(f"Pin {pin} has not been configured")

        if cfg["direction"] != "in":
            raise RuntimeError(f"Pin {pin} is not configured as input")

        self._levels[pin] = 1 if value else 0

    def configured_pins(self) -> dict[int, dict[str, object]]:
        return {pin: dict(cfg) for pin, cfg in self._configured.items()}
