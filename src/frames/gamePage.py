import tkinter as tk
from fonts.font import *
from widgets.button import Button
from config.config import *
from frames.page import Page

class GamePage(Page):

    def create_widgets(self):
        self.selected_card = None
        self.occupied_slots = [[False for _ in range(4)] for _ in range(3)]
        self.occupied_slots_hand = [[False for _ in range(3)] for _ in range(3)]

        start_page_button = Button(self, "Voltar ao Menu", "show_frame", self.controller, ("StartPage", ))
        start_page_button.place(relx=0.90, rely=0.05, relwidth=0.05, relheight=0.05)

        buy_card_button = Button(self, "Comprar Carta", "buy_card_interface", self.controller)
        buy_card_button.place(relx=0.90, rely=0.95, relwidth=0.05, relheight=0.05)

        container_hand = tk.Frame(self, bg="lightgrey", relief=tk.RAISED, borderwidth=2)
        container_hand.place(relx=0.05, rely=0.05, relwidth=0.30, relheight=0.90)

        container_field = tk.Frame(self, bg="red", relief=tk.RAISED, borderwidth=2)
        container_field.place(relx=0.4, rely=0.05, relwidth=0.40, relheight=0.90)

        for i in range(3):
            container_hand.grid_columnconfigure(i, weight=1)
            container_hand.grid_rowconfigure(i, weight=1)

            container_field.grid_rowconfigure(i, weight=1)
        for j in range(4):
            container_field.grid_columnconfigure(j, weight=1)

        self.cards_hand_containers = [[]]
        self.cards_field_containers = [[]]
        self.controller.create_hand_UI(self, container_hand)
        self.controller.create_field_UI(self, container_field)
    

    