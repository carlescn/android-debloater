import logging

from src.adb_utils import AdbUtils
from src.device import Device


class DeviceManager:
    def __init__(self):
        self.__log = logging.getLogger(__name__)
        self.__adb = AdbUtils()

        self.__devices: list[Device] = []
        self.__active_device: Device = None

    def get_devices_serials(self) -> list[str]:
        return [d.serial for d in self.__devices]

    def get_active_device(self) -> Device:
        return self.__active_device

    def get_device_from_serial(self, serial: str) -> Device:
        device = [d for d in self.__devices if d.serial == serial]

        if len(device) == 0:
            self.__log.exception("Did not find any device with serial '%s'", serial)
            raise IndexError
        if len(device) > 1:
            self.__log.exception("Found more than one device with serial '%s'", serial)
            raise IndexError

        return device[0]

    def set_active_device(self, serial: str) -> None:
        try:
            self.__active_device = self.get_device_from_serial(serial)
            self.__log.info("Active device is set to '%s'", serial)
        except IndexError:
            self.__active_device = None

    def update_devices(self) -> None:
        raw_devices = self.__adb.list_devices()
        devices = [self.parse_adb_line(line) for line in raw_devices]
        self.__devices = [self.get_device_from_dict(d) for d in devices]

        self.__log.info("Devices updated: found %d device(s)", len(self.__devices))
        for device in self.__devices:
            self.__log.debug("Device added: %s", device)

    def parse_adb_line(self, line: str) -> dict[str: str]:
        values = line.split()
        value_pairs = [value.split(":") for value in values[2:]]

        properties = {key: value for key, value in value_pairs}
        properties["serial"] = values[0]
        properties["status"] = values[1]

        self.__log.debug("Parsed line: %s", line.strip())
        self.__log.debug("Got properties: %s", properties)

        return properties

    @staticmethod
    def get_device_from_dict(properties: dict) -> Device:
        return Device(
            serial       = properties.get("serial"),
            model        = properties.get("model"),
            device       = properties.get("device"),
            status       = properties.get("status"),
            usb          = properties.get("usb"),
            product      = properties.get("product"),
            transport_id = properties.get("transport_id"),
        )
