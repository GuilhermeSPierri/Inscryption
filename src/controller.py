import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from frames.startPage import StartPage  
from frames.gamePage import GamePage  
from frames.deckPage import DeckPage
from fonts.font import *
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from problem_domain.library.library import Library
from problem_domain.table import Table

class Controller(DogPlayerInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.library = Library()
        self.frames = {}
        self.table = Table()
        self.pages = [StartPage, GamePage, DeckPage] # Add a new page here
        player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)
        


    ######### Create UI #########

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

    def create_deck_page_UI(self, page):
        # Get all cards and deck information
        all_cards_dict = self.get_all_cards()
        deck_info = self.get_deck_info()

        # Convert dictionaries to lists for iteration
        all_cards_list = list(all_cards_dict.items())
        deck_cards_list = list(deck_info.items())

        left_container = tk.Frame(page, bg="lightgrey", relief=tk.RAISED, borderwidth=2)
        left_container.place(relx=0.05, rely=0.05, relwidth=0.30, relheight=0.90)

        for i in range(4):
            left_container.grid_columnconfigure(i, weight=1)
            left_container.grid_rowconfigure(i, weight=1)

        # Create the label for all cards on the left
        for row in range(5):
            for col in range(4):
                index = row * 4 + col
                
                if index < len(all_cards_list):
                    _, card_object = all_cards_list[index]
                    card_name = card_object.get_name() # Assuming the CardObject has a `name` attribute
                    
                    # Create container with card name
                    left_container_card = self.create_container_grid(
                        left_container, 
                        "", 
                        10, 
                        10, 
                        row, 
                        col,  # Offset the column to the right side
                        f"{card_name} \n Damage: {card_object.get_damage()} \n HP: {card_object.get_hp()}"
                    )
                    left_container_card.bind("<Button-1>", lambda e, object = card_object: self.add_card_to_deck_UI(object, page))

                    if len(page.all_cards_containers) <= row:
                        page.all_cards_containers.append([])
                    page.all_cards_containers[row].append(left_container_card)
                else:
                    # Empty placeholder
                    placeholder = self.create_container_grid(left_container, "Empty", 10, 10, row, col, "Empty")
                    if len(page.all_cards_containers) <= row:
                        page.all_cards_containers.append([])
                    page.all_cards_containers[row].append(placeholder)

        right_container = tk.Frame(page, bg="lightgrey", relief=tk.RAISED, borderwidth=2)
        right_container.place(relx=0.65, rely=0.05, relwidth=0.30, relheight=0.90)

        for i in range(4):
            right_container.grid_columnconfigure(i, weight=1)
            right_container.grid_rowconfigure(i, weight=1)

        # Create the label for deck cards on the right
        for row in range(5):
            for col in range(4):
                index = row * 4 + col
                
                if index < len(deck_cards_list):
                    _, card_object = deck_cards_list[index]
                    card_name = card_object.get_name()  # Assuming the CardObject has a `name` attribute
                    
                    # Create container with card name
                    right_container_card = self.create_container_grid(
                        right_container, 
                        "", 
                        10, 
                        10, 
                        row, 
                        col,  # Offset the column to the right side
                        f"{card_name} \n Damage: {card_object.get_damage()} \n HP: {card_object.get_hp()}"
                    )
                    right_container_card.bind("<Button-1>", lambda e, card_index = index: self.remove_card_from_deck_UI(card_index,page))

                    if len(page.my_deck_containers) <= row:
                        page.my_deck_containers.append([])
                    page.my_deck_containers[row].append(right_container_card)

                    self.append_card_to_deck(page, card_object)

                else:
                    # Empty placeholder
                    placeholder = self.create_container_grid(right_container, "Empty", 10, 10, row, col, "Empty")
                    if len(page.my_deck_containers) <= row:
                        page.my_deck_containers.append([])
                    page.my_deck_containers[row].append(placeholder)

    def add_card_to_deck_UI(self, card_object, page):
        for row in range(5):
            for col in range(4):
                if page.my_deck_containers[row][col].cget("text") == "Empty":
                    # Replace the placeholder with the selected card
                    card_container = self.create_container_grid(
                        page.my_deck_containers[row][col].master,  # Parent container
                        "",
                        10,
                        10,
                        row,
                        col,
                        f"{card_object.get_name()} \n Damage: {card_object.get_damage()} \n HP: {card_object.get_hp()}"
                    )

                    # Bind the removal function to the newly added card
                    card_index = row * 4 + col  # Adjusted for correct index calculation
                    card_container.bind(
                        "<Button-1>",
                        lambda e, idx=card_index: self.remove_card_from_deck_UI(idx, page)
                    )

                    # Update the container reference
                    page.my_deck_containers[row][col].destroy()
                    page.my_deck_containers[row][col] = card_container

                    self.append_card_to_deck(page,card_object)

                    print(f"Added card '{card_object.get_name()}' to the right container at position ({row}, {col})")
                    return

        print("No empty slots available in the deck.")

    def append_card_to_deck(self, page, card_object):
        page._list_of_cards.append(card_object)
        print(f"Card '{card_object.get_name()}' added to the deck.")
        print(len(page._list_of_cards))
        print(page.names()) ##REMOVER ESSA FUNCAO 


    def remove_card_from_deck_UI(self, card_index, page):
        # Calculate the row and column of the card to be removed
        row = card_index // 4  # Adjusted for correct row calculation
        col = card_index % 4   # Adjusted for correct column calculation

        # Remove the card visually
        if row < len(page.my_deck_containers) and col < len(page.my_deck_containers[row]):
            card_container = page.my_deck_containers[row][col]
            card_container.destroy()

        # Update the deck list by removing the corresponding card
        if 0 <= card_index < len(page._list_of_cards):
            removed_card = self.remove_card_from_deck(card_index, page)
            print(f"Removed card: {removed_card.get_name()} at index {card_index}")

        # Reorganize the UI to fill gaps
        deck_size = len(page._list_of_cards)
        for i in range(deck_size):
            current_row = i // 4
            current_col = i % 4

            card_object = page._list_of_cards[i]
            card_name = card_object.get_name()
            card_damage = card_object.get_damage()
            card_life = card_object.get_life()

            # Create or update the card container
            if len(page.my_deck_containers) > current_row and len(page.my_deck_containers[current_row]) > current_col:
                page.my_deck_containers[current_row][current_col].destroy()  # Remove placeholder if present

            container = self.create_container_grid(
                page.my_deck_containers[current_row][current_col].master,  # Parent container
                "",
                10,
                10,
                current_row,
                current_col,
                f"{card_name} \n Damage: {card_damage} \n Life: {card_life}"
            )
            container.bind(
                "<Button-1>",
                lambda e, idx=i: self.remove_card_from_deck_UI(idx, page)
            )

            # Update the reference
            page.my_deck_containers[current_row][current_col] = container

        # Fill the remaining slots with placeholders
        for i in range(deck_size, 20):  # Assuming max deck size is 20
            current_row = i // 4
            current_col = i % 4

            if len(page.my_deck_containers) > current_row and len(page.my_deck_containers[current_row]) > current_col:
                page.my_deck_containers[current_row][current_col].destroy()

            placeholder = self.create_container_grid(
                page.my_deck_containers[current_row][current_col].master,  # Parent container
                "Empty",
                10,
                10,
                current_row,
                current_col,
                "Empty"
            )
            page.my_deck_containers[current_row][current_col] = placeholder

    def remove_card_from_deck(self, card_index, page):
        return page._list_of_cards.pop(card_index)

    def verify_deck(self, page):
        print("tamanho do deck")
        print(self.table._local_deck.get_deck_size())
        for _ in range(len(page._list_of_cards)):
            self.remove_card_from_deck_UI(0, page)
        print("Deck reset")
        print(self.table._local_deck.get_deck_size())
        for i in range(self.table._local_deck.get_deck_size()):
            card = self.table._local_deck.get_card_list()[i]
            self.add_card_to_deck_UI(card, page)
    
    def get_all_cards(self):
        return self.library.get_all_cards()
    
    def get_deck_info(self):
        deck = self.table._local_player.get_deck()
        return {idx: card for idx, card in enumerate(deck.get_card_list())}

    def save_deck(self, list_of_cards):
        # salvar o deck
        if len(list_of_cards) == 20:
            self.table.update_local_deck(list_of_cards)
            messagebox.showinfo("Deck salvo", "Deck salvo com sucesso")
        else:
            messagebox.showerror("Erro", "Deck precisa ter 20 cartas")
        


                
    ######### Logic for all the pages #########

    def end_fullscreen(self, event=None):
        self.fullscreen = False
        self.attributes("-fullscreen", False)
        return "break"
    
    def fill_pages(self, main_window):
        container = tk.Frame(main_window)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        for page in self.pages:
            frame = page(container, self)
            self.frames[page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
    ######### Logic for the start page #########

    def show_frame(self, page_name, reset):
        frame = self.get_frame(page_name)
        if frame:
            if reset:
                frame.reset_page()
            frame.tkraise()
        else:
            messagebox.showerror("Error", f"Page {page_name} not found")

    def get_frame(self, page_name):
        return self.frames.get(page_name)

    def exit_game(self):
        quit()

    ######### Logic for the game page #########

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

    def buy_deck_card(self):
        # comprar uma carta
        pass

    def buy_squirrel_card(self):
        # comprar um esquilo
        pass

    def update_gui(self):
        # atualizar a interface grafica
        pass

    def verify_card_cost(self):
        # verificar o custo da carta
        pass

    def place_card(self, card, pos):
        # colocar a carta no campo
        pass


    def buy_card_interface(self):
        messagebox.showinfo("Inscryption", "Voce comprou uma carta")

    def skip_turn(self):
        match_status = self.dog_server_interface.proxy.get_status()
        if match_status == 2:
            self.receive_withdrawal_notification()
            self.show_frame("StartPage")
        else:
            pass

        

    
    ######### Logic for the deck page #########

    def add_card_to_interface(self, id):
        # checar se o deck ja nao esta cheio
        pass

    def remove_card_from_interface(self, id):
        # checar se o deck ja nao esta vazio
        pass

    def show_deck(self):
        # mostrar o deck
        pass

    def get_number_cards_local_deck(self):
        # retornar o numero de cartas no deck local
        pass

    ######### Logic for the player #########

    def invoke_card(self, card):
        # invocar a carta
        pass

    def get_card_by_id(self, id):
        return self.library.get_card(id)

    ######### Logic for the dog #########

    def start_match(self): 
        start_status = self.dog_server_interface.start_match(2)
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        if message == "Partida iniciada":
            self.show_frame("GamePage")

    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        if message == "Partida iniciada":
            self.show_frame("GamePage")

    def receive_withdrawal_notification(self):
        self.dog_server_interface.proxy.get_status()
        messagebox.showinfo(message="O oponente desistiu da partida")
        self.show_frame("StartPage")

    def make_withdrawal(self):
        self.dog_server_interface.make_withdrawal()
        self.show_frame("StartPage")
        

    

