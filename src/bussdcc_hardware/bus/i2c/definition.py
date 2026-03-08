from bussdcc.device.definition import DeviceDefinition

from .config import I2CBusConfig
from .driver import I2CBus

definition = DeviceDefinition(
    config_class=I2CBusConfig,
    driver_class=I2CBus,
)
