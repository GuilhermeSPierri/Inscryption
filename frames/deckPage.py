import tkinter as tk
from fonts.font import *
from button import Button

class DeckPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Criador de Deck", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        cardName = tk.StringVar()

        entry = tk.Entry(master = self, textvariable=cardName)
        entry.pack()

        searchCardButton = Button(self, "Procurar carta", "search_card", controller, (entry, ))
        
        searchCardButton.pack()

        addCardButton = Button(self, "Adicionar carta ao Deck", "add_card_to_deck", controller)
        
        addCardButton.pack()

        startPageButton = Button(self, "Voltar ao Menu", "show_frame", controller, ("StartPage", ))
        
        startPageButton.pack()

        namesOfCards = ['card1', 'card2', 'card3', 'card4', 'card5']

        for card in namesOfCards:
            checkVar = tk.IntVar()
            check = tk.Checkbutton(
                self, 
                text=card, 
                variable=checkVar, 
                command=lambda card=card, var=checkVar: controller.on_check(var, card) # card = card and var = checkVar freezes the variable with the value of each iteration, without this on_check function would use only the value of the last iteration(card5) to test
            )
            check.pack()

    