import logging
from collections.abc import Iterable
from typing import Callable

from src import adb_utils
from src import event_handler
from src.event import Event
from src.package import Package
from src.protocols import DeviceGetter


log = logging.getLogger(__name__)


class PackageManager:
    def __init__(self, device_getter: DeviceGetter):
        self.__register_events()

        self.__device_getter = device_getter
        self.__packages: dict[str, Package] = {}

    def __register_events(self):
        event_handler.register(Event.ACTIVE_DEVICE_UPDATED, self.clear_packages)

    def get_packages(self) -> list[Package]:
        return list(self.__packages.values())

    def clear_packages(self) -> None:
        self.__packages = {}
        log.debug("Emptied packages list from package manager")

    def update_packages(self) -> None:
        device = self.__device_getter.get_active_device()
        if device is None:
            log.error("Not updating packages because device is not set")
            return

        # uninstalled returns both installed and uninstalled packages
        uninstalled = adb_utils.list_packages_uninstalled(device.serial)
        self.__packages = {p: Package(full_name=p, installed=False) for p in uninstalled}

        # installed returns only the installed packages
        installed = adb_utils.list_packages_installed(device.serial)
        for p in installed:
            self.__packages[p].installed = True

        disabled = adb_utils.list_packages_disabled(device.serial)
        for p in disabled:
            self.__packages[p].disabled = True

        system = adb_utils.list_packages_system(device.serial)
        for p in system:
            self.__packages[p].system = True

        log.info("Packages updated: found " +
                 f"{len(installed):d} installed, " +
                 f"{len(uninstalled) - len(installed):d} uninstalled, " +
                 f"{len(disabled):d} disabled")
        for package in self.__packages.values():
            log.debug("Package added: %s", package)

        event_handler.fire(Event.PACKAGE_LIST_UPDATED, packages=self.get_packages())

    def __packages_action(self, method: Callable, package_ids: Iterable[str]) -> None:
        device = self.__device_getter.get_active_device()
        if device is None:
            log.error("Can't continue: active device is not set")
            return

        for package in package_ids:
            method(device.serial, device.release, package)

    def uninstall_packages(self, package_ids: Iterable[str]) -> None:
        log.debug("Uninstalling packages: %s", package_ids)
        self.__packages_action(adb_utils.uninstall_package, package_ids)

    def reinstall_packages(self, package_ids: Iterable[str]) -> None:
        log.debug("Reinstalling packages: %s", package_ids)
        self.__packages_action(adb_utils.reinstall_package, package_ids)

    def disable_packages(self, package_ids: Iterable[str]) -> None:
        log.debug("Disabling packages: %s", package_ids)
        self.__packages_action(adb_utils.disable_package, package_ids)

    def enable_packages(self, package_ids: Iterable[str]) -> None:
        log.debug("Enabling packages: %s", package_ids)
        self.__packages_action(adb_utils.enable_package, package_ids)
