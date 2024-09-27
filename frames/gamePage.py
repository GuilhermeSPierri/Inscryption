import tkinter as tk
from fonts.font import *
from button import Button

class GamePage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Game Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        startPageButton = Button(self, "Voltar ao Menu", "show_frame", controller, ("StartPage", ))
        
        startPageButton.pack()
