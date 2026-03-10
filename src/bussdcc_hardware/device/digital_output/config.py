from typing import Any, Literal
from dataclasses import dataclass, field

SafeState = Literal["off", "on"]


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

    active_high: bool = field(
        default=True,
        metadata={
            "label": "Active High",
            "group": "Hardware",
            "help": "If false, the output is active-low",
        },
    )

    safe_state: SafeState = field(
        default="off",
        metadata={
            "label": "Safe State",
            "group": "Safety",
            "ui": "select",
            "options": ["off", "on"],
            "help": "State to enter when device disconnects",
        },
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DigitalOutputConfig":
        return cls(
            bus_id=data["bus_id"],
            pin=data["pin"],
            active_high=data.get("active_high", True),
            safe_state=data.get("safe_state", "off"),
        )
