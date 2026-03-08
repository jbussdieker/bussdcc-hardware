from dataclasses import dataclass
from typing import Type

from .config import PumpConfig
from .driver import Pump


@dataclass(slots=True, frozen=True)
class PumpDefinition:
    config_class: Type[PumpConfig] = PumpConfig
    driver_class: Type[Pump] = Pump


definition = PumpDefinition()
