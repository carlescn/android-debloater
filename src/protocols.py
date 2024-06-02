from typing import Protocol

from src.device import Device


class DeviceGetter(Protocol):
    def get_active_device(self) -> Device | None:
        pass


class DeviceSetter(Protocol):
    def set_active_device(self, serial: str) -> None:
        pass


class DeviceManager(DeviceGetter, DeviceSetter):
    def update_devices(self) -> None:
        pass


class PackageManager(Protocol):
    pass
