import tkinter as tk

class CustomButton(tk.Canvas):
    """
    CustomButton class to provide enhanced visual buttons in tkinter.
    """

    def __init__(self, master, **kwargs):
        """
        Initialize a new custom button.
        Accepts all regular tkinter.Canvas parameters, and additional parameters for customization.
        """
        width = kwargs.pop('width', 100)
        height = kwargs.pop('height', 40)
        self.bg_color = kwargs.pop('bg_color', '#ffffff')
        self.hover_color = kwargs.pop('hover_color', '#f0f0f0')
        self.fg_color = kwargs.pop('fg_color', '#000000')
        self.text = kwargs.pop('text', '')
        self.font = kwargs.pop('font', ('Arial', 10))
        self.command = kwargs.pop('command', None)
        super().__init__(master, width=width, height=height, bg=self.bg_color, **kwargs)

        # Create button text in the center of the canvas
        self.create_text(self.width // 2, self.height // 2, text=self.text, fill=self.fg_color, font=self.font)

        # Bind mouse events for hover and click effects
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def on_hover(self, event):
        """
        Change button background on mouse hover.
        """
        self.config(bg=BUTTON_HOVER_COLOR)

    def on_leave(self, event):
        """
        Reset button background when mouse leaves.
        """
        self.config(bg=self.bg_color)

    def on_press(self, event):
        """
        Placeholder for future enhancements during button press.
        """
        pass

    def on_release(self, event):
        """
        Execute the assigned command (if any) and reset button hover color on mouse release.
        """
        self.config(bg=self.hover_color)
        if self.command:
            self.command()
