from typing import Any, Literal
from dataclasses import dataclass, field


@dataclass(slots=True)
class NAU7802CalibrationConfig:
    offset: int = field(
        default=0,
        metadata={
            "label": "Offset",
            "group": "Calibration",
        },
    )

    scale: float = field(
        default=1.0,
        metadata={
            "label": "Scale Factor",
            "group": "Calibration",
        },
    )


@dataclass(slots=True)
class NAU7802ChannelConfig:
    calibration: NAU7802CalibrationConfig = field(metadata={"group": "Channels"})


@dataclass(slots=True)
class NAU7802Config:
    bus_id: str = field(
        metadata={
            "label": "I²C Bus",
            "group": "Connection",
            "ref": {"kind": "bus"},
            "required": True,
        }
    )

    addr: int = field(
        default=0x2A,
        metadata={
            "label": "I²C Address",
            "group": "Connection",
            "min": 0,
            "max": 127,
        },
    )

    gain: Literal[1, 2, 4, 8, 16, 32, 64, 128] = field(
        default=128,
        metadata={
            "label": "Gain",
            "group": "ADC",
        },
    )

    sample_rate: Literal[10, 20, 40, 80, 320] = field(
        default=10,
        metadata={
            "label": "Sample Rate (SPS)",
            "group": "ADC",
        },
    )

    samples: int = field(
        default=1,
        metadata={
            "label": "Samples per Reading",
            "group": "Performance",
            "min": 1,
            "max": 64,
        },
    )

    discard_samples: int = field(
        default=8,
        metadata={
            "label": "Discard Samples After Channel Switch",
            "group": "Performance",
            "min": 0,
            "max": 32,
        },
    )

    channels: dict[int, NAU7802ChannelConfig] = field(
        default_factory=dict,
        metadata={"group": "Channels"},
    )
