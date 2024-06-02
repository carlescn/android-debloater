import logging

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
