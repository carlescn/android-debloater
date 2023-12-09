import tkinter as tk
from tkinter import ttk

from src import event_handler
from src.event import Event


class DevicesFrame(ttk.Frame):
    def __init__(self, master: ttk.Frame):
        super().__init__(master)
        self.__register_events()

        ttk.Label(self, text="Active device:").pack(side=tk.LEFT)

        self.cmb_devices = ttk.Combobox(self)
        self.cmb_devices.pack(side=tk.LEFT)
        self.cmb_devices.bind('<<ComboboxSelected>>', self.__cmb_devices_selected_action)

        event_handler.fire(Event.DEVICE_LIST_UPDATE_REQUESTED)

    def __register_events(self):
        event_handler.register(Event.DEVICE_LIST_UPDATED, self.set_values)

    def __cmb_devices_selected_action(self, *args, **kwargs):
        event_handler.fire(Event.ACTIVE_DEVICE_UPDATED, serial=self.get_active())

    def set_values(self, serials: list[str]) -> None:
        self.cmb_devices["values"] = serials
        self.cmb_devices.current(0)
        self.__cmb_devices_selected_action()

    def get_active(self) -> str:
        return self.cmb_devices.get()
