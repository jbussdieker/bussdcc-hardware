from typing import Any
from dataclasses import dataclass, field


@dataclass(slots=True)
class DS18B20Config:
    bus_id: str = field(
        metadata={
            "label": "1-Wire Bus",
            "group": "Connection",
            "ui": "bus",
        }
    )

    device_id: str = field(
        metadata={
            "label": "Device ID",
            "group": "Connection",
            "ui": "text",
        }
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DS18B20Config":
        return cls(bus_id=data["bus_id"], device_id=data["device_id"])
