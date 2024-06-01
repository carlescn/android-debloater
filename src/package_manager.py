import logging

from src import adb_utils
from src import event_handler
from src.event import Event
from src.package import Package

log = logging.getLogger(__name__)


class PackageManager:
    def __init__(self):
        self.__register_events()

        self.__serial: str = None
        self.__packages: dict[str, Package] = {}

    def __register_events(self):
        event_handler.register(Event.ACTIVE_DEVICE_UPDATED, self.set_device)
        event_handler.register(Event.PACKAGE_LIST_UPDATE_REQUESTED, self.update_packages)

    def set_device(self, serial: str) -> None:
        self.__serial = serial
        self.clear_packages()
        log.debug("Set package manager device to '%s'", serial)

    def get_packages(self) -> list[Package]:
        return list(self.__packages.values())

    def clear_packages(self) -> None:
        self.__packages = {}
        log.debug("Emptied packages list from package manager")

    def update_packages(self) -> None:
        if self.__serial is None:
            log.error("Not updating packages because device is not set")
            return

        # uninstalled returns both installed and uninstalled packages
        uninstalled = adb_utils.list_packages_uninstalled(self.__serial)
        self.__packages = {p: Package(full_name=p, installed=False) for p in uninstalled}

        # installed returns only the installed packages
        installed = adb_utils.list_packages_installed(self.__serial)
        for p in installed:
            self.__packages.get(p).installed = True

        disabled = adb_utils.list_packages_disabled(self.__serial)
        for p in disabled:
            self.__packages.get(p).disabled = True

        system = adb_utils.list_packages_system(self.__serial)
        for p in system:
            self.__packages.get(p).system = True

        log.info("Packages updated: found " +
                 f"{len(installed):d} installed, " +
                 f"{len(uninstalled) - len(installed):d} uninstalled, " +
                 f"{len(disabled):d} disabled")
        for package in self.__packages.values():
            log.debug("Package added: %s", package)

        event_handler.fire(Event.PACKAGE_LIST_UPDATED, packages=self.get_packages())
