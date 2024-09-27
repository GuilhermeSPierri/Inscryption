import tkinter as tk
from fonts.font import *
from button import Button

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Inscryption", font=LARGE_FONT)
        label.pack(pady=10, padx=10) #possivel substituir por grid

        gameButton = Button(self, "Jogar", "show_frame", controller, ("GamePage", ))

        gameButton.pack()

        deckButton = Button(self, "Criar Deck", "show_frame", controller, ("DeckPage", ))

        deckButton.pack()
