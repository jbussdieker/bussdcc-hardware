from typing import Any
from dataclasses import dataclass


@dataclass(slots=True)
class PumpConfig:
    pin: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PumpConfig":
        return cls(pin=data["pin"])
