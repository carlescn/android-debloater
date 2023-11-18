import logging

from src.adb_utils import AdbUtils
from src.package import Package


class PackageManager:
    def __init__(self):
        self.__log = logging.getLogger(__name__)
        self.__adb = AdbUtils()

        self.__serial: str = None
        self.__packages: list[Package] = []

    def set_device(self, serial: str) -> None:
        self.__serial = serial
        self.clear_packages()
        self.__log.debug("Set package manager device to '%s'", serial)

    def get_packages(self) -> list[Package]:
        return self.__packages

    def clear_packages(self) -> None:
        self.__packages = []
        self.__log.debug("Emptied packages list from package manager")

    def update_packages(self) -> None:
        installed   = self.__adb.list_packages(self.__serial, AdbUtils.LIST_PACKAGES_I)
        uninstalled = self.__adb.list_packages(self.__serial, AdbUtils.LIST_PACKAGES_U)
        uninstalled = list(set(uninstalled) - set(installed))

        installed_packages  : list[Package] = [self.__get_package_from_str(p, "installed") for p in installed]
        uninstalled_packages: list[Package] = [self.__get_package_from_str(p, "uninstalled") for p in uninstalled]

        self.__packages = installed_packages + uninstalled_packages

        self.__log.info("Packages updated: found " +
                        f"{len(installed_packages):d} installed, " +
                        f"{len(uninstalled_packages):d} uninstalled")
        for package in self.__packages:
            self.__log.debug("Package added: %s", package)

    @staticmethod
    def __get_package_from_str(string: str, status: str) -> Package:
        full_name = string.split(":")[-1]

        return Package(full_name=full_name,
                       short_name=full_name.split(".")[-1],
                       status=status)
