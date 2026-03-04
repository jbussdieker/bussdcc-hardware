from typing import Iterable, cast, Optional, Any
import smbus2

from nau7802.protocol import BusProtocol

from bussdcc.device import Device


class I2CBus(Device):
    kind = "bus"

    def __init__(self, *, id: str, config: Optional[dict[str, Any]] = None):
        super().__init__(id=id, config=config)

        self.bus_num = self.config.get("bus", 1)
        self._bus: smbus2.SMBus | None = None

    def connect(self) -> None:
        self._bus = smbus2.SMBus(self.bus_num)

    def disconnect(self) -> None:
        if self._bus:
            self._bus.close()
            self._bus = None

    def protocol(self) -> BusProtocol | None:
        if not self._bus:
            return None

        return cast(BusProtocol, self._bus)

    def discover(self) -> Iterable[int]:
        if not self._bus:
            return []

        found = []
        for addr in range(0x03, 0x78):
            try:
                # Read a single byte without specifying a register
                msg = smbus2.i2c_msg.read(addr, 1)
                self._bus.i2c_rdwr(msg)
                found.append(addr)
            except OSError:
                pass
        return found
