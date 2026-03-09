from typing import Any
from dataclasses import dataclass, field


@dataclass(slots=True)
class NAU7802CalibrationConfig:
    offset: int = field(
        default=0,
        metadata={
            "label": "Offset",
            "group": "Calibration",
            "ui": "number",
        },
    )

    scale: float = field(
        default=1.0,
        metadata={
            "label": "Scale Factor",
            "group": "Calibration",
            "ui": "number",
            "step": 0.0001,
        },
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NAU7802CalibrationConfig":
        return cls(
            offset=data.get("offset", 0),
            scale=data.get("scale", 1.0),
        )


@dataclass(slots=True)
class NAU7802ChannelConfig:
    calibration: NAU7802CalibrationConfig = field(metadata={"group": "Channels"})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NAU7802ChannelConfig":
        return cls(
            calibration=NAU7802CalibrationConfig.from_dict(data.get("calibration", {}))
        )


@dataclass(slots=True)
class NAU7802Config:
    bus_id: str = field(
        metadata={
            "label": "I²C Bus",
            "group": "Connection",
            "ui": "bus",
        }
    )

    addr: int = field(
        default=0x2A,
        metadata={
            "label": "I²C Address",
            "group": "Connection",
            "ui": "hex",
            "min": 0,
            "max": 127,
        },
    )

    channels: dict[str, NAU7802ChannelConfig] = field(
        default_factory=dict,
        metadata={"group": "Channels"},
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NAU7802Config":
        channels = {
            str(k): NAU7802ChannelConfig.from_dict(v)
            for k, v in data.get("channels", {}).items()
        }

        return cls(
            bus_id=data["bus_id"],
            addr=data.get("addr", 0x2A),
            channels=channels,
        )
