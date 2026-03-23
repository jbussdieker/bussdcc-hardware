from bussdcc.device.definition import DeviceDefinition

from .config import MockGPIOBusConfig
from .driver import MockGPIOBus

definition = DeviceDefinition(
    config_class=MockGPIOBusConfig,
    driver_class=MockGPIOBus,
)
