import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedTk

from src.gui.tkinter.devices_frame import DevicesFrame
from src.gui.tkinter.packages_frame import PackagesFrame


class MainWindow:
    def __init__(self, main_app):
        # Main window
        self.root = ThemedTk(theme="scidgrey")
        self.root.title("Android Debloater")

        # Top bar
        self.frm_top_bar = ttk.Frame(self.root)
        self.frm_top_bar.pack(anchor="nw", side=tk.TOP)

        # Device selector
        self.frm_devices = DevicesFrame(master=self.frm_top_bar,
                                        cmb_command=main_app.update_active_device)
        self.frm_devices.pack(side=tk.LEFT)

        # Update packages button
        self.btn_update_packages = ttk.Button(master=self.frm_top_bar,
                                              text="Read packages",
                                              command=main_app.update_packages_list)
        self.btn_update_packages.pack(side=tk.RIGHT)

        # Packages list
        self.frm_packages = PackagesFrame(self.root)
        self.frm_packages.pack()

    def update_devices_list(self, serials: list[str]) -> None:
        self.frm_devices.set_values(serials)

    def get_active_device(self) -> str:
        return self.frm_devices.get_active()

    def update_packages_list(self, rows) -> None:
        self.clear_packages_list()
        self.frm_packages.add_rows(rows)

    def clear_packages_list(self) -> None:
        self.frm_packages.clear()

    def mainloop(self) -> None:
        self.root.mainloop()
