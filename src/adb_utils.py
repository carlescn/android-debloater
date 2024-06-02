import logging

from src.logging import logging_utils

ADB_COMMAND  = ["adb"]  # TODO: set this depending on environment

START_SERVER = ["start-server"]
KILL_SERVER  = ["kill-server"]

LIST_DEVICES = ["devices", "-l"]

GET_DEVICE_PROPERTY = ["shell", "getprop"]
DEVICE_PROPERTY_RELEASE     = "ro.build.version.release"
DEVICE_PROPERTY_NAME        = "ro.product.name"
DEVICE_PROPERTY_MARKET_NAME = "ro.product.marketname"

LIST_PACKAGES = ["shell", "pm", "list", "packages"]
# By default, it returns the installed packages list. Option "-i" means show the installer.
LIST_OPT_UNINSTALLED = ["-u"]
LIST_OPT_SYSTEM      = ["-d"]
LIST_OPT_DISABLED    = ["-s"]

PACKAGE_MANAGER   = ["shell", "pm"]
INSTALL_OPT_USER  = ["--user", "0"]
INSTALL_OPT_KEEP  = ["-k"]

log = logging.getLogger(__name__)


# ADB server

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


# Devices

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


def __get_device_property(serial: str, prop: str) -> str | None:
    cmd = ADB_COMMAND + ["-s", serial] + GET_DEVICE_PROPERTY + [prop]

    try:
        output = logging_utils.subprocess_with_logging(cmd, log)
    except OSError:
        log.exception("Something went wrong getting device property '%s'", prop)
        return None

    if len(output) == 1 and output[0] == "":
        log.error("Device property '%s' did not return anything", prop)
        return None

    return output[0]


def get_device_release(serial: str) -> str | None:
    log.debug("Getting device release version")
    return __get_device_property(serial, DEVICE_PROPERTY_RELEASE)


def get_device_name(serial: str) -> str | None:
    log.debug("Getting device name")
    market_name = __get_device_property(serial, DEVICE_PROPERTY_MARKET_NAME)
    name = __get_device_property(serial, DEVICE_PROPERTY_NAME)

    return name if market_name is None else market_name


# Packages (list)

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


# Packages (command)

def __run_command(command: list[str], error_message: str = "Something went wrong!") -> None:
    try:
        logging_utils.subprocess_with_logging(command, log)
    except OSError:
        log.exception(error_message)


def __get_uninstall_command(serial: str, release: str) -> list[str]:
    cmd = ADB_COMMAND + ["-s", serial]
    match release:
        # TODO: set correct options depending on release version
        case _: cmd += PACKAGE_MANAGER + ["uninstall"] + INSTALL_OPT_USER + INSTALL_OPT_KEEP
    return cmd


def __get_reinstall_command(serial: str, release: str) -> list[str]:
    cmd = ADB_COMMAND + ["-s", serial]
    match release:
        # TODO: set correct options depending on release version
        case _: cmd += PACKAGE_MANAGER + ["install-existing"]
    return cmd


def __get_disable_command(serial: str, release: str) -> list[str]:
    cmd = ADB_COMMAND + ["-s", serial]
    match release:
        # TODO: set correct options depending on release version
        case _: cmd += PACKAGE_MANAGER + ["disable-user"] + INSTALL_OPT_USER
    return cmd


def __get_enable_command(serial: str, release: str) -> list[str]:
    cmd = ADB_COMMAND + ["-s", serial]
    match release:
        # TODO: set correct options depending on release version
        case _: cmd += PACKAGE_MANAGER + ["enable"]
    return cmd


def uninstall_package(serial: str, release: str, package: str) -> None:
    log.info("Uninstalling package: %s", package)
    cmd = __get_uninstall_command(serial, release) + [package]
    __run_command(cmd)


def reinstall_package(serial: str, release: str, package: str) -> None:
    log.info("Reinstalling package: %s", package)
    cmd = __get_reinstall_command(serial, release) + [package]
    __run_command(cmd)


def disable_package(serial: str, release: str, package: str) -> None:
    log.info("Disabling package: %s", package)
    cmd = __get_disable_command(serial, release) + [package]
    __run_command(cmd)


def enable_package(serial: str, release: str, package: str) -> None:
    log.info("Enabling package: %s", package)
    cmd = __get_enable_command(serial, release) + [package]
    __run_command(cmd)
