import tkinter as tk
from fonts.font import *
from widgets.button import Button
from frames.page import Page

class DeckPage(Page):

    def create_widgets(self):
        label = tk.Label(self, text="Criador de Deck", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        card_name = tk.StringVar()
        entry = tk.Entry(master=self, textvariable=card_name)
        entry.pack()

        search_card_button = Button(self, "Procurar carta", "search_card", self.controller, (entry,))
        search_card_button.pack()

        add_card_button = Button(self, "Adicionar carta ao Deck", "add_card_to_deck", self.controller)
        add_card_button.pack()

        start_page_button = Button(self, "Voltar ao Menu", "show_frame", self.controller, ("StartPage", ))
        start_page_button.pack()

        names_of_cards = ['card1', 'card2', 'card3', 'card4', 'card5']
        for card in names_of_cards:
            check_var = tk.IntVar()
            check = tk.Checkbutton(
                self,
                text=card,
                variable=check_var,
                command=lambda card=card, var=check_var: self.controller.on_check(var, card)
            )
            check.pack()

    