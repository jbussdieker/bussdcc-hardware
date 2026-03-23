from bussdcc.device.definition import DeviceDefinition

from .config import MockTemperatureConfig
from .driver import MockTemperature

definition = DeviceDefinition(
    config_class=MockTemperatureConfig,
    driver_class=MockTemperature,
)
