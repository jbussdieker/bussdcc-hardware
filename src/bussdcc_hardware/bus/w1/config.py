from typing import Any
from dataclasses import dataclass, field


@dataclass(slots=True)
class W1BusConfig:
    base_path: str = field(
        default="/sys/bus/w1/devices",
        metadata={
            "label": "Base Path",
            "group": "Connection",
            "ui": "path",
        },
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "W1BusConfig":
        return cls(base_path=data.get("base_path", "/sys/bus/w1/devices"))
