import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedTk

from src import event_handler
from src.event import Event
from src.gui.tkinter.devices_frame import DevicesFrame
from src.gui.tkinter.packages_frame import PackagesFrame


class MainWindow:
    def __init__(self):
        # Main window
        self.root = ThemedTk(theme="scidgrey")
        self.root.title("Android Debloater")

        # Top bar
        self.frm_top_bar = ttk.Frame(self.root)
        self.frm_top_bar.pack(anchor="nw", side=tk.TOP)

        # Device selector
        self.frm_devices = DevicesFrame(master=self.frm_top_bar)
        self.frm_devices.pack(side=tk.LEFT)

        # Update packages button
        self.btn_update_packages = ttk.Button(master=self.frm_top_bar,
                                              text="Read packages",
                                              command=self.__btn_update_packages_action)
        self.btn_update_packages.pack(side=tk.RIGHT)

        # Packages list
        self.frm_packages = PackagesFrame(self.root)
        self.frm_packages.pack()

    @staticmethod
    def __btn_update_packages_action(*args, **kwargs):
        event_handler.fire(Event.PACKAGE_LIST_UPDATE_REQUESTED)

    def mainloop(self) -> None:
        self.root.mainloop()
