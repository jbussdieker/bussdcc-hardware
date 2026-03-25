from typing import Literal, Any
import threading

from bussdcc import Device
from bussdcc.message import DeviceFailed
from bme688 import Reading, BME688 as _BME688
from typed_registers import SMBusRegisterBus

from ...bus.i2c.driver import I2CBus
from .config import BME688Config


class BME688(Device[BME688Config]):
    kind = "environmental"

    def __init__(self, *, id: str, config: BME688Config):
        super().__init__(id=id, config=config)

        self.device: _BME688 | None = None
        self.bus: I2CBus | None = None

    def connect(self) -> None:
        if not self.ctx:
            raise RuntimeError("Device not attached")

        runtime = self.ctx.runtime
        bus = runtime.devices.get(self.config.bus_id)

        if not isinstance(bus, I2CBus):
            raise RuntimeError("BME688 requires an I2CBus")

        protocol: SMBusRegisterBus | None = bus.protocol()
        if protocol is None:
            raise RuntimeError("I2C bus not ready")

        self.bus = bus
        self.device = _BME688(protocol, self.config.addr)

        self.device.initialize()

    def disconnect(self) -> None:
        self.device = None
        self.bus = None

    def read(self) -> Reading | None:
        reading = None
        return reading
