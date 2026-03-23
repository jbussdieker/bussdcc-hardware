from typing import Literal
from dataclasses import dataclass, field


@dataclass(slots=True)
class USBCameraConfig:
    device_index: int = field(
        default=0,
        metadata={
            "label": "Camera Device Index",
            "group": "Device",
            "ui": "number",
            "min": 0,
            "max": 16,
        },
    )

    format: Literal["MJPG", "YUYV"] = field(
        default="MJPG",
        metadata={
            "label": "Pixel Format",
            "group": "Video",
            "ui": "select",
        },
    )

    width: int = field(
        default=1280,
        metadata={
            "label": "Frame Width",
            "group": "Video",
            "ui": "number",
            "min": 160,
            "max": 3840,
        },
    )

    height: int = field(
        default=720,
        metadata={
            "label": "Frame Height",
            "group": "Video",
            "ui": "number",
            "min": 120,
            "max": 2160,
        },
    )

    fps: int = field(
        default=30,
        metadata={
            "label": "Frames Per Second",
            "group": "Video",
            "ui": "number",
            "min": 1,
            "max": 120,
        },
    )

    auto_exposure: bool = field(
        default=True,
        metadata={
            "label": "Auto Exposure",
            "group": "Exposure",
        },
    )

    exposure: float = field(
        default=-6.0,
        metadata={
            "label": "Exposure",
            "group": "Exposure",
            "ui": "number",
            "min": -13.0,
            "max": -1.0,
            "step": 0.1,
        },
    )

    gain: float = field(
        default=1.0,
        metadata={
            "label": "Gain",
            "group": "Exposure",
            "help": "Amplification applied to the sensor signal",
            "ui": "number",
            "min": 0,
            "max": 16,
            "step": 0.1,
        },
    )

    auto_focus: bool = field(
        default=True,
        metadata={
            "label": "Auto Focus",
            "group": "Focus",
        },
    )

    focus: float = field(
        default=0.0,
        metadata={
            "label": "Focus",
            "group": "Focus",
            "ui": "number",
            "min": 0,
            "max": 255,
        },
    )

    auto_white_balance: bool = field(
        default=True,
        metadata={
            "label": "Auto White Balance",
            "group": "White Balance",
        },
    )

    white_balance_temperature: float = field(
        default=4500.0,
        metadata={
            "label": "White Balance Temperature (K)",
            "group": "White Balance",
            "ui": "number",
            "min": 2800,
            "max": 6500,
            "step": 10,
        },
    )

    buffersize: int = field(
        default=1,
        metadata={
            "label": "Buffer Size",
            "group": "Video",
            "ui": "number",
            "help": "Number of frames the driver buffers internally (OpenCV CAP_PROP_BUFFERSIZE)",
            "min": 1,
            "max": 16,
            "step": 1,
        },
    )

    flush_frames: int = field(
        default=0,
        metadata={
            "label": "Frames to Flush",
            "group": "Video",
            "ui": "number",
            "help": "Number of stale frames to discard on each read to reduce latency",
            "min": 0,
            "max": 16,
            "step": 1,
        },
    )
