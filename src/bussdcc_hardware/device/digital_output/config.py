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
            "ref": {"kind": "bus"},
            "required": True,
        }
    )

    pin: int = field(
        metadata={
            "label": "GPIO Output Pin",
            "group": "Hardware",
            "min": 2,
            "max": 27,
        },
    )

    logic: Logic = field(
        default="active_high",
        metadata={
            "label": "Logic Level",
            "group": "Behavior",
            "help": "Determines whether the device is active when the pin is HIGH or LOW",
        },
    )

    safe_state: SafeState = field(
        default="off",
        metadata={
            "label": "Safe State",
            "group": "Safety",
            "help": "State to enter when device disconnects",
        },
    )
