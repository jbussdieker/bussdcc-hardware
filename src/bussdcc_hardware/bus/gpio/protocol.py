from typing import Protocol, Iterable, Literal


class GPIOProtocol(Protocol):
    # constants
    IN: Literal[1]
    OUT: Literal[0]
    LOW: Literal[0]
    HIGH: Literal[1]
    PUD_UP: int
    PUD_DOWN: int
    BCM: int

    # functions
    def setmode(self, mode: Literal[10, 11]) -> None: ...
    def setwarnings(self, flag: bool) -> None: ...
    def setup(
        self,
        pin: int | list[int] | tuple[int, ...],
        direction: Literal[0, 1],
        pull_up_down: int = ...,
        initial: int = ...,
    ) -> None: ...
    def output(
        self,
        pin: int | list[int] | tuple[int, ...],
        state: (
            Literal[0, 1]
            | bool
            | list[Literal[0, 1] | bool]
            | tuple[Literal[0, 1] | bool, ...]
        ),
    ) -> None: ...
    def input(self, pin: int) -> int: ...
    def cleanup(self, pin: int | list[int] | tuple[int, ...] = ...) -> None: ...
