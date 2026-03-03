from typing import Optional

from bussdcc.device import Device


class DS18B20(Device):
    kind = "temperature"

    def __init__(self, *, id: str, uid: str) -> None:
        super().__init__(id=id)
        self._uid = uid

    def connect(self) -> None:
        pass

    def _read_file(self, path: str) -> Optional[str]:
        try:
            with open(path, "r") as f:
                return f.read().strip("\x00").strip()
        except Exception:
            return None

    def get_temperature(self) -> Optional[float]:
        temp_string = self._read_file(f"/sys/bus/w1/devices/{self._uid}/temperature")
        if temp_string is None:
            return None
        return float(temp_string) / 1000
