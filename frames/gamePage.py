import tkinter as tk
from fonts.font import *
from button import Button
from config import *

class GamePage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.selected_card = None
        self.occupied_slots = [[False for _ in range(4)] for _ in range(3)]

        start_page_button = Button(self, "Voltar ao Menu", "show_frame", controller, ("StartPage", ))
        start_page_button.place(relx=0.90, rely=0.05, relwidth=0.05, relheight=0.05)

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
        self.create_hand_UI(container_hand)
        self.create_field_UI(container_field)

    def create_hand_UI(self, container):
        for row in range(3):
            for col in range(3):
                container_card = tk.LabelFrame(container, text=f"Container {row} {col}", padx=10, pady=10)
                container_card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                
                label = tk.Label(container_card, text=f"Item {row * 3 + col + 1}")
                label.pack(padx=5, pady=5)

                container_card.bind("<Button-1>", lambda e, r=row, c=col: self.select_card(r, c))

                if len(self.cards_hand_containers) <= row:
                    self.cards_hand_containers.append([])
                self.cards_hand_containers[row].append(container_card)

    def create_field_UI(self, container):
        for row in range(3):
            if row == 1:
                self.cards_field_containers.append([])
                continue
            for col in range(4):

                container_card = tk.LabelFrame(container, text=f"Container {row} {col}", padx=10, pady=10)
                container_card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

                label = tk.Label(container_card, text=f"Item {row * 3 + col + 1}")
                label.pack(padx=5, pady=5)

                if len(self.cards_field_containers) <= row:
                    self.cards_field_containers.append([])
                self.cards_field_containers[row].append(container_card)

                container_card.bind("<Button-1>", lambda e, r=row, c=col: self.transfer_card(r, c))

    def select_card(self, row, col):
        if self.selected_card:
            prev_row, prev_col = self.selected_card
            self.cards_hand_containers[prev_row][prev_col].config(bg="SystemButtonFace")

        self.cards_hand_containers[row][col].config(bg="yellow")
        self.selected_card = (row, col)

    def transfer_card(self, row, col):
        if self.selected_card:
            if self.occupied_slots[row][col]:
                return

            hand_row, hand_col = self.selected_card

            card = self.cards_hand_containers[hand_row][hand_col]

            field_card = tk.LabelFrame(self.cards_field_containers[row][col], text=card.cget("text"), padx=10, pady=10)
            field_card.pack(fill="both", expand=True)

            card.grid_forget()
            self.cards_hand_containers[hand_row][hand_col].config(bg="SystemButtonFace")
            self.selected_card = None

            self.occupied_slots[row][col] = True

            field_card.bind("<Button-1>", lambda e: None)