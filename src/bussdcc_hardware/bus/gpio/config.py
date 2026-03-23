from typing import Literal
from dataclasses import dataclass, field

PinMode = Literal["BCM", "BOARD"]


@dataclass(slots=True)
class GPIOBusConfig:
    mode: PinMode = field(
        default="BCM",
        metadata={
            "label": "Pin Numbering Mode",
            "group": "GPIO",
            "ui": "select",
            "options": ["BCM", "BOARD"],
        },
    )

    warnings: bool = field(
        default=False,
        metadata={
            "label": "Enable GPIO Warnings",
            "group": "GPIO",
        },
    )
