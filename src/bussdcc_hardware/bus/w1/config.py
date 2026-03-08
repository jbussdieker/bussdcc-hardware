from typing import Any
from dataclasses import dataclass


@dataclass(slots=True)
class W1BusConfig:
    base_path: str = "/sys/bus/w1/devices"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "W1BusConfig":
        return cls(base_path=data.get("base_path", "/sys/bus/w1/devices"))
