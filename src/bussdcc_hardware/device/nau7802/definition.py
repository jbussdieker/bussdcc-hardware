from bussdcc.device.definition import DeviceDefinition

from .config import NAU7802Config
from .driver import NAU7802

definition = DeviceDefinition(
    config_class=NAU7802Config,
    driver_class=NAU7802,
)
