from bussdcc.device.definition import DeviceDefinition

from .config import BlueZAdapterConfig
from .driver import BlueZAdapter

definition = DeviceDefinition(
    config_class=BlueZAdapterConfig,
    driver_class=BlueZAdapter,
)
