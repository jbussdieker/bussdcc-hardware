from bussdcc.device.definition import DeviceDefinition

from .config import PumpConfig
from .driver import Pump

definition = DeviceDefinition(
    config_class=PumpConfig,
    driver_class=Pump,
)
