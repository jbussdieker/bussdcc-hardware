from functools import lru_cache
from typing import Any

from bussdcc import Device

from .config import BlueZAdapterConfig
from .interface import BlueZAdapterInterface

try:
    import dbus  # type: ignore[import-not-found]
except ImportError as e:  # pragma: no cover
    raise RuntimeError(
        "BlueZAdapter requires python3-dbus and BlueZ system packages"
    ) from e


BLUEZ_SERVICE_NAME = "org.bluez"
DBUS_OM_IFACE = "org.freedesktop.DBus.ObjectManager"
ADAPTER_IFACE = "org.bluez.Adapter1"
LE_ADVERTISING_MANAGER_IFACE = "org.bluez.LEAdvertisingManager1"
GATT_MANAGER_IFACE = "org.bluez.GattManager1"


class BlueZAdapter(Device[BlueZAdapterConfig], BlueZAdapterInterface):
    kind = "bluetooth"

    def __init__(self, *, id: str, config: BlueZAdapterConfig):
        super().__init__(id=id, config=config)
        self._bus: dbus.SystemBus | None = None
        self._adapter_path: str | None = None

    def connect(self) -> None:
        self._bus = dbus.SystemBus()
        path = f"/org/bluez/{self.config.adapter}"

        objects = self._object_manager().GetManagedObjects()

        if path not in objects:
            raise RuntimeError(f"BlueZ adapter not found: {self.config.adapter}")

        if ADAPTER_IFACE not in objects[path]:
            raise RuntimeError(f"Path is not a BlueZ adapter: {path}")

        self._adapter_path = path
        self._clear_caches()

    def disconnect(self) -> None:
        self._clear_caches()
        self._adapter_path = None
        self._bus = None

    def protocol(self) -> BlueZAdapterInterface:
        return self

    @property
    def bus(self) -> dbus.SystemBus:
        if self._bus is None:
            raise RuntimeError("BlueZ adapter not connected")
        return self._bus

    @property
    def path(self) -> str:
        if self._adapter_path is None:
            raise RuntimeError("BlueZ adapter not connected")
        return self._adapter_path

    @property
    def advertising_manager(self) -> Any:
        return self._interface(LE_ADVERTISING_MANAGER_IFACE)

    @property
    def gatt_manager(self) -> Any:
        return self._interface(GATT_MANAGER_IFACE)

    def _clear_caches(self) -> None:
        self._object_manager.cache_clear()
        self._adapter_object.cache_clear()
        self._interface.cache_clear()

    @lru_cache(maxsize=1)
    def _object_manager(self) -> Any:
        obj = self.bus.get_object(BLUEZ_SERVICE_NAME, "/")
        return dbus.Interface(obj, DBUS_OM_IFACE)

    @lru_cache(maxsize=1)
    def _adapter_object(self) -> Any:
        return self.bus.get_object(BLUEZ_SERVICE_NAME, self.path)

    @lru_cache(maxsize=None)
    def _interface(self, name: str) -> Any:
        return dbus.Interface(self._adapter_object(), name)
