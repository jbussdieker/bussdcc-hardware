from typing import Any
from dataclasses import dataclass


@dataclass(slots=True)
class USBCameraConfig:
    device_index: int = 0
    format: str = "MJPG"
    width: int = 640
    height: int = 480
    fps: int = 30

    auto_exposure: bool = True
    exposure: float = 0.0
    gain: float = 0.0

    auto_focus: bool = True
    focus: float = 0.0

    auto_white_balance: bool = True
    white_balance_temperature: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "USBCameraConfig":
        return cls(
            device_index=data.get("device_index", 0),
            format=data.get("format", "MJPG"),
            width=data.get("width", 640),
            height=data.get("height", 480),
            fps=data.get("fps", 30),
            auto_exposure=data.get("auto_exposure", True),
            exposure=data.get("exposure", 0.0),
            gain=data.get("gain", 0.0),
            auto_focus=data.get("auto_focus", True),
            focus=data.get("focus", 0.0),
            auto_white_balance=data.get("auto_white_balance", True),
            white_balance_temperature=data.get("white_balance_temperature", 0.0),
        )
