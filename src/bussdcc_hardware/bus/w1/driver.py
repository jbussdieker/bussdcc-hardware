from typing import Iterable, Optional, Any
from pathlib import Path

from bussdcc import Device

from .config import W1BusConfig


class W1Bus(Device[W1BusConfig]):
    kind = "bus"

    def __init__(self, *, id: str, config: W1BusConfig):
        super().__init__(id=id, config=config)
        self.base_path = Path(config.base_path)

    def connect(self) -> None:
        if not self.base_path.exists():
            raise RuntimeError("1-Wire bus not available")

    def disconnect(self) -> None:
        pass

    def discover_devices(self) -> Iterable[str]:
        return [
            p.name
            for p in self.base_path.iterdir()
            if p.is_dir() and p.name.startswith("28-")
        ]

    def device_path(self, device_id: str) -> Path:
        return Path(self.base_path / device_id)
