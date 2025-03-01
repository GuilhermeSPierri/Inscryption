import tkinter as tk
from abc import ABC, abstractmethod
from fonts.font import *
from widgets.button import Button
#from PIL import Image, ImageTk

class Page(tk.Frame, ABC):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.custom_font_buttons = font.Font(family="The Macabre", size=14)
        self.create_widgets()
        self.buttons = []
        self.labels = []

    @abstractmethod
    def create_widgets(self):
        pass
    