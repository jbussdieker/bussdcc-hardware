from dataclasses import dataclass, field


@dataclass(slots=True)
class MockGPIOBusConfig:
    metadata_only: bool = field(
        default=False,
        metadata={
            "label": "Metadata Only",
            "group": "Simulation",
            "help": "Reserved for future use",
        },
    )
