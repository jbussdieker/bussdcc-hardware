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
