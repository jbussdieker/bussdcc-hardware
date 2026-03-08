from dataclasses import dataclass
from typing import Type

from .config import DS18B20Config
from .driver import DS18B20


@dataclass(slots=True, frozen=True)
class DS18B20Definition:
    config_class: Type[DS18B20Config] = DS18B20Config
    driver_class: Type[DS18B20] = DS18B20


definition = DS18B20Definition()
