from typing import Iterable, cast
import smbus2

from nau7802.protocol import BusProtocol

from bussdcc.device import Device


class I2CBus(Device):
    kind = "bus"

    def __init__(self, *, id: str, bus: int = 1):
        self.bus_num = bus
        self._bus: smbus2.SMBus | None = None
        super().__init__(id=id)

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
