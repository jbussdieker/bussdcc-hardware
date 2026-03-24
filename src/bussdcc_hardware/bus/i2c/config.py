from dataclasses import dataclass, field


@dataclass(slots=True)
class I2CBusConfig:
    bus: int = field(
        default=1,
        metadata={
            "label": "I²C Bus Number",
            "group": "Connection",
            "min": 0,
        },
    )
