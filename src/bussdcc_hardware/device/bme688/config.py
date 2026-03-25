from dataclasses import dataclass, field


@dataclass(slots=True)
class BME688Config:
    bus_id: str = field(
        metadata={
            "label": "I²C Bus",
            "group": "Connection",
            "ref": {"kind": "bus"},
            "required": True,
        }
    )

    addr: int = field(
        default=0x77,
        metadata={
            "label": "I²C Address",
            "group": "Connection",
            "min": 0,
            "max": 127,
        },
    )
