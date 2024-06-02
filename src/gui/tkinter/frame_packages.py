import tkinter as tk
from collections.abc import Iterable
from dataclasses import dataclass, field
from tkinter import ttk

from src import event_handler
from src.event import Event
from src.gui.tkinter.constants import PADDING_INNER, PADDING_OUTER
from src.package import Package
from src.protocols import PackageManager


@dataclass
class Column:
    id     : str = field()
    text   : str = field()
    width  : int = field()
    anchor : str = field()


COLUMNS: list[Column] = [
    Column(id="package",        text="package",        width=400, anchor="w"),
    Column(id="short_name",     text="name",           width=200, anchor="w"),
    Column(id="installed",      text="installed",      width=100, anchor="center"),
    Column(id="disabled",       text="disabled",       width=100, anchor="center"),
    Column(id="system",         text="system",         width=100, anchor="center"),
    Column(id="safe_to_remove", text="safe to remove", width=100, anchor="center"),
]

SYMBOL_SORTED_DESC = " \u25BE"  # utf-8 hex for triangle pointing down
SYMBOL_SORTED_ASC  = " \u25B4"  # utf-8 hex for triangle pointing up


class FramePackages(ttk.LabelFrame):
    def __init__(self, package_manager: PackageManager, master: ttk.Frame, padding: int = 0):
        super().__init__(master=master, padding=padding, text="Packages")
        self.__register_events()

        self.__package_manager = package_manager

        self.__make_treeview()
        self.__make_buttons()
        self.__pack()

    def __register_events(self) -> None:
        event_handler.register(Event.ACTIVE_DEVICE_UPDATED, self.clear_package_list)
        event_handler.register(Event.ACTIVE_DEVICE_UPDATED, self.btn_update_enable)
        event_handler.register(Event.PACKAGE_LIST_UPDATED, self.update_package_list)

    def __make_treeview(self) -> None:
        self.tree = ttk.Treeview(self, show=["headings"], selectmode="none", height=20)
        # Columns and headers
        self.tree["columns"] = [c.id for c in COLUMNS]
        for col in COLUMNS:
            self.tree.heading(column=col.id,
                              text=col.text,
                              command=lambda c=col.id: self.sort_by_column(c))  # type: ignore
            self.tree.column(column=col.id,  # type: ignore
                             width=col.width,
                             anchor=col.anchor)
        # Actions
        self.tree.bind("<Button-1>", self.update_selection)

    def __make_buttons(self) -> None:
        # List actions
        self.btn_update = ttk.Button(master=self, padding=PADDING_INNER, state=tk.DISABLED,
                                     text="Update list",
                                     command=self.__package_manager.update_packages)
        self.btn_clear = ttk.Button(master=self, padding=PADDING_INNER, state=tk.DISABLED,
                                    text="Clear selection",
                                    command=self.clear_selection)
        # Package actions
        self.btn_uninstall = ttk.Button(master=self, padding=PADDING_INNER, state=tk.DISABLED,
                                        text="Uninstall selected",
                                        command=self.__btn_uninstall_action)
        self.btn_reinstall = ttk.Button(master=self, padding=PADDING_INNER, state=tk.DISABLED,
                                        text="Reinstall selected",
                                        command=self.__btn_reinstall_action)
        self.btn_enable = ttk.Button(master=self, padding=PADDING_INNER, state=tk.DISABLED,
                                     text="Enable selected",
                                     command=self.__btn_enable_action)
        self.btn_disable = ttk.Button(master=self, padding=PADDING_INNER, state=tk.DISABLED,
                                      text="Disable selected",
                                      command=self.__btn_disable_action)

    def __pack(self) -> None:
        self.tree.pack(pady=(0, PADDING_OUTER))
        self.btn_uninstall.pack(side=tk.LEFT, padx=(0, PADDING_INNER))
        self.btn_reinstall.pack(side=tk.LEFT, padx=PADDING_INNER)
        self.btn_enable.pack(side=tk.LEFT, padx=PADDING_INNER)
        self.btn_disable.pack(side=tk.LEFT, padx=PADDING_INNER)
        self.btn_update.pack(side=tk.RIGHT, padx=(PADDING_INNER, 0))
        self.btn_clear.pack(side=tk.RIGHT, padx=PADDING_INNER)

    # List methods

    def clear_package_list(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.btns_disable_on_clear_list()

    def update_package_list(self, packages: Iterable[Package]) -> None:
        self.clear_package_list()

        for p in packages:
            values = (
                p.full_name,
                p.short_name,
                "Installed" if p.installed else "Uninstalled",
                "Disabled" if p.disabled else "Enabled",
                "System" if p.system else "User",
                "Yes" if p.safe_to_remove else "NO!!!",
            )
            self.tree.insert(parent="", index="end", iid=p.full_name, values=values)

        self.sort_by_column(COLUMNS[0].id, False)

        self.btns_enable_on_fill_list()

    def get_selection(self) -> tuple[str, ...]:
        return self.tree.selection()

    def clear_selection(self, *args, **kwargs) -> None:
        self.tree.selection_set()

    def update_selection(self, event, *args, **kwargs) -> None:
        if self.tree.identify_region(event.x, event.y) != "cell":
            return
        item = self.tree.identify_row(event.y)
        self.tree.selection_toggle(item)
        self.tree.focus(item)

    def sort_by_column(self, column: str, reverse: bool | None = None) -> None:
        if reverse is None:
            reverse = self.tree.heading(column, "text").endswith(SYMBOL_SORTED_DESC)

        items = list(self.tree.get_children(""))
        items.sort(key=lambda i: self.tree.set(i, column).lower(), reverse=reverse)

        for index, item in enumerate(items):
            self.tree.move(item, "", index)

        # Update headers
        suffix = SYMBOL_SORTED_ASC if reverse else SYMBOL_SORTED_DESC
        for col in COLUMNS:
            text = col.text + (suffix if col.id == column else "")
            self.tree.heading(col.id, text=text)

    # Button methods

    def btn_update_enable(self) -> None:
        self.btn_update.state(["!" + tk.DISABLED])

    def btn_update_disable(self) -> None:
        self.btn_update.state([tk.DISABLED])

    def btns_enable_on_fill_list(self) -> None:
        self.btn_clear.state(["!" + tk.DISABLED])
        self.btn_uninstall.state(["!" + tk.DISABLED])
        self.btn_reinstall.state(["!" + tk.DISABLED])
        self.btn_enable.state(["!" + tk.DISABLED])
        self.btn_disable.state(["!" + tk.DISABLED])

    def btns_disable_on_clear_list(self) -> None:
        self.btn_clear.state([tk.DISABLED])
        self.btn_uninstall.state([tk.DISABLED])
        self.btn_reinstall.state([tk.DISABLED])
        self.btn_enable.state([tk.DISABLED])
        self.btn_disable.state([tk.DISABLED])

    def __btn_uninstall_action(self) -> None:
        self.__package_manager.uninstall_packages(self.get_selection())

    def __btn_reinstall_action(self) -> None:
        self.__package_manager.reinstall_packages(self.get_selection())

    def __btn_enable_action(self) -> None:
        self.__package_manager.enable_packages(self.get_selection())

    def __btn_disable_action(self) -> None:
        self.__package_manager.disable_packages(self.get_selection())
