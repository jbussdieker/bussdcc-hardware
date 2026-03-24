from dataclasses import dataclass, field


@dataclass(slots=True)
class MockTemperatureConfig:
    value: float = field(
        default=22.0,
        metadata={
            "label": "Base Temperature",
            "group": "Simulation",
            "step": 0.1,
        },
    )

    jitter: float = field(
        default=0.0,
        metadata={
            "label": "Random Jitter",
            "group": "Simulation",
            "help": "Maximum random variation added to each reading (+/- jitter)",
            "min": 0.0,
            "step": 0.1,
        },
    )

    drift_per_second: float = field(
        default=0.0,
        metadata={
            "label": "Drift Per Second",
            "group": "Simulation",
            "help": "Linear drift added over time",
            "step": 0.001,
        },
    )

    min_value: float = field(
        default=-40.0,
        metadata={
            "label": "Minimum Temperature",
            "group": "Simulation",
            "step": 0.1,
        },
    )

    max_value: float = field(
        default=125.0,
        metadata={
            "label": "Maximum Temperature",
            "group": "Simulation",
            "step": 0.1,
        },
    )
