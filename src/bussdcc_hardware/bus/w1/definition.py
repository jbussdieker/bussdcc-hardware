from bussdcc.device.definition import DeviceDefinition

from .config import W1BusConfig
from .driver import W1Bus

definition = DeviceDefinition(
    config_class=W1BusConfig,
    driver_class=W1Bus,
)
