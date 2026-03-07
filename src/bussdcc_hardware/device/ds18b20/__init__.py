from typing import Optional, Any
from pathlib import Path

from bussdcc.device import Device

from ...bus.w1 import W1Bus


class DS18B20(Device):
    kind = "temperature"

    def __init__(self, *, id: str, config: Optional[dict[str, Any]] = None):
        super().__init__(id=id, config=config)

        self.bus_id = self.config["bus_id"]
        self.device_id = self.config["device_id"]
        self._device_path: Path | None = None

    def connect(self) -> None:
        if not self.ctx:
            raise RuntimeError("Device not attached")

        bus = self.ctx.runtime.devices.get(self.bus_id)
        if not isinstance(bus, W1Bus):
            raise RuntimeError("Failed to find W1Bus")

        self._device_path = bus.device_path(self.device_id)

    def read(self) -> float | None:
        if not self._device_path:
            return None

        temp_file = self._device_path / "temperature"

        try:
            value = temp_file.read_text().strip()
        except FileNotFoundError:
            return None

        return float(value) / 1000
