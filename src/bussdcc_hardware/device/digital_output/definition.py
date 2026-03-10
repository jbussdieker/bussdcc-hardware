from bussdcc.device.definition import DeviceDefinition

from .config import DigitalOutputConfig
from .driver import DigitalOutput

definition = DeviceDefinition(
    config_class=DigitalOutputConfig,
    driver_class=DigitalOutput,
)
