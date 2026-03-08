from typing import Any
from dataclasses import dataclass


@dataclass(slots=True)
class USBCameraConfig:
    device_index: int = 0
    format: str = "MJPG"
    width: int = 640
    height: int = 480
    fps: int = 30

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "USBCameraConfig":
        return cls(
            device_index=data.get("device_index", 0),
            format=data.get("format", "MJPG"),
            width=data.get("width", 640),
            height=data.get("height", 480),
            fps=data.get("fps", 30),
        )
