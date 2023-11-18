import tkinter as tk
from tkinter import ttk


class Scrollable(ttk.Frame):
    """
    Make a frame scrollable with scrollbar on the right.
    After adding or removing widgets to the scrollable frame,
    call the update() method to refresh the scrollable area.
    @credit: https://stackoverflow.com/a/47985165
    """

    def __init__(self, master: tk.Frame):
        scrollbar = ttk.Scrollbar(master)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(master, yscrollcommand=scrollbar.set, width=800, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        super().__init__(master)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0, 0, window=self, anchor="nw")

    def __fill_canvas(self, event):
        """Enlarge the windows item to the canvas width"""
        self.canvas.itemconfig(self.windows_item, width=event.width)

    def update(self):
        """Update the canvas and the scroll region"""

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))
