from bussdcc.device.definition import DeviceDefinition

from .config import BME688Config
from .driver import BME688

definition = DeviceDefinition(
    config_class=BME688Config,
    driver_class=BME688,
)
