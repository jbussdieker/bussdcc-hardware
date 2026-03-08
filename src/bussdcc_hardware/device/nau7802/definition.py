from dataclasses import dataclass
from typing import Type

from .config import NAU7802Config
from .driver import NAU7802


@dataclass(slots=True, frozen=True)
class NAU7802Definition:
    config_class: Type[NAU7802Config] = NAU7802Config
    driver_class: Type[NAU7802] = NAU7802


definition = NAU7802Definition()
