from dataclasses import dataclass, field


@dataclass(slots=True)
class W1BusConfig:
    base_path: str = field(
        default="/sys/bus/w1/devices",
        metadata={
            "label": "Base Path",
            "group": "Connection",
            "required": True,
        },
    )
