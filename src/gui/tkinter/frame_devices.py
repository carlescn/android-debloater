import tkinter as tk
from tkinter import ttk

from src import event_handler
from src.event import Event
from src.gui.tkinter.constants import PADDING_INNER
from src.device import Device
from src.protocols import DeviceManager


class FrameDevices(ttk.LabelFrame):
    def __init__(self, device_manager: DeviceManager, master: ttk.Frame, padding: int = 0):
        super().__init__(master=master, padding=padding, text="Devices")
        self.__register_events()

        self.__device_manager = device_manager

        # Label
        ttk.Label(self, text="Active device:").pack(side=tk.LEFT, padx=(0, PADDING_INNER))

        # Devices list
        self.cmb_devices = ttk.Combobox(self)
        self.cmb_devices.pack(side=tk.LEFT, padx=PADDING_INNER)
        self.cmb_devices.bind('<<ComboboxSelected>>', self.__cmb_devices_selected_action)

        # Update button
        self.btn_clear = ttk.Button(master=self, padding=PADDING_INNER, text="Update list",
                                    command=self.__device_manager.update_devices)
        self.btn_clear.pack(side=tk.RIGHT, padx=(PADDING_INNER, 0))

        # Device displayed info
        self.displayed_info = tk.StringVar()
        ttk.Label(self, textvariable=self.displayed_info).pack(side=tk.LEFT, padx=PADDING_INNER)
        self.reset_displayed_info()

    def __register_events(self):
        event_handler.register(Event.DEVICE_LIST_UPDATED, self.reset_device_list)

    def __cmb_devices_selected_action(self, *args, **kwargs):
        serial = self.get_selected_device()
        self.__device_manager.set_active_device(serial)
        self.update_displayed_info()

    def reset_device_list(self, devices: list[Device]) -> None:
        self.reset_displayed_info()

        self.cmb_devices["values"] = [d.serial for d in devices]
        self.cmb_devices.current(0)
        self.__cmb_devices_selected_action()

    def reset_displayed_info(self) -> None:
        self.displayed_info.set("No active device has been set")

    def update_displayed_info(self) -> None:
        device = self.__device_manager.get_active_device()
        if device is None:
            self.reset_displayed_info()
            return
        self.displayed_info.set(f"Name: {device.name} | Release: {device.release}")

    def get_selected_device(self) -> str:
        return self.cmb_devices.get()
