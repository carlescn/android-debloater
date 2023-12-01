import logging

from src.logging import logging_utils

ADB_COMMAND       = ["adb"]  # TODO: set this depending on environment
START_SERVER      = ["start-server"]
KILL_SERVER       = ["kill-server"]
LIST_DEVICES      = ["devices", "-l"]
LIST_INSTALLED    = ["shell", "pm", "list", "packages"]  # "-i" means show the installer
LIST_UNINSTALLED  = ["shell", "pm", "list", "packages", "-u"]
LIST_SYSTEM       = ["shell", "pm", "list", "packages", "-d"]
LIST_DISABLED     = ["shell", "pm", "list", "packages", "-s"]

log = logging.getLogger(__name__)


def start_server() -> None:
    cmd = ADB_COMMAND + START_SERVER

    log.info("Starting ADB server")
    log.debug("Running command: %s", " ".join(cmd))
    try:
        logging_utils.subprocess_with_logging(cmd, log)
        log.debug("ADB server started")
    except OSError:
        log.exception("Could not start ADB server")
        # TODO: handle this?


def kill_server() -> None:
    cmd = ADB_COMMAND + KILL_SERVER

    log.info("Killing ADB server")
    log.debug("Running command: %s", " ".join(cmd))
    try:
        logging_utils.subprocess_with_logging(cmd, log)
        log.debug("ADB server killed")
    except OSError:
        log.exception("Could not kill ADB server")
        # TODO: handle this?


def list_devices() -> list[str]:
    cmd = ADB_COMMAND + LIST_DEVICES

    log.debug("Listing devices")
    log.debug("Running command: %s", " ".join(cmd))
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


def list_packages(serial: str, options: list[str] = None) -> list[str]:
    if options is None:
        options = LIST_INSTALLED

    cmd = ADB_COMMAND + ["-s", serial] + options

    log.debug("Listing packages")
    log.debug("Running command: %s", " ".join(cmd))
    try:
        output = logging_utils.subprocess_with_logging(cmd, log)
    except OSError:
        log.exception("Something went wrong when listing packages")
        return []

    return [line.strip().split(":")[-1] for line in output]
