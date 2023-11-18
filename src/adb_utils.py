import logging

from src.logging.logging_utils import LoggingUtils


class AdbUtils:
    BASE          = "base"
    START_SERVER  = "start_server"
    KILL_SERVER   = "kill_server"
    LIST_DEVICES  = "list_devices"
    LIST_PACKAGES_I = "list_installed_packages"
    LIST_PACKAGES_U = "list_uninstalled_packages"

    __params = {
        BASE           : [],
        START_SERVER   : ["start-server"],
        KILL_SERVER    : ["kill-server"],
        LIST_DEVICES   : ["devices", "-l"],
        LIST_PACKAGES_I: ["shell", "pm", "list", "packages"],
        LIST_PACKAGES_U: ["shell", "pm", "list", "packages", "-u"],
    }

    __adb_cmd = "adb"  # TODO: set this depending on environment

    def __init__(self):
        self.__log = logging.getLogger(__name__)

    def get_cmd(self, command: str = BASE) -> list[str]:
        params = self.__params.get(command)
        return [self.__adb_cmd] + params

    def get_cmd_with_serial(self, command: str, serial: str = None) -> list[str]:
        params = ["-s", serial] + self.__params.get(command)
        return [self.__adb_cmd] + params

    def start_server(self):
        cmd = self.get_cmd(self.START_SERVER)

        self.__log.info("Starting ADB server")
        self.__log.debug("Running command: %s", " ".join(cmd))
        try:
            LoggingUtils.subprocess_with_logging(cmd, self.__log)
            self.__log.debug("ADB server started")
        except OSError:
            self.__log.exception("Could not start ADB server")
            # TODO: handle this?

    def kill_server(self):
        cmd = self.get_cmd(self.KILL_SERVER)

        self.__log.info("Killing ADB server")
        self.__log.debug("Running command: %s", " ".join(cmd))
        try:
            LoggingUtils.subprocess_with_logging(cmd, self.__log)
            self.__log.debug("ADB server killed")
        except OSError:
            self.__log.exception("Could not kill ADB server")
            # TODO: handle this?

    def list_devices(self) -> list[str]:
        cmd = self.get_cmd(self.LIST_DEVICES)

        self.__log.debug("Listing devices")
        self.__log.debug("Running command: %s", " ".join(cmd))
        try:
            output = LoggingUtils.subprocess_with_logging(cmd, self.__log)
        except OSError:
            self.__log.exception("Could not update devices")
            return []

        # first and last line are only cosmetic
        return [line.strip() for line in output[1:-1]]

    def list_packages(self, serial: str, params: str = LIST_PACKAGES_I) -> list[str]:
        cmd = self.get_cmd_with_serial(params, serial)

        self.__log.debug("Listing packages")
        self.__log.debug("Running command: %s", " ".join(cmd))
        try:
            output = LoggingUtils.subprocess_with_logging(cmd, self.__log)
        except OSError:
            self.__log.exception("Something went wrong when listing packages")
            return []

        return [line.strip() for line in output]
