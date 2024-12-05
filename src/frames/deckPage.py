import tkinter as tk
from fonts.font import *
from widgets.button import Button
from frames.page import Page

class DeckPage(Page):

    def __init__(self, *args, **kwargs):
        self.list_of_cards = []

        ## TODO - Library nao deve ser instanciada em interface, e sim em controller

        super().__init__(*args, **kwargs)

    def create_widgets(self):
        label = tk.Label(self, text="Criador de Deck", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


        start_page_button = Button(self, "Voltar ao Menu", "show_frame", self.controller, ("StartPage", ))
        start_page_button.pack()

        
        self.all_cards_containers = [[]]
        self.my_deck_containers = [[]]
        self.controller.create_deck_page_UI(self)