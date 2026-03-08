from bussdcc.device.definition import DeviceDefinition

from .config import DS18B20Config
from .driver import DS18B20

definition = DeviceDefinition(
    config_class=DS18B20Config,
    driver_class=DS18B20,
)
