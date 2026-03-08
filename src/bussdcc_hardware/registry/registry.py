from importlib import metadata


class DeviceRegistry:
    def __init__(self) -> None:
        self.buses = self._load_entry_points("bussdcc.bus")
        self.devices = self._load_entry_points("bussdcc.device")

    def _load_entry_points(self, group: str) -> dict[str, object]:
        eps = metadata.entry_points()
        return {ep.name: ep.load() for ep in eps.select(group=group)}
