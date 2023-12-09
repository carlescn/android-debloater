import tkinter as tk
from tkinter import ttk

from src import event_handler
from src.event import Event
from src.gui.tkinter.constants import PADDING_INNER


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
        self.btn_clear.pack(side=tk.LEFT, padx=PADDING_INNER)

    def __register_events(self):
        event_handler.register(Event.DEVICE_LIST_UPDATED, self.set_values)

    def __cmb_devices_selected_action(self, *args, **kwargs):
        event_handler.fire(Event.ACTIVE_DEVICE_UPDATED, serial=self.get_active())

    @staticmethod
    def __btn_update_action(*args, **kwargs) -> None:
        event_handler.fire(Event.DEVICE_LIST_UPDATE_REQUESTED)

    def set_values(self, serials: list[str]) -> None:
        self.cmb_devices["values"] = serials
        self.cmb_devices.current(0)
        self.__cmb_devices_selected_action()

    def get_active(self) -> str:
        return self.cmb_devices.get()
