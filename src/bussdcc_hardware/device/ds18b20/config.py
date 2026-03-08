from typing import Any
from dataclasses import dataclass


@dataclass(slots=True)
class DS18B20Config:
    bus_id: str
    device_id: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DS18B20Config":
        return cls(bus_id=data["bus_id"], device_id=data["device_id"])
