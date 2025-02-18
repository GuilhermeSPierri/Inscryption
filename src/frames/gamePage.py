import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from fonts.font import *
from widgets.button import Button
from config.config import *
from frames.page import Page

class GamePage(Page):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hand_data = {}
        self._local_field_data = {}
        self._remote_field_data = {}

    def create_widgets(self):
        self.selected_card = None
        self.occupied_slots = [[False for _ in range(4)] for _ in range(3)]
        self.occupied_slots_hand = [[False for _ in range(3)] for _ in range(3)]

        start_page_button = Button(self, "Desistir da partida", 200, 100, "receive_withdrawal_notification", self.controller)
        start_page_button.place(relx=0.90, rely=0.05, relwidth=0.05, relheight=0.05)

        buy_card_button = Button(
            self, 
            "Comprar Carta do Deck", 
            20, 
            10, 
            "buy_deck_card", 
            self.controller
        )
        buy_card_button.place(relx=0.90, rely=0.70, relwidth=0.05, relheight=0.05)

        buy_squirrel_button = Button(self, "Comprar Esquilo", 200, 100, "buy_squirrel_card", self.controller)
        buy_squirrel_button.place(relx=0.90, rely=0.80, relwidth=0.05, relheight=0.05)

        pass_turn_button = Button(self, "Passar Turno", 200, 100, "pass_turn", self.controller)
        pass_turn_button.place(relx=0.90, rely=0.50, relwidth=0.05, relheight=0.05)

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

        # Add a label to display the scale information
        self.scale_label = tk.Label(self, text="Your points: 0 | Enemy points: 0", font=LARGE_FONT)
        self.scale_label.place(relx=0.05, rely=0.95, anchor="w")

        self.bones_label = tk.Label(self, text="Bones: 0", font=LARGE_FONT)
        self.bones_label.place(relx=0.95, rely=0.95, anchor="e")

    def reset_page(self):
        # Limpa os widgets existentes
        for widget in self.winfo_children():
            widget.destroy()

        # Reseta os estados
        self.occupied_slots = [[False for _ in range(4)] for _ in range(3)]
        self.occupied_slots_hand = [[False for _ in range(3)] for _ in range(3)]
        self.cards_hand_containers = [[]]
        self.cards_field_containers = [[]]

        # Recria a UI
        self.create_widgets()

    def get_hand_data(self):
        return self._hand_data