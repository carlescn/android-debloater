import logging

from src import adb_utils
from src import event_handler
from src.device import Device
from src.event import Event

log = logging.getLogger(__name__)


class DeviceManager:
    def __init__(self) -> None:
        self.__register_events()

        self.__devices: list[Device] = []
        self.__active_device: Device | None = None

    def __register_events(self):
        event_handler.register(Event.ACTIVE_DEVICE_UPDATE_REQUESTED, self.set_active_device)
        event_handler.register(Event.DEVICE_LIST_UPDATE_REQUESTED, self.update_devices)

    def get_devices_serials(self) -> list[str]:
        return [d.serial for d in self.__devices]

    def get_active_device(self) -> Device | None:
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
            event_handler.fire(Event.ACTIVE_DEVICE_UPDATED, self.__active_device)
        except ValueError:
            self.__active_device = None

    def update_devices(self) -> None:
        raw_devices = adb_utils.list_devices()
        self.__devices = [self.get_device_from_adb_line(line) for line in raw_devices]

        log.info("Devices updated: found %d device(s)", len(self.__devices))
        for device in self.__devices:  # type: ignore
            log.debug("Device added: %s", device)

        if len(self.__devices) > 0:
            event_handler.fire(Event.DEVICE_LIST_UPDATED, devices=self.__devices)

    def get_device_from_adb_line(self, line: str) -> Device:
        device = self.parse_adb_line(line)

        properties = {
            "release": adb_utils.get_device_release(device["serial"]),
            "name": adb_utils.get_device_name(device["serial"])
        }
        filtered_properties = {k: v for k, v in properties.items() if v is not None}
        device.update(filtered_properties)

        return self.get_device_from_dict(device)

    @staticmethod
    def parse_adb_line(line: str) -> dict[str, str]:
        items = [item.split(":") for item in line.split()]
        items[0].insert(0, "serial")
        items[1].insert(0, "status")

        features = {item[0]: item[1] for item in items}

        log.debug("Parsed line: %s", line.strip())
        log.debug("Got features: %s", features)

        return features

    @staticmethod
    def get_device_from_dict(features: dict) -> Device:
        default_value = "UNKNOWN"
        return Device(
            serial      =features.get("serial", default_value),
            model       =features.get("model", default_value),
            device      =features.get("device", default_value),
            status      =features.get("status", default_value),
            usb         =features.get("usb", default_value),
            product     =features.get("product", default_value),
            transport_id=features.get("transport_id", default_value),
            release     =features.get("release", default_value),
            name        =features.get("name", default_value),
        )
