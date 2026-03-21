from typing import Any
from dataclasses import dataclass, field


@dataclass(slots=True)
class BlueZAdapterConfig:
    adapter: str = field(
        default="hci0",
        metadata={
            "label": "Bluetooth Adapter",
            "group": "Connection",
            "ui": "text",
            "help": "BlueZ adapter name such as hci0",
        },
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BlueZAdapterConfig":
        return cls(adapter=data.get("adapter", "hci0"))
