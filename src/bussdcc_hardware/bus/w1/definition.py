from dataclasses import dataclass
from typing import Type

from .config import W1BusConfig
from .driver import W1Bus


@dataclass(slots=True, frozen=True)
class W1BusDefinition:
    config_class: Type[W1BusConfig] = W1BusConfig
    driver_class: Type[W1Bus] = W1Bus


definition = W1BusDefinition()
