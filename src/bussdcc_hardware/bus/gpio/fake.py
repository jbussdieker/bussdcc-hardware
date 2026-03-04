from typing import Literal

from .protocol import GPIOProtocol


class FakeGPIO(GPIOProtocol):
    BOARD = 10
    BCM = 11
    OUT = 0
    IN = 1
    PUD_OFF = 20
    PUD_DOWN = 21
    PUD_UP = 22
    LOW = 0
    HIGH = 1

    def __init__(self) -> None:
        self._pins: dict[int, int] = {}

    def setmode(self, mode: int) -> None:
        pass

    def setwarnings(self, flag: bool) -> None:
        pass

    def setup(
        self,
        pin: int | list[int] | tuple[int, ...],
        direction: Literal[0, 1],
        pull_up_down: int = 0,
        initial: int = 0,
    ) -> None:
        if isinstance(pin, int):
            self._pins[pin] = initial if initial is not None else self.LOW

    def output(
        self,
        pin: int | list[int] | tuple[int, ...],
        level: (
            Literal[0, 1]
            | bool
            | list[Literal[0, 1] | bool]
            | tuple[Literal[0, 1] | bool, ...]
        ),
    ) -> None:
        if isinstance(pin, int) and isinstance(level, int):
            self._pins[pin] = int(level)

    def input(self, pin: int) -> int:
        return self._pins.get(pin, self.LOW)

    def cleanup(self, pin: int | list[int] | tuple[int, ...] = []) -> None:
        if isinstance(pin, int):
            self._pins.pop(pin, None)
