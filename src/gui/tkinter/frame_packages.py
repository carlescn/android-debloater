import tkinter as tk
from tkinter import ttk

from src import event_handler
from src.event import Event
from src.gui.tkinter.constants import PADDING_INNER, PADDING_OUTER
from src.package import Package


class FramePackages(ttk.LabelFrame):
    COLUMNS = [
        {"id": "package",        "text": "package",        "width": 400, "anchor": "w"},
        {"id": "short_name",     "text": "name",           "width": 200, "anchor": "w"},
        {"id": "installed",      "text": "installed",      "width": 100, "anchor": "center"},
        {"id": "disabled",       "text": "disabled",       "width": 100, "anchor": "center"},
        {"id": "system",         "text": "system",         "width": 100, "anchor": "center"},
        {"id": "safe_to_remove", "text": "safe_to_remove", "width": 100, "anchor": "center"},
    ]

    def __init__(self, master: ttk.Frame, padding: int = 0):
        super().__init__(master=master, padding=padding, text="Packages")
        self.__register_events()

        # Tree view
        self.tree = ttk.Treeview(self, show=["headings"])
        self.tree.pack(pady=(0, PADDING_OUTER))
        self.__setup_treeview()

        # Update button
        self.btn_update = ttk.Button(master=self, padding=PADDING_INNER, state=tk.DISABLED,
                                     text="Update",
                                     command=self.__btn_update_action)
        self.btn_update.pack(side=tk.RIGHT, padx=(PADDING_INNER, 0))

        # Clear button
        self.btn_clear = ttk.Button(master=self, padding=PADDING_INNER, state=tk.DISABLED,
                                    text="Clear",
                                    command=self.clear_package_list)
        self.btn_clear.pack(side=tk.RIGHT, padx=PADDING_INNER)

    def __register_events(self) -> None:
        event_handler.register(Event.ACTIVE_DEVICE_UPDATED, self.clear_package_list)
        event_handler.register(Event.ACTIVE_DEVICE_UPDATED, self.enable_btn_update)
        event_handler.register(Event.PACKAGE_LIST_UPDATED, self.update_package_list)

    def __setup_treeview(self):
        # Columns and headers
        self.tree["columns"] = [c.get("id") for c in self.COLUMNS]
        for col in self.COLUMNS:
            self.tree.heading(col.get("id"), text=col.get("text"))
            self.tree.column(col.get("id"), width=col.get("width"), anchor=col.get("anchor"))

    @staticmethod
    def __btn_update_action(*args, **kwargs) -> None:
        event_handler.fire(Event.PACKAGE_LIST_UPDATE_REQUESTED)

    def enable_btn_update(self, *args, **kwargs) -> None:
        self.btn_update.state(["!" + tk.DISABLED])

    def disable_btn_update(self, *args, **kwargs) -> None:
        self.btn_update.state([tk.DISABLED])

    def enable_btn_clear(self, *args, **kwargs) -> None:
        self.btn_clear.state(["!" + tk.DISABLED])

    def disable_btn_clear(self, *args, **kwargs) -> None:
        self.btn_clear.state([tk.DISABLED])

    def clear_package_list(self, *args, **kwargs) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.disable_btn_clear()

    def update_package_list(self, packages: list[Package]) -> None:
        self.clear_package_list()

        packages.sort()
        for p in packages:
            installed = "Installed" if p.installed else "Uninstalled"
            disabled = "Disabled" if p.disabled else "Enabled"
            system = "System" if p.system else "User"
            safe_to_remove = "Yes" if p.safe_to_remove else "NO!"

            values = (p.full_name, p.short_name, installed, disabled, system, safe_to_remove)
            self.tree.insert(parent="", index="end", iid=p.full_name, values=values)

        self.enable_btn_clear()
