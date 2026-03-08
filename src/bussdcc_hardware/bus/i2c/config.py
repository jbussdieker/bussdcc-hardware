from typing import Any
from dataclasses import dataclass


@dataclass(slots=True)
class I2CBusConfig:
    bus: int = 1

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "I2CBusConfig":
        return cls(bus=data.get("bus", 1))
