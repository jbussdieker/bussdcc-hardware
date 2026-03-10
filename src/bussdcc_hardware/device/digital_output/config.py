from typing import Any
from dataclasses import dataclass, field


@dataclass(slots=True)
class DigitalOutputConfig:
    bus_id: str = field(
        metadata={
            "label": "GPIO Bus",
            "group": "Connection",
            "ui": "bus",
        }
    )

    pin: int = field(
        metadata={
            "label": "GPIO Output Pin",
            "group": "Hardware",
            "ui": "number",
            "min": 2,
            "max": 27,
        },
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DigitalOutputConfig":
        return cls(bus_id=data["bus_id"], pin=data["pin"])
