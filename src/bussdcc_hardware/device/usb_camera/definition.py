from bussdcc.device.definition import DeviceDefinition

from .config import USBCameraConfig
from .driver import USBCamera

definition = DeviceDefinition(
    config_class=USBCameraConfig,
    driver_class=USBCamera,
)
