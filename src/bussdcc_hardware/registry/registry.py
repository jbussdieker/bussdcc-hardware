from importlib import metadata
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class RegistryEntry:
    name: str
    definition: Any | None
    available: bool
    error: Exception | None = None


class DeviceRegistry:
    def __init__(self) -> None:
        self.devices = self._load_entry_points("bussdcc.device")

    def _load_entry_points(self, group: str) -> dict[str, RegistryEntry]:
        result = {}

        for ep in metadata.entry_points(group=group):
            try:
                definition = ep.load()

                result[ep.name] = RegistryEntry(
                    name=ep.name,
                    definition=definition,
                    available=True,
                    error=None,
                )

            except Exception as e:
                result[ep.name] = RegistryEntry(
                    name=ep.name,
                    definition=None,
                    available=False,
                    error=e,
                )

        return result
