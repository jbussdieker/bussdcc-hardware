from dataclasses import dataclass
from typing import Type

from .config import I2CBusConfig
from .driver import I2CBus


@dataclass(slots=True, frozen=True)
class I2CBusDefinition:
    config_class: Type[I2CBusConfig] = I2CBusConfig
    driver_class: Type[I2CBus] = I2CBus


definition = I2CBusDefinition()
