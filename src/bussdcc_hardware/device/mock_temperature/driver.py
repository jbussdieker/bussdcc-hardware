import random

from bussdcc import Device

from .config import MockTemperatureConfig


class MockTemperature(Device[MockTemperatureConfig]):
    kind = "temperature"

    def __init__(self, *, id: str, config: MockTemperatureConfig):
        super().__init__(id=id, config=config)
        self._started_at: float | None = None

    def connect(self) -> None:
        if not self.ctx:
            raise RuntimeError("Device not attached")

        self._started_at = self.ctx.clock.monotonic()
        self.set_online()

    def disconnect(self) -> None:
        self._started_at = None

    def read(self) -> float | None:
        if not self.ctx or self._started_at is None:
            return None

        elapsed = self.ctx.clock.monotonic() - self._started_at

        value = self.config.value
        value += elapsed * self.config.drift_per_second

        if self.config.jitter > 0:
            value += random.uniform(-self.config.jitter, self.config.jitter)

        value = max(self.config.min_value, min(self.config.max_value, value))

        self.set_online()
        return float(value)
