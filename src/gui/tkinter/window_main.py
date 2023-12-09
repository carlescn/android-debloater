import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedTk

from src import event_handler
from src.event import Event
from src.gui.tkinter.constants import PADDING_OUTER
from src.gui.tkinter.frame_devices import FrameDevices
from src.gui.tkinter.frame_packages import FramePackages


class WindowMain:
    def __init__(self):
        # Main window
        self.window = ThemedTk(theme="scidgrey")
        self.window.title("Android Debloater")

        frm_main = ttk.Frame(master=self.window, padding=PADDING_OUTER)
        frm_main.pack()

        # Device selector
        frm_devices = FrameDevices(master=frm_main, padding=PADDING_OUTER)
        frm_devices.pack(anchor="nw", fill=tk.X, pady=(0, PADDING_OUTER))

        # Packages list
        frm_packages = FramePackages(master=frm_main, padding=PADDING_OUTER)
        frm_packages.pack()

        event_handler.fire(Event.DEVICE_LIST_UPDATE_REQUESTED)

    def mainloop(self) -> None:
        self.window.mainloop()
