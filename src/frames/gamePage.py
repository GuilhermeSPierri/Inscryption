import tkinter as tk
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
        start_page_button = Button(self, "Desistir  da  partida", 0, 0, "receive_withdrawal_notification", self.controller, font=self.custom_font_buttons)
        start_page_button.place(relx=0.90, rely=0.05, relwidth=0.05, relheight=0.05, width=60, height=10)

        buy_card_button = Button(
            self, 
            "Comprar  Carta  do  Deck", 
            0, 
            0, 
            "buy_deck_card", 
            self.controller,
            font=self.custom_font_buttons
        )
        buy_card_button.place(relx=0.89, rely=0.70, relwidth=0.05, relheight=0.05, width=90, height=10)

        buy_squirrel_button = Button(self, "Comprar  Esquilo", 0, 0, "buy_squirrel_card", self.controller, font=self.custom_font_buttons)
        buy_squirrel_button.place(relx=0.90, rely=0.80, relwidth=0.05, relheight=0.05, width=40, height=10)

        pass_turn_button = Button(self, "Passar  Turno", 0, 0, "pass_turn", self.controller, font=self.custom_font_buttons)
        pass_turn_button.place(relx=0.90, rely=0.50, relwidth=0.05, relheight=0.05, width=40, height=10)

        container_hand = tk.Frame(self, bg="lightgrey", relief=tk.RAISED, borderwidth=2)
        container_hand.place(relx=0.05, rely=0.05, relwidth=0.30, relheight=0.90)

        container_field = tk.Frame(self, bg="#fcd33f", relief=tk.RAISED, borderwidth=2)
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
        self.scale_label = tk.Label(self, text="Your scale: 0 | Enemy scale: 0", font=LARGE_FONT)
        self.scale_label.place(relx=0.05, rely=0.95, anchor="w")

        bones_image = tk.PhotoImage(file="assets/bones.png").zoom(2, 2)  # Enlarge the image 2x
        self.bones_label = tk.Label(self, text="Bones: 0", font=LARGE_FONT, image=bones_image, compound="center")
        self.bones_label.image = bones_image  # Keep a reference to the image
        self.bones_label.config(width=bones_image.width(), height=bones_image.height(),
        borderwidth=0, highlightthickness=0, padx=0, pady=0)  # Set the label size to the image size


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