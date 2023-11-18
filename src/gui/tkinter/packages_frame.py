from tkinter import ttk

from src.gui.tkinter.scrollable import Scrollable


class PackagesFrame(ttk.Frame):
    def __init__(self, master: ttk.Frame):
        super().__init__(master)

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

    def __add_single_row(self, labels) -> None:
        n = len(self.rows)

        row = [ttk.Label(self.scrollable, text=label) for label in labels]
        for j, cell in enumerate(row):
            cell.grid(row=n, column=j)

        self.rows.append(row)

    def add_rows(self, rows: tuple | list) -> None:
        for row in rows:
            self.__add_single_row(row)
        self.update()

    def update(self):
        for col in self.columns:
            width = col.get("width")
            i = col.get("index")
            self.header.columnconfigure(index=i, minsize=width, weight=0)
            self.scrollable.columnconfigure(index=i, minsize=width, weight=0)
        self.scrollable.update()

    def clear(self):
        for row in self.rows:
            for label in row:
                label.destroy()

        self.rows = []
        self.update()
