import tkinter as tk
from fonts.font import *
from widgets.button import Button
from frames.page import Page
from functools import partial

class DeckPage(Page):

    def __init__(self, *args, **kwargs):
        self._all_cards_data = {}
        self._my_deck_data = {}

        ## TODO - Library nao deve ser instanciada em interface, e sim em controller

        super().__init__(*args, **kwargs)

    def create_widgets(self):
        label = tk.Label(self, text="Criador de Deck", font=LARGE_FONT, bg="#1a1a1a", fg="white")
        label.pack(pady=10, padx=10)


        save_deck_button = Button(
            self, 
            "Salvar  Deck  e  Sair", 
            0, 
            0, 
            "save_deck", 
            self.controller, 
            (lambda: self.get_my_deck_data(),),
            self.custom_font_buttons
        )
        save_deck_button.place(relx=0.46, rely=0.11, relwidth=0.05, relheight=0.05, width=60, height=10)


        self.all_cards_containers = [[]]
        self.my_deck_containers = [[]]
        self.controller.create_deck_page_UI(self)

    
    def get_all_cards_data(self):
        return self._all_cards_data

    def set_all_cards_data(self, all_cards_data):
        self._all_cards_data = all_cards_data

    def get_my_deck_data(self):
        return self._my_deck_data

    def set_my_deck_data(self, deck_data):
        self._my_deck_data = deck_data