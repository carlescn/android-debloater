import logging

from src.logging import logging_utils

ADB_COMMAND  = ["adb"]  # TODO: set this depending on environment

START_SERVER = ["start-server"]
KILL_SERVER  = ["kill-server"]

LIST_DEVICES = ["devices", "-l"]

LIST_PACKAGES = ["shell", "pm", "list", "packages"]
# By default, it returns the installed packages list. Option "-i" means show the installer.
LIST_OPT_UNINSTALLED = ["-u"]
LIST_OPT_SYSTEM      = ["-d"]
LIST_OPT_DISABLED    = ["-s"]

UNINSTALL_PACKAGE  = ["shell", "pm", "uninstall"]
UNINSTALL_OPT_USER = ["--user 0"]
UNINSTALL_OPT_KEEP = ["-k"]

log = logging.getLogger(__name__)


def start_server() -> None:
    cmd = ADB_COMMAND + START_SERVER

    log.info("Starting ADB server")
    try:
        logging_utils.subprocess_with_logging(cmd, log)
        log.debug("ADB server started")
    except OSError:
        log.exception("Could not start ADB server")
        # TODO: handle this?


def kill_server() -> None:
    cmd = ADB_COMMAND + KILL_SERVER

    log.info("Killing ADB server")
    try:
        logging_utils.subprocess_with_logging(cmd, log)
        log.debug("ADB server killed")
    except OSError:
        log.exception("Could not kill ADB server")
        # TODO: handle this?


def list_devices() -> list[str]:
    cmd = ADB_COMMAND + LIST_DEVICES

    log.debug("Listing devices")
    try:
        output = logging_utils.subprocess_with_logging(cmd, log)
    except OSError:
        log.exception("Could not list devices")
        return []

    if len(output) < 3:
        log.error("No devices detected")
        return []

    # first and last line do not carry device info
    return [line.strip() for line in output[1:-1]]


def __list_packages(serial: str, options: list[str] | None = None) -> list[str]:
    options = [] if options is None else options

    cmd = ADB_COMMAND + ["-s", serial] + LIST_PACKAGES + options

    try:
        output = logging_utils.subprocess_with_logging(cmd, log)
    except OSError:
        log.exception("Something went wrong when listing packages")
        return []

    return [line.strip().split(":")[-1] for line in output]


def list_packages_installed(serial: str) -> list[str]:
    log.debug("Listing installed packages")
    return __list_packages(serial, None)


def list_packages_uninstalled(serial: str) -> list[str]:
    log.debug("Listing uninstalled packages")
    return __list_packages(serial, LIST_OPT_UNINSTALLED)


def list_packages_system(serial: str) -> list[str]:
    log.debug("Listing system packages")
    return __list_packages(serial, LIST_OPT_SYSTEM)


def list_packages_disabled(serial: str) -> list[str]:
    log.debug("Listing disabled packages")
    return __list_packages(serial, LIST_OPT_DISABLED)


# def uninstall_apk() -> None:
#     cmd = ADB_COMMAND + UNINSTALL
