import tkinter as tk
from fonts.font import *

class DeckPage(tk.Frame):

    def __init__(self, parent, controller, show_startPage):
        super().__init__(parent)
        label = tk.Label(self, text="Criador de Deck", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        cardName = tk.StringVar()

        entry = tk.Entry(master = self, textvariable=cardName)
        entry.pack()

        searchCardButton = tk.Button(
            self,
            text="Procurar carta", 
            command = lambda: print(entry.get())
            )
        
        searchCardButton.pack()

        addCardButton = tk.Button(
            self,
            text="Adicionar carta ao Deck", 
            )
        
        addCardButton.pack()

        startPageButton = tk.Button(
            self,
            text="Voltar ao Menu", 
            command=show_startPage)
        
        startPageButton.pack()

        namesOfCards = ['card1', 'card2', 'card3', 'card4', 'card5']

        for card in namesOfCards:
            checkVar = tk.IntVar()
            check = tk.Checkbutton(
                self, 
                text=card, 
                variable=checkVar, 
                command=lambda card=card, var=checkVar: self.on_check(var, card) # card = card and var = checkVar freezes the variable with the value of each iteration, without this on_check function would use only the value of the last iteration(card5) to test
            )
            check.pack()

    def buttonSearch(self, entry):
        print(entry.get())

    def on_check(self, var, card):
        state = var.get()
        print(f"{card} is {'selected' if state else 'deselected'}")