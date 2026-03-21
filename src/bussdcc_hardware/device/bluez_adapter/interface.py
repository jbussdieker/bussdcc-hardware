from typing import Any, Protocol


class BlueZAdapterInterface(Protocol):
    @property
    def path(self) -> str: ...

    @property
    def advertising_manager(self) -> Any: ...

    @property
    def gatt_manager(self) -> Any: ...
