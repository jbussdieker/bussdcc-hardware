from pathlib import Path
from typing import Iterable

from bussdcc.device import Device


class W1Bus(Device):
    kind = "bus"

    def __init__(self, *, id: str, base_path: str = "/sys/bus/w1/devices"):
        super().__init__(id=id)
        self.base_path = Path(base_path)

    def connect(self) -> None:
        if not self.base_path.exists():
            raise RuntimeError("1-Wire bus not available")

    def disconnect(self) -> None:
        pass

    def discover(self) -> Iterable[str]:
        return [
            p.name
            for p in self.base_path.iterdir()
            if p.is_dir() and p.name.startswith("28-")
        ]

    def device_path(self, device_id: str) -> Path:
        return self.base_path / device_id
