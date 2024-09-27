import tkinter as tk
from fonts.font import *

class StartPage(tk.Frame):

    def __init__(self, parent, controller, show_gamePage, show_deckPage):
        super().__init__(parent)
        label = tk.Label(self, text="Inscryption", font=LARGE_FONT)
        label.pack(pady=10, padx=10) #possivel substituir por grid

        gameButton = tk.Button(
            self,
            text="Jogar",
            command= show_gamePage
        )

        gameButton.pack()

        deckButton = tk.Button(
            self,
            text="Criar Deck",
            command= show_deckPage
        )

        deckButton.pack()
