from bussdcc.device.definition import DeviceDefinition

from .config import GPIOBusConfig
from .driver import GPIOBus

definition = DeviceDefinition(
    config_class=GPIOBusConfig,
    driver_class=GPIOBus,
)
