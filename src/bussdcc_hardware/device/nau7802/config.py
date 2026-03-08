from typing import Any
from dataclasses import dataclass


@dataclass(slots=True)
class NAU7802CalibrationConfig:
    offset: int = 0
    scale: float = 1.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NAU7802CalibrationConfig":
        return cls(
            offset=data.get("offset", 0),
            scale=data.get("scale", 1.0),
        )


@dataclass(slots=True)
class NAU7802ChannelConfig:
    calibration: NAU7802CalibrationConfig

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NAU7802ChannelConfig":
        return cls(
            calibration=NAU7802CalibrationConfig.from_dict(data.get("calibration", {}))
        )


@dataclass(slots=True)
class NAU7802Config:
    bus_id: str
    channels: dict[str, NAU7802ChannelConfig]
    addr: int = 0x2A

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
