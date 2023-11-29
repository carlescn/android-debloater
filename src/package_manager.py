import logging

from src.adb_utils import AdbUtils
from src.package import Package


class PackageManager:
    def __init__(self):
        self.__log = logging.getLogger(__name__)
        self.__adb = AdbUtils()

        self.__serial: str = None
        self.__packages: dict[str, Package] = {}

    def set_device(self, serial: str) -> None:
        self.__serial = serial
        self.clear_packages()
        self.__log.debug("Set package manager device to '%s'", serial)

    def get_packages(self) -> list[Package]:
        return list(self.__packages.values())

    def clear_packages(self) -> None:
        self.__packages = {}
        self.__log.debug("Emptied packages list from package manager")

    def update_packages(self) -> None:
        if self.__serial is None:
            self.__log.error("Not updating packages because device is not set")
            return

        # uninstalled returns both installed and uninstalled packages
        uninstalled = self.__adb.list_packages(self.__serial, AdbUtils.LIST_UNINSTALLED)
        self.__packages = {p: Package(full_name=p, installed=False) for p in uninstalled}

        # installed returns only the installed packages
        installed = self.__adb.list_packages(self.__serial, AdbUtils.LIST_INSTALLED)
        for p in installed:
            self.__packages.get(p).installed = True

        disabled = self.__adb.list_packages(self.__serial, AdbUtils.LIST_DISABLED)
        for p in disabled:
            self.__packages.get(p).disabled = True

        system = self.__adb.list_packages(self.__serial, AdbUtils.LIST_SYSTEM)
        for p in system:
            self.__packages.get(p).system = True

        self.__log.info("Packages updated: found " +
                        f"{len(installed):d} installed, " +
                        f"{len(uninstalled) - len(installed):d} uninstalled, " +
                        f"{len(disabled):d} disabled")
        for package in self.__packages.values():
            self.__log.debug("Package added: %s", package)
