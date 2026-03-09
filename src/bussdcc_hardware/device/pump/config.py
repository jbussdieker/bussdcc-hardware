from typing import Any
from dataclasses import dataclass, field


@dataclass(slots=True)
class PumpConfig:
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
    def from_dict(cls, data: dict[str, Any]) -> "PumpConfig":
        return cls(pin=data["pin"])
