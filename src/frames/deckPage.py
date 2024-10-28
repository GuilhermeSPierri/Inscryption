import tkinter as tk
from fonts.font import *
from widgets.button import Button
from frames.page import Page
from library.library import Library  # Import the Library class

class DeckPage(Page):

    def __init__(self, *args, **kwargs):
        self.library = Library()  # Instantiate the Library class
        super().__init__(*args, **kwargs)

    def create_widgets(self):
        label = tk.Label(self, text="Criador de Deck", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        card_name = tk.StringVar()
        entry = tk.Entry(master=self, textvariable=card_name)
        entry.pack()

        start_page_button = Button(self, "Voltar ao Menu", "show_frame", self.controller, ("StartPage", ))
        start_page_button.pack()

        # Retrieve cards from the library
    
        cards = self.library.cards_model

        # Create a button for each card in the cards_model dictionary
        for card_id, card in cards.items():
            add_card_button = Button(self, card.name, "card_action", self.controller, (card_id,))
            add_card_button.pack()