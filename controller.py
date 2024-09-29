import tkinter as tk
from tkinter import messagebox
from frames.startPage import StartPage  
from frames.gamePage import GamePage  
from frames.deckPage import DeckPage
from fonts.font import *

class Controller(tk.Tk):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        self.title('Inscryption')
        self.geometry('1920x1080')
        self.fullscreen = True
        self.bind("<F11>", self.toggle_fullscreen)
        
        #self.bind("<Escape>", self.end_fullscreen)

        #self.overrideredirect(True)
    
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        pages = [StartPage, GamePage, DeckPage] # Add a new page here

        for page in pages:
            frame = page(container, self)
            self.frames[page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()

    def search_card(self, entry):
        print(entry.get())

    def on_check(self, var, card):
        state = var.get()
        print(f"{card} is {'selected' if state else 'deselected'}")

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
           #self.overrideredirect(True)
            self.attributes("-fullscreen", True)
        else:
            #self.overrideredirect(False)
            self.attributes("-fullscreen", False)
        return "break"
    
    def end_fullscreen(self, event=None):
        self.fullscreen = False
        self.attributes("-fullscreen", False)
        return "break"
    
    def exit_game(self):
        self.quit()

    #def create_container_place(self):
    #    pass

    def buy_card_interface(self):
        messagebox.showinfo("Inscryption", "Voce comprou uma carta")

    def create_container_grid(self, parent, text, padx, pady, row, col, textLabel):
        container = tk.LabelFrame(parent, text=text, padx=padx, pady=pady)
        container.grid(row = row, column= col, padx=5, pady=5, sticky="nsew")

        label = tk.Label(container, text=textLabel)
        label.pack(padx=5, pady=5)

        return container

    def create_hand_UI(self, page, container):
        for row in range(3):
            for col in range(3):
                container_card = self.create_container_grid(container, f"Container {row} {col}", 10, 10, row, col, f"Item {row * 3 + col + 1}")
                container_card.bind("<Button-1>", lambda e, r=row, c=col: self.select_card(page, r, c))

                if len(page.cards_hand_containers) <= row:
                    page.cards_hand_containers.append([])
                page.cards_hand_containers[row].append(container_card)

    def create_field_UI(self, page, container):
        for row in range(3):
            if row == 1:
                page.cards_field_containers.append([])
                continue
            for col in range(4):

                container_card = self.create_container_grid(container, f"Container {row} {col}", 10, 10, row, col, f"Item {row * 3 + col + 1}")
                container_card.bind("<Button-1>", lambda e, r=row, c=col: self.transfer_card(page, r, c))

                if len(page.cards_field_containers) <= row:
                    page.cards_field_containers.append([])
                page.cards_field_containers[row].append(container_card)

                

    def select_card(self, page, row, col):
        if page.selected_card:
            prev_row, prev_col = page.selected_card
            page.cards_hand_containers[prev_row][prev_col].config(bg="SystemButtonFace")

        page.cards_hand_containers[row][col].config(bg="yellow")
        page.selected_card = (row, col)

    def transfer_card(self, page, row, col):
        if page.selected_card:
            if page.occupied_slots[row][col]:
                return

            hand_row, hand_col = page.selected_card

            card = page.cards_hand_containers[hand_row][hand_col]

            field_card = tk.LabelFrame(page.cards_field_containers[row][col], text=card.cget("text"), padx=10, pady=10)
            field_card.pack(fill="both", expand=True)

            card.grid_forget()
            page.cards_hand_containers[hand_row][hand_col].config(bg="SystemButtonFace")
            page.selected_card = None

            page.occupied_slots[row][col] = True

            field_card.bind("<Button-1>", lambda e: None)
