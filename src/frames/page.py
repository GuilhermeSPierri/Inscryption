import tkinter as tk
from abc import ABC, abstractmethod
from fonts.font import *
from widgets.button import Button
#from PIL import Image, ImageTk

class Page(tk.Frame, ABC):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.buttons = []
        self.labels = []

    @abstractmethod
    def create_widgets(self):
        pass

    #def set_background(self, image_path):
     #   image = Image.open(image_path)
      #  image = image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.LANCZOS)
       # self.background_image = ImageTk.PhotoImage(image)