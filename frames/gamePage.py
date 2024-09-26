import tkinter as tk
from fonts.font import *

class GamePage(tk.Frame):

    def __init__(self, parent, controller, show_startPage):
        super().__init__(parent)
        label = tk.Label(self, text="Game Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        startPageButton = tk.Button(
            self,
            text="Voltar ao Menu", 
            command=show_startPage)
        
        startPageButton.pack()
