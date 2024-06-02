from collections.abc import Iterable
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
    def update_packages(self) -> None:
        pass

    def reinstall_packages(self, package_ids: Iterable[str]) -> None:
        pass

    def uninstall_packages(self, package_ids: Iterable[str]) -> None:
        pass

    def enable_packages(self, package_ids: Iterable[str]) -> None:
        pass

    def disable_packages(self, package_ids: Iterable[str]) -> None:
        pass
