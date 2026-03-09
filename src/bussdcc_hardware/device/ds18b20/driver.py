from typing import Optional, Any
from pathlib import Path

from bussdcc.device import Device

from ...bus.w1 import W1Bus

from .config import DS18B20Config


class DS18B20(Device[DS18B20Config]):
    kind = "temperature"

    def __init__(self, *, id: str, config: DS18B20Config):
        super().__init__(id=id, config=config)
        self._device_path: Path | None = None

    def connect(self) -> None:
        if not self.ctx:
            raise RuntimeError("Device not attached")

        bus = self.ctx.runtime.devices.get(self.config.bus_id)
        if not isinstance(bus, W1Bus):
            raise RuntimeError("Failed to find W1Bus")

        self._device_path = bus.device_path(self.config.device_id)
        if not self._device_path.exists():
            raise RuntimeError("Failed to find device")

    def read(self) -> float | None:
        if not self._device_path:
            return None

        temp_file = self._device_path / "temperature"

        try:
            value = temp_file.read_text().strip()
        except FileNotFoundError as e:
            self.set_offline(e)
            return None

        try:
            temp = float(value) / 1000
        except ValueError as e:
            self.set_offline(e)
            return None

        self.set_online()
        return temp
