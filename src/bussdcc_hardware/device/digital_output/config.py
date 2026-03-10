from typing import Any, Literal
from dataclasses import dataclass, field

SafeState = Literal["off", "on"]
Logic = Literal["active_high", "active_low"]


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

    logic: Logic = field(
        default="active_high",
        metadata={
            "label": "Logic Level",
            "group": "Behavior",
            "ui": "select",
            "options": ["active_high", "active_low"],
            "help": "Determines whether the device is active when the pin is HIGH or LOW",
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
            logic=data.get("logic", "active_high"),
            safe_state=data.get("safe_state", "off"),
        )
