import logging

from src.logging.logging_utils import LoggingUtils


class AdbUtils:
    START_SERVER      = 10
    KILL_SERVER       = 11
    LIST_DEVICES      = 20
    LIST_INSTALLED    = 30
    LIST_UNINSTALLED  = 31
    LIST_SYSTEM       = 32
    LIST_DISABLED     = 33

    __params = {
        START_SERVER    : ["start-server"],
        KILL_SERVER     : ["kill-server"],
        LIST_DEVICES    : ["devices", "-l"],
        LIST_INSTALLED  : ["shell", "pm", "list", "packages"],  # "-i" means show the installer
        LIST_UNINSTALLED: ["shell", "pm", "list", "packages", "-u"],
        LIST_DISABLED   : ["shell", "pm", "list", "packages", "-d"],
        LIST_SYSTEM     : ["shell", "pm", "list", "packages", "-s"],
    }

    __adb_cmd = "adb"  # TODO: set this depending on environment

    def __init__(self):
        self.__log = logging.getLogger(__name__)

    def get_cmd(self, options: int) -> list[str]:
        return [self.__adb_cmd] + self.__params.get(options, [])

    def get_cmd_with_serial(self, options: int, serial: str = None) -> list[str]:
        return [self.__adb_cmd, "-s", serial] + self.__params.get(options, [])

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
            self.__log.exception("Could not list devices")
            return []

        if len(output) < 3:
            self.__log.error("No devices detected")
            return []

        # first and last line do not carry device info
        return [line.strip() for line in output[1:-1]]

    def list_packages(self, serial: str, options: int = LIST_INSTALLED) -> list[str]:
        cmd = self.get_cmd_with_serial(options, serial)

        self.__log.debug("Listing packages")
        self.__log.debug("Running command: %s", " ".join(cmd))
        try:
            output = LoggingUtils.subprocess_with_logging(cmd, self.__log)
        except OSError:
            self.__log.exception("Something went wrong when listing packages")
            return []

        return [line.strip().split(":")[-1] for line in output]
