import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedTk

from src.gui.tkinter.constants import PADDING_OUTER
from src.gui.tkinter.frame_devices import FrameDevices
from src.gui.tkinter.frame_packages import FramePackages
from src.protocols import DeviceManager


class WindowMain:
    def __init__(self, device_manager: DeviceManager):
        # Main window
        self.window = ThemedTk(theme="scidgrey")
        self.window.title("Android Debloater")

        frm_main = ttk.Frame(master=self.window, padding=PADDING_OUTER)
        frm_main.pack()

        # Device selector
        frm_devices = FrameDevices(device_manager=device_manager, master=frm_main, padding=PADDING_OUTER)
        frm_devices.pack(anchor="nw", fill=tk.X, pady=(0, PADDING_OUTER))

        # Packages list
        frm_packages = FramePackages(master=frm_main, padding=PADDING_OUTER)
        frm_packages.pack()

        # Run on startup
        device_manager.update_devices()

    def mainloop(self) -> None:
        self.window.mainloop()
