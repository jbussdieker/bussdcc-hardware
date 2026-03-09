from typing import Literal, Optional, Any
import threading
import time

from bussdcc.device import Device
from bussdcc.message import DeviceFailed
from nau7802 import NAU7802 as _NAU7802
from typed_registers import SMBusRegisterBus

from ...bus.i2c import I2CBus

from .config import NAU7802Config


class NAU7802(Device[NAU7802Config]):
    kind = "adc"

    def __init__(self, *, id: str, config: NAU7802Config):
        super().__init__(id=id, config=config)
        self._current_channel: int | None = None
        self._lock = threading.Lock()

    def connect(self) -> None:
        if not self.ctx:
            raise RuntimeError("Device not attached")

        runtime = self.ctx.runtime
        bus = runtime.devices.get(self.config.bus_id)

        if not isinstance(bus, I2CBus):
            raise RuntimeError("NAU7802 requires an I2CBus")

        self.bus: I2CBus = bus

        protocol: SMBusRegisterBus | None = bus.protocol()

        if protocol:
            self.device = _NAU7802(protocol, self.config.addr)

        with self._lock:
            self.device.initialize()
            self.device.set_crs(3)
            self.device.set_gain(7)

    def disconnect(self) -> None:
        pass

    def _wait_ready(self) -> bool:
        if not self.ctx:
            return False

        timeout = self.ctx.clock.monotonic() + 0.15  # at a minimum we expect 10 SPS
        while not self.device.cycle_ready:
            self.ctx.clock.sleep(0.001)
            if self.ctx.clock.monotonic() > timeout:
                return False
        return True

    def _switch_channel(self, channel: Literal[1, 2]) -> bool:
        if not self.ctx:
            return False
        if self._current_channel == channel:
            return True

        self.device.set_channel(channel)

        # Discard 10 samples after changing channels
        for n in range(1, 10):
            if not self._wait_ready():
                self.ctx.emit(
                    DeviceFailed(
                        device=self.id,
                        kind=self.kind,
                        error="timeout changing channels",
                    )
                )
                return False
            self.device.adco

        self._current_channel = channel
        return True

    def read(self, channel: Literal[1, 2]) -> int | None:
        if not self._switch_channel(channel):
            self.set_offline()
            return None

        with self._lock:
            try:
                value = self.device.adco.value
            except Exception as e:
                self.set_offline(e)
                return None

        self.set_online()
        return value
