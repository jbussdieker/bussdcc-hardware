from dataclasses import dataclass
from typing import Type

from .config import USBCameraConfig
from .driver import USBCamera


@dataclass(slots=True, frozen=True)
class USBCameraDefinition:
    config_class: Type[USBCameraConfig] = USBCameraConfig
    driver_class: Type[USBCamera] = USBCamera


definition = USBCameraDefinition()
