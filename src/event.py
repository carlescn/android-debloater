from enum import Enum, auto


class Event(Enum):
    ACTIVE_DEVICE_UPDATED = auto()
    DEVICE_LIST_UPDATED = auto()
    PACKAGE_LIST_UPDATED = auto()
