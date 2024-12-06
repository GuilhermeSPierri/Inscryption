import tkinter as tk
from fonts.font import *
from widgets.button import Button
from frames.page import Page

class DeckPage(Page):

    def __init__(self, *args, **kwargs):
        self._list_of_cards = []

        ## TODO - Library nao deve ser instanciada em interface, e sim em controller

        super().__init__(*args, **kwargs)

    def create_widgets(self):
        label = tk.Label(self, text="Criador de Deck", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


        start_page_button = Button(self, "Voltar ao Menu", "show_frame", self.controller, ("StartPage", True))
        start_page_button.pack()

        save_deck_button = Button(self, "Salvar Deck", "save_deck", self.controller, (self._list_of_cards,))
        save_deck_button.pack()

        verify_deck_button = Button(self, "Verificar Deck Atual", "verify_deck", self.controller, (self,))
        verify_deck_button.pack()

        
        self.all_cards_containers = [[]]
        self.my_deck_containers = [[]]
        self.controller.create_deck_page_UI(self)
    
    def reset_page(self):
        self._list_of_cards = []
        self.all_cards_containers = [[]]
        self.my_deck_containers = [[]]
        self.controller.create_deck_page_UI(self)

    def names(self):
        return [card._name for card in self._list_of_cards]