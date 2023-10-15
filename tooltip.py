import tkinter as tk
from tkinter import Toplevel

class ToolTip:
    """
    ToolTip class to create and manage hover tooltips for tkinter widgets.
    """

    def __init__(self, widget, text):
        """
        Initialize a new tooltip.
        :param widget: The tkinter widget to which the tooltip will be attached.
        :param text: The text to display in the tooltip.
        """
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        """
        Display the tooltip.
        """
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        self.tooltip = Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        """
        Hide the tooltip.
        """
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


