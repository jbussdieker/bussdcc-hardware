from typing import Protocol, Literal

PinDirection = Literal["in", "out"]
Pull = Literal["up", "down", "off"]
Level = Literal[0, 1]


class GPIOProtocol(Protocol):

    def setup(
        self,
        pin: int,
        direction: PinDirection,
        *,
        pull: Pull = "off",
        initial: Level | None = None,
    ) -> None: ...

    def input(self, pin: int) -> Level: ...

    def output(self, pin: int, value: Level) -> None: ...
