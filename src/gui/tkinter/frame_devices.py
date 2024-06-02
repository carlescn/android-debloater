import tkinter as tk
from tkinter import ttk

from src import event_handler
from src.event import Event
from src.gui.tkinter.constants import PADDING_INNER
from src.device import Device


class FrameDevices(ttk.LabelFrame):
    def __init__(self, master: ttk.Frame, padding: int = 0):
        super().__init__(master=master, padding=padding, text="Devices")
        self.__register_events()

        # Label
        ttk.Label(self, text="Active device:").pack(side=tk.LEFT, padx=(0, PADDING_INNER))

        # Devices list
        self.cmb_devices = ttk.Combobox(self)
        self.cmb_devices.pack(side=tk.LEFT, padx=PADDING_INNER)
        self.cmb_devices.bind('<<ComboboxSelected>>', self.__cmb_devices_selected_action)

        # Update button
        self.btn_clear = ttk.Button(master=self, padding=PADDING_INNER, text="Update list",
                                    command=self.__btn_update_action)
        self.btn_clear.pack(side=tk.RIGHT, padx=(PADDING_INNER, 0))

        # Device info
        self.var_device_info = tk.StringVar()
        ttk.Label(self, textvariable=self.var_device_info).pack(side=tk.LEFT, padx=PADDING_INNER)
        self.reset_active_device_info()

    def __register_events(self):
        event_handler.register(Event.DEVICE_LIST_UPDATED, self.reset_device_list)
        event_handler.register(Event.ACTIVE_DEVICE_UPDATED, self.update_active_device_info)

    def __cmb_devices_selected_action(self, *args, **kwargs):
        event_handler.fire(Event.ACTIVE_DEVICE_UPDATE_REQUESTED, serial=self.get_active_device())

    @staticmethod
    def __btn_update_action(*args, **kwargs) -> None:
        event_handler.fire(Event.DEVICE_LIST_UPDATE_REQUESTED)

    def reset_device_list(self, devices: list[Device]) -> None:
        self.reset_active_device_info()

        self.cmb_devices["values"] = [d.serial for d in devices]
        self.cmb_devices.current(0)
        self.__cmb_devices_selected_action()

    def reset_active_device_info(self) -> None:
        self.var_device_info.set("No active device has been set")

    def update_active_device_info(self, device: Device) -> None:
        self.var_device_info.set(f"Name: {device.name} | Release: {device.release}")

    def get_active_device(self) -> str:
        return self.cmb_devices.get()
