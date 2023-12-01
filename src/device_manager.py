import logging

from src import adb_utils
from src.device import Device

log = logging.getLogger(__name__)


class DeviceManager:
    def __init__(self):
        self.__devices: list[Device] = []
        self.__active_device: Device = None

    def get_devices_serials(self) -> list[str]:
        return [d.serial for d in self.__devices]

    def get_active_device(self) -> Device:
        return self.__active_device

    def get_device_from_serial(self, serial: str) -> Device:
        device = [d for d in self.__devices if d.serial == serial]

        if len(device) == 0:
            log.error("Did not find any device with serial '%s'", serial)
            raise ValueError
        if len(device) > 1:
            log.error("Found more than one device with serial '%s'", serial)
            raise ValueError

        return device[0]

    def set_active_device(self, serial: str) -> None:
        try:
            self.__active_device = self.get_device_from_serial(serial)
            log.info("Active device is set to '%s'", serial)
        except ValueError:
            self.__active_device = None

    def update_devices(self) -> None:
        raw_devices    = adb_utils.list_devices()
        parsed_devices = [self.parse_adb_line(line) for line in raw_devices]
        self.__devices = [self.get_device_from_dict(d) for d in parsed_devices]

        log.info("Devices updated: found %d device(s)", len(self.__devices))
        for device in self.__devices:
            log.debug("Device added: %s", device)

    @staticmethod
    def parse_adb_line(line: str) -> dict[str: str]:
        items = [item.split(":") for item in line.split()]
        items[0].insert(0, "serial")
        items[1].insert(0, "status")

        features = {item[0]: item[1] for item in items}

        log.debug("Parsed line: %s", line.strip())
        log.debug("Got features: %s", features)

        return features

    @staticmethod
    def get_device_from_dict(features: dict) -> Device:
        return Device(
            serial      =features.get("serial"),
            model       =features.get("model"),
            device      =features.get("device"),
            status      =features.get("status"),
            usb         =features.get("usb"),
            product     =features.get("product"),
            transport_id=features.get("transport_id"),
        )
