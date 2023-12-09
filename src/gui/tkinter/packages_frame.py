from tkinter import ttk

from src import event_handler
from src.event import Event
from src.gui.tkinter.scrollable import Scrollable
from src.package import Package


class PackagesFrame(ttk.Frame):
    def __init__(self, master: ttk.Frame):
        super().__init__(master)
        self.__register_events()

        self.rows = []
        self.columns = [
            {"name": "Short name", "index": 0, "width": 200},
            {"name": "Long name",  "index": 1, "width": 500},
            {"name": "Status",     "index": 2, "width": 100},
        ]

        # Header
        self.header = ttk.Frame(master)
        self.header.pack(anchor="nw")
        for col in self.columns:
            name = col.get("name")
            i = col.get("index")
            ttk.Label(self.header, text=name).grid(row=0, column=i)

        # Body
        self.body = ttk.Frame(master)
        self.body.pack(anchor="nw")
        self.scrollable = Scrollable(self.body)

        # Footer
        # self.footer = ttk.Frame(master)
        # self.footer.pack(anchor="nw")

        self.update()

    def __register_events(self):
        event_handler.register(Event.ACTIVE_DEVICE_UPDATED, self.clear_package_list)
        event_handler.register(Event.PACKAGE_LIST_UPDATED, self.update_package_list)

    def update(self):
        for col in self.columns:
            width = col.get("width")
            i = col.get("index")
            self.header.columnconfigure(index=i, minsize=width, weight=0)
            self.scrollable.columnconfigure(index=i, minsize=width, weight=0)
        self.scrollable.update()

    def clear_package_list(self, *args, **kwargs) -> None:
        for row in self.rows:
            for label in row:
                label.destroy()

        self.rows = []
        self.update()

    def update_package_list(self, packages: list[Package]) -> None:
        self.clear_package_list()

        packages_info = [(p.short_name, p.full_name, p.installed) for p in packages]
        packages_info.sort(key=lambda x: x[1])
        for i, labels in enumerate(packages_info):
            row = []
            for j, label in enumerate(labels):
                cell = ttk.Label(self.scrollable, text=label)
                cell.grid(row=i, column=j)
                row.append(cell)
            self.rows.append(row)

        self.update()
