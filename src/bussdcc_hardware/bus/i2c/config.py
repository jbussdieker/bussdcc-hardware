from typing import Any
from dataclasses import dataclass, field


@dataclass(slots=True)
class I2CBusConfig:
    bus: int = field(
        default=1,
        metadata={
            "label": "I²C Bus Number",
            "group": "Connection",
            "ui": "number",
            "min": 0,
        },
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "I2CBusConfig":
        return cls(bus=data.get("bus", 1))
