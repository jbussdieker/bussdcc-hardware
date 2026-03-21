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
        self._interfaces: dict[str, Any] = {}

    def connect(self) -> None:
        self._bus = dbus.SystemBus()

        path = f"/org/bluez/{self.config.adapter}"
        obj = self._bus.get_object(BLUEZ_SERVICE_NAME, "/")
        om = dbus.Interface(obj, DBUS_OM_IFACE)
        objects = om.GetManagedObjects()

        if path not in objects:
            raise RuntimeError(f"BlueZ adapter not found: {self.config.adapter}")

        interfaces = objects[path]
        if ADAPTER_IFACE not in interfaces:
            raise RuntimeError(f"Path is not a BlueZ adapter: {path}")

        self._adapter_path = path
        self._interfaces = dict(interfaces)

    def disconnect(self) -> None:
        self._interfaces = {}
        self._adapter_path = None
        self._bus = None

    def protocol(self) -> BlueZAdapterInterface:
        return self

    def adapter_path(self) -> str:
        if self._adapter_path is None:
            raise RuntimeError("BlueZ adapter not connected")
        return self._adapter_path

    def has_advertising_manager(self) -> bool:
        return LE_ADVERTISING_MANAGER_IFACE in self._interfaces

    def has_gatt_manager(self) -> bool:
        return GATT_MANAGER_IFACE in self._interfaces

    def status(self) -> dict[str, Any]:
        return {
            "device": self.id,
            "adapter": self.config.adapter,
            "path": self._adapter_path,
            "advertising_manager": self.has_advertising_manager(),
            "gatt_manager": self.has_gatt_manager(),
        }
