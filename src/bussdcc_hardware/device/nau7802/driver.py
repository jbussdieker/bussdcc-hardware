from typing import Literal, Any
import threading

from bussdcc.device import Device
from bussdcc.message import DeviceFailed
from nau7802 import NAU7802 as _NAU7802
from typed_registers import SMBusRegisterBus

from ...bus.i2c.driver import I2CBus
from .config import NAU7802Config

Channel = Literal[1, 2]


class NAU7802(Device[NAU7802Config]):
    kind = "adc"

    ADC_MAX = 8388607
    ADC_MIN = -8388608

    GAIN_MAP = {
        1: 0,
        2: 1,
        4: 2,
        8: 3,
        16: 4,
        32: 5,
        64: 6,
        128: 7,
    }

    CRS_MAP = {
        10: 0,
        20: 1,
        40: 2,
        80: 3,
        320: 7,
    }

    def __init__(self, *, id: str, config: NAU7802Config):
        super().__init__(id=id, config=config)

        self._lock = threading.Lock()
        self._current_channel: Channel | None = None

        # runtime tare offsets
        self._tare: dict[Channel, int] = {1: 0, 2: 0}

        self.device: _NAU7802 | None = None
        self.bus: I2CBus | None = None

    # ---------------------------------------------------------
    # lifecycle
    # ---------------------------------------------------------

    def connect(self) -> None:
        if not self.ctx:
            raise RuntimeError("Device not attached")

        runtime = self.ctx.runtime
        bus = runtime.devices.get(self.config.bus_id)

        if not isinstance(bus, I2CBus):
            raise RuntimeError("NAU7802 requires an I2CBus")

        protocol: SMBusRegisterBus | None = bus.protocol()
        if protocol is None:
            raise RuntimeError("I2C bus not ready")

        self.bus = bus
        self.device = _NAU7802(protocol, self.config.addr)

        with self._lock:
            self.device.initialize()
            self.device.set_gain(self.GAIN_MAP[self.config.gain])
            self.device.set_crs(self.CRS_MAP[self.config.sample_rate])

    def disconnect(self) -> None:
        self.device = None
        self.bus = None

    # ---------------------------------------------------------
    # hardware helpers
    # ---------------------------------------------------------

    def _wait_ready(self) -> bool:
        if not self.ctx or not self.device:
            return False

        timeout = self.ctx.clock.monotonic() + 0.2

        while not self.device.cycle_ready:
            self.ctx.clock.sleep(0.001)
            if self.ctx.clock.monotonic() > timeout:
                return False

        return True

    def _switch_channel(self, channel: Channel) -> bool:
        if not self.device:
            return False

        if self._current_channel == channel:
            return True

        self.device.set_channel(channel)

        # discard unstable readings after channel switch
        for _ in range(self.config.discard_samples):
            if not self._wait_ready():
                return False
            _ = self.device.adco.value

        self._current_channel = channel
        return True

    # ---------------------------------------------------------
    # raw reading
    # ---------------------------------------------------------

    def read_raw(self, channel: Channel) -> int | None:
        if not self.device:
            return None

        if not self._switch_channel(channel):
            self.set_offline()
            return None

        samples = max(1, self.config.samples)

        total = 0

        with self._lock:
            for _ in range(samples):
                if not self._wait_ready():
                    self.set_offline()
                    return None

                try:
                    value = self.device.adco.value
                except Exception as e:
                    self.set_offline(e)
                    return None

                total += value

        raw = int(total / samples)

        # detect ADC saturation
        if raw >= self.ADC_MAX or raw <= self.ADC_MIN:
            if self.ctx:
                self.ctx.emit(
                    DeviceFailed(
                        device=self.id,
                        kind=self.kind,
                        error="ADC saturation",
                    )
                )

        self.set_online()
        return raw

    # ---------------------------------------------------------
    # calibrated reading
    # ---------------------------------------------------------

    def read(self, channel: Channel) -> float | None:
        raw = self.read_raw(channel)
        if raw is None:
            return None

        value = float(raw)

        ch = self.config.channels.get(channel)
        if not ch:
            return value

        cal = ch.calibration

        value -= self._tare[channel]
        value -= cal.offset
        value *= cal.scale

        return float(value)

    # ---------------------------------------------------------
    # runtime operations
    # ---------------------------------------------------------

    def tare(self, channel: Channel) -> None:
        raw = self.read_raw(channel)
        if raw is not None:
            self._tare[channel] = raw

    def clear_tare(self, channel: Channel) -> None:
        self._tare[channel] = 0

    # ---------------------------------------------------------
    # diagnostics
    # ---------------------------------------------------------

    def status(self) -> dict[str, Any]:
        return {
            "device": self.id,
            "channel": self._current_channel,
            "tare": self._tare,
            "samples": self.config.samples,
        }
