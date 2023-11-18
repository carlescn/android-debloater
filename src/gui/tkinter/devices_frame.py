import tkinter as tk
from tkinter import ttk


class DevicesFrame(ttk.Frame):
    def __init__(self,
                 master: ttk.Frame,
                 cmb_command):
        super().__init__(master)

        ttk.Label(self, text="Active device:").pack(side=tk.LEFT)

        self.cmb_devices = ttk.Combobox(self)
        self.cmb_devices.pack(side=tk.LEFT)
        self.cmb_devices.bind('<<ComboboxSelected>>', cmb_command)

    def set_values(self, serials: list[str]) -> None:
        self.cmb_devices["values"] = serials
        self.cmb_devices.current(0)

    def get_active(self) -> str:
        return self.cmb_devices.get()
