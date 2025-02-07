import tkinter as tk
from functools import partial
from tkinter import messagebox
from tkinter import simpledialog
from frames.startPage import StartPage  
from frames.gamePage import GamePage  
from frames.deckPage import DeckPage
from fonts.font import *
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from problem_domain.library import Library
from problem_domain.table import Table
from problem_domain.position import Position
from problem_domain.cards.sacrificeCard import SacrificeCard

class Controller(DogPlayerInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.library = Library()
        self.frames = {}
        self._table = Table()
        self._players = None
        self.pages = [StartPage, GamePage, DeckPage] # Add a new page here
        player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)
        
    ######### Logic for general purposes #########

    def create_container_grid(self, parent, text, padx, pady, row, col, textLabel):
        container = tk.LabelFrame(parent, text=text, padx=padx, pady=pady)
        container.grid(row = row, column= col, padx=5, pady=5, sticky="nsew")

        label = tk.Label(container, text=textLabel)
        label.pack(padx=5, pady=5)

        return container
    
    ######### Logic for the game page #########
    
    def create_hand_UI(self, page, container):

        if self._players:
            if self._players[0][1] == self._table._local_player.get_id():
                hand_dict = {idx: {
                    "id": card,
                    "name": card.get_name(),
                    "damage": card.get_damage(),
                    "life": card.get_hp()
                } for idx, card in self.get_local_hand().items()}

            elif self._players[1][1] == self._table._local_player.get_id():
                hand_dict = {idx: {
                    "id": card,
                    "name": card.get_name(),
                    "damage": card.get_damage(),
                    "life": card.get_hp()
                } for idx, card in self.get_remote_hand().items()}

            for row in range(3):
                for col in range(3):
                    index = row * 3 + col
                    
                    # Check if the index exists in hand_data
                    if index in hand_dict:
                        card_data = hand_dict[index]
                        card_label = f"{str(card_data['id'])[-8:]} \n {card_data['name']} \n Damage: {card_data['damage']} \n Life: {card_data['life']}"
                    else:
                        # Empty slot for unavailable indices
                        card_label = "Empty"
                    
                    # Create the card container
                    container_card = self.create_container_grid(
                        container,
                        f"Container {row} {col}",
                        10,
                        10,
                        row,
                        col,
                        card_label
                    )
                    
                    # Bind the click event for card selection
                    container_card.bind(
                        "<Button-1>",
                        lambda event, page=page, position_in_field=None, position_in_hand=index: 
                        self.select_position(page, position_in_field, position_in_hand, event)
                    )

                    # Ensure the cards_hand_containers list structure is maintained
                    if len(page.cards_hand_containers) <= row:
                        page.cards_hand_containers.append([])
                    page.cards_hand_containers[row].append(container_card)




    def create_field_UI(self, page, container):
        for row in range(3):
            if row == 1:  # Continua ignorando a linha do meio
                page.cards_field_containers.append([])
                continue

            for col in range(4):
                container_card = self.create_container_grid(
                    container,
                    f"Container {row} {col}",
                    10,
                    10,
                    row,
                    col,
                    f"Item {row * 2 + col}"
                )

                # Bind usando partial para garantir a passagem correta das coordenadas
                container_card.bind(
                    "<Button-1>",
                    lambda event, page=page, position_in_field=col, position_in_hand=None, row=row: 
                    self.select_position(page, position_in_field, position_in_hand, row, event)
                )

                if len(page.cards_field_containers) <= row:
                    page.cards_field_containers.append([])
                page.cards_field_containers[row].append(container_card)
        
    def select_card(self, page, selected_position, position_in_hand, row=None):
        selected_card = self._table.select_card(selected_position)

        if not hasattr(page, 'selected_cards'):
            page.selected_cards = []

        if selected_position.get_origin() == "hand":
            # Deselect the previously selected card in hand
            col = position_in_hand % 3
            row = position_in_hand // 3

            print(f"DENTRO DE SELECT_CARD = Selected card: {selected_card}", f"Position: {row} {col}", f"from {selected_position.get_origin()}")

            # If clicking the same card again, just deselect it
            if (row, col) == page.selected_card:
                page.cards_hand_containers[row][col].config(bg="SystemButtonFace")
                page.selected_card = None
                return

            if page.selected_card:
                prevrow, prevcol = page.selected_card
                page.cards_hand_containers[prevrow][prevcol].config(bg="SystemButtonFace")
                page.selected_card = (row, col)

            # Highlight the new selected card in hand
            if selected_card is not None:
                page.cards_hand_containers[row][col].config(bg="yellow")
                page.selected_card = (row, col)
            else:
                page.selected_card = None

        elif selected_position.get_origin() == "field":
            col = position_in_hand % 4

            print(f"DENTRO DE SELECT_CARD = Selected card: {selected_card}", f"Position: {row} {col}", f"from {selected_position.get_origin()}")
            # If clicking the same card again, just deselect it
            if (row, col) in page.selected_cards:
                page.selected_cards.remove((row, col))
                page.cards_field_containers[row][col].config(bg="SystemButtonFace")
                #self._table.get_local_field().remove_card_from_field(selected_card)
                self._table.get_local_field().remove_from_sacrifice_cards(selected_card)
                return

            # Highlight the new selected card in the field
            elif selected_card is not None and selected_card.get_name() != "Empty":
                print(f"DENTRO DO IF LA: Selected card: {selected_card}", f"Position: {row} {col}", f"from {selected_position.get_origin()}")
                page.cards_field_containers[row][col].config(bg="lightblue")
                page.selected_cards.append((row, col))
                self._table.get_local_field().append_to_sacrifice_cards(selected_card)
                print("tamanho da lista de sacrificio: ", len(self._table.get_local_field().get_sacrifice_cards()) )
            else:
                page.selected_cards = []

    def select_position(self, page, position_in_field=None, position_in_hand=None, row=None,event=None):
        turn_player = self._table.get_turn_player()

        if position_in_field is not None:
            if turn_player.get_id() == self._table.get_local_player().get_id():
                selected_position = self._table.get_local_field().get_position_in_field(position_in_field)

            selected_position.set_field(True)

        if position_in_hand is not None:
            selected_position = self._table.get_position_in_hand(position_in_hand)
            selected_position.set_hand(True)

        print("ID's:", turn_player.get_id(), "id local player da mesa :", self._table._local_player.get_id())
        if turn_player.get_id() == self._table._local_player.get_id() and selected_position is not None:
            occupied = self._table.check_position(selected_position)

            if occupied:
                if position_in_field is not None:
                    print("valor de row::::")
                    self.select_card(page, selected_position, position_in_field, row)
                elif position_in_hand is not None:
                    self.select_card(page, selected_position, position_in_hand)
            if not occupied and selected_position._field:
                self.invoke_card(selected_position, position_in_field, turn_player, row)

    ################### Logic for the deck page ###################

    def create_deck_page_UI(self, page):
        # Get all cards and deck information
        all_cards_dict = {idx: {
            "name": card.get_name(),
            "damage": card.get_damage(),
            "life": card.get_hp()
        } for idx, card in self.get_all_cards().items()}

        deck_info_dict = {idx: {
            "name": card.get_name(),
            "damage": card.get_damage(),
            "life": card.get_hp()
        } for idx, card in self.get_deck_info().items()}

        page.set_all_cards_data(all_cards_dict)
        page.set_my_deck_data(deck_info_dict)

        # Create UI for the left container (all cards)
        left_container = tk.Frame(page, bg="lightgrey", relief=tk.RAISED, borderwidth=2)
        left_container.place(relx=0.05, rely=0.05, relwidth=0.30, relheight=0.90)

        # Create UI for the right container (deck cards)
        right_container = tk.Frame(page, bg="lightgrey", relief=tk.RAISED, borderwidth=2)
        right_container.place(relx=0.65, rely=0.05, relwidth=0.30, relheight=0.90)

        for i in range(4):
            left_container.grid_columnconfigure(i, weight=1)
            left_container.grid_rowconfigure(i, weight=1)
            right_container.grid_columnconfigure(i, weight=1)
            right_container.grid_rowconfigure(i, weight=1)

        self.populate_card_container(
            left_container, 
            page.get_all_cards_data(), 
            lambda card_data, idx: self.add_card_to_deck_UI(card_data, idx, page),
            page.all_cards_containers
        )

        self.populate_card_container(
            right_container, 
            page.get_my_deck_data(), 
            lambda card_data, idx: self.remove_card_from_deck_UI(idx, page),
            page.my_deck_containers
        )


    def populate_card_container(self, container, card_data_dict, on_click, container_list):
        for row in range(5):
            for col in range(4):
                index = row * 4 + col
                
                if index < len(card_data_dict):
                    card_data = card_data_dict[index]
                    card_label = f"{card_data['name']} \n Damage: {card_data['damage']} \n Life: {card_data['life']}"
                    card_container = self.create_container_grid(container, "", 10, 10, row, col, card_label)

                    # Bind the click event
                    card_container.bind("<Button-1>", lambda e, cd=card_data, idx=index: on_click(cd, idx))
                else:
                    # Empty placeholder
                    card_container = self.create_container_grid(container, "Empty", 10, 10, row, col, "Empty")

                # Store reference
                if len(container_list) <= row:
                    container_list.append([])
                container_list[row].append(card_container)
   
    def add_card_to_deck_UI(self, card_data, index, page):
        for row in range(5):
            for col in range(4):
                if page.my_deck_containers[row][col].cget("text") == "Empty":
                    # Replace the placeholder with the selected card
                    card_label = f"{card_data['name']} \n Damage: {card_data['damage']} \n Life: {card_data['life']}"
                    card_container = self.create_container_grid(
                        page.my_deck_containers[row][col].master,  # Parent container
                        "",
                        10,
                        10,
                        row,
                        col,
                        card_label
                    )

                    # Bind the removal function
                    card_container.bind("<Button-1>", lambda e, idx=row * 4 + col: self.remove_card_from_deck_UI(idx, page))

                    # Update UI reference
                    page.my_deck_containers[row][col].destroy()
                    page.my_deck_containers[row][col] = card_container

                    # Update deck data
                    page.get_my_deck_data()[row * 4 + col] = card_data
                    return

        messagebox.showinfo("Deck cheio", "Seu deck já possui o tamanho máximo")

    def remove_card_from_deck_UI(self, card_index, page):
        # Calculate row and column
        row = card_index // 4
        col = card_index % 4

        # Remove UI element
        if row < len(page.my_deck_containers) and col < len(page.my_deck_containers[row]):
            page.my_deck_containers[row][col].destroy()

        # Remove from deck data
        if card_index in page.get_my_deck_data():
            removed_card = page.get_my_deck_data().pop(card_index)

        # Fill the gap in the UI
        placeholder = self.create_container_grid(
            page.my_deck_containers[row][col].master,
            "Empty",
            10,
            10,
            row,
            col,
            "Empty"
        )
        page.my_deck_containers[row][col] = placeholder

    def save_deck(self, deck_data_func):
        # Salvar o deck
        print("Salvando deck...")
        deck_data = deck_data_func()
        try:
            if len(deck_data) == 20:
                self._table._local_deck.reset_deck()
                for _, card_dict in deck_data.items():
                    card_object = self.library.get_card(card_dict["name"])
                    self._table._local_deck.add_card_to_deck(card_object)
                messagebox.showinfo("Deck salvo", "Deck salvo com sucesso")

                # Atualiza a interface da GamePage
                game_page = self.get_frame("GamePage")
                game_page.reset_page()

                self.show_frame("StartPage")
            else:
                messagebox.showerror("Erro", "Deck precisa ter 20 cartas")
        except:
            pass

    ######### Logic for the library #########

    def get_all_cards(self):
        return self.library.get_all_cards()
    
    def get_deck_info(self):
        deck = self._table.get_local_deck()
        return {idx: card for idx, card in enumerate(deck.get_card_list())}
    
    def get_local_hand(self):
        hand = self._table.get_local_hand()
        return {idx: card for idx, card in enumerate(hand.get_card_list())}
    
    def get_remote_hand(self):
        hand = self._table.get_remote_hand()
        return {idx: card for idx, card in enumerate(hand.get_card_list())}

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

    def show_frame(self, page_name):
        frame = self.get_frame(page_name)
        if frame:
            frame.tkraise()
        else:
            messagebox.showerror("Error", f"Page {page_name} not found")

    def get_frame(self, page_name):
        return self.frames.get(page_name)

    def exit_game(self):
        quit()

    ######### Logic for the game page #########

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
        # Get the top card from the deck
        turn_player = self._table.get_turn_player()
        if turn_player.get_id() == self._table._local_player.get_id():
            top_card = self._table.buy_deck_card()
            if top_card:
                
                # Update the UI
                game_page = self.get_frame("GamePage")
                if game_page:
                    self.update_hand_UI(game_page)
                    messagebox.showinfo("Inscryption", "Você comprou uma carta do deck")
            else:
                messagebox.showinfo("Inscryption", "O deck está vazio")

    def update_hand_UI(self, game_page):
        hand_dict = {idx: {
            "id": card,
            "name": card.get_name(),
            "damage": card.get_damage(),
            "life": card.get_hp()
        } for idx, card in self.get_local_hand().items()}
        
        for row in range(3):
            for col in range(3):
                index = row * 3 + col
                if index in hand_dict:
                    card_data = hand_dict[index]
                    card_label = f"{str(card_data['id'])[-8:]} \n{card_data['name']} \n Damage: {card_data['damage']} \n Life: {card_data['life']}"
                else:
                    card_label = "Empty"
                
                container_card = game_page.cards_hand_containers[row][col]
                for widget in container_card.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(text=card_label)

    #def update_scale_UI(self, game_page, move):
        # Atualizar a balança com base na jogada
        #local_points = self._table._scale._local_player_points
        #remote_points = self._table._scale._remote_player_points
        #game_page.scale_label.config(text=f"Local: {local_points} | Remote: {remote_points}")


    def buy_squirrel_card(self):
        turn_player = self._table.get_turn_player()
        print("turno do jogador: ", turn_player.get_id())
        print("este é o jogador local da mesa: ", self._table._local_player.get_id())
        if turn_player.get_id() == self._table._local_player.get_id():
            # Get the top squirrel card from the deck
            squirrel_card = self._table.buy_squirrel_card()
            if squirrel_card:
                # Update the UI
                game_page = self.get_frame("GamePage")
                if game_page:
                    self.update_hand_UI(game_page)
                    messagebox.showinfo("Inscryption", "Você comprou um Esquilo")
            else:
                messagebox.showinfo("Inscryption", "Você já comprou uma carta!")


    def update_gui(self, move):
        # Atualiza a interface com base na jogada
        game_page = self.get_frame("GamePage")
        if game_page:
            # Atualiza o campo de batalha
            self.update_field_UI(game_page, move)

            # Atualiza a escala (se necessário)
            #self.update_scale_UI(game_page, move)


    def update_field_UI(self, game_page, move):
        # Atualiza o campo de batalha com base na jogada
        positions = move.get("position", [])
        for row in range (2):
            if row == 1:
                continue
            for col in range(4):

            #Para atualizar o local_field
                print(f'Posição {col}: {positions[col]}')
                print('Posições:', positions)
                posicao = Position.from_dict(positions[col])
                self._table.get_local_field().set_position(col, posicao)
                # Atualizar o contêiner correspondente no campo de batalha
                print(f'row: {row}, col: {col}')
                container = game_page.cards_field_containers[0][col]
                # Verificar se há uma carta na posição
                
                if positions[col]["occupied"]:
                    card_data = SacrificeCard.from_dict(positions[col]["card"])
                    print("AQUIIIIIIIIIIIIIIIIIIIIIIII", str(posicao.get_card)[-8:], "ZZZZZZZZZZZZZZZZZZZZZZZZZZZ", str(posicao.get_card))
                    card_label = f"{str(card_data)[-8:]} \n {card_data.get_name()} \n Damage: {card_data.get_damage()} \n Life: {card_data.get_hp()}"
                else:
                    card_label = "Empty"

                for widget in container.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(text=card_label)

                # Para atualizar o remote field
                for row in range(2,3):
                    for col in range(4,8):
                        print(f'Posição {col}: {positions[col-4]}')
                        print('Posições:', positions)
                        posicao = Position.from_dict(positions[col-4])
                        self._table.get_remote_field().set_position(col-4, posicao)
                        # Atualizar o contêiner correspondente no campo de batalha
                        print(f'row: {row}, col: {col}')
                        container = game_page.cards_field_containers[2][col-4]
                        # Verificar se há uma carta na posição
                        if positions[col]["occupied"]:
                            print("TRUE OR FALSE: ", positions[col]["occupied"])
                            print("tem uma carta: ", self._table.get_remote_field().get_position_in_field(col-4).get_card(),
                            "na posicao: ", self._table.get_remote_field().get_position_in_field(col-4))
                            card_data = Position.from_dict(positions[col-4]).get_card()
                            print("AQUIIIIIIIIIIIIIIIIIIIIIIII", str(posicao.get_card)[-8:], "ZZZZZZZZZZZZZZZZZZZZZZZZZZZ", str(posicao.get_card))
                            card_label = f"{str(card_data)[-8:]} \n {card_data.get_name()} \n Damage: {card_data.get_damage()} \n Life: {card_data.get_hp()}"
                        else:
                            card_label = "Empty"

                        for widget in container.winfo_children():
                            if isinstance(widget, tk.Label):
                                widget.config(text=card_label)

    def place_card(self, card, pos):
        # colocar a carta no campo
        pass

    def buy_card_interface(self):
        self._table.b
        messagebox.showinfo("Inscryption", "Voce comprou uma carta")

    def pass_turn(self):
        print("jogador com o turno", self._table.get_turn_player().get_id())
        winner = self._table.pass_turn()
        print("jogador com o turno", self._table.get_turn_player().get_id())

        if winner != "":
            if winner == "local_player":
                messagebox.showinfo("Jogo finalizado", "O jogador Local venceu")
                self.show_frame("StartPage")
            elif winner == "remote_player":
                messagebox.showinfo("Jogo finalizado", "O jogador Remoto venceu")
                self.show_frame("StartPage")

        elif winner == "":

            if self._table._local_player.get_id() < self._table._remote_player.get_id():
                # Criar um dicionário com a jogada atual
                local_positions = self._table.get_local_field().get_positions()
                remote_positions = self._table.get_remote_field().get_positions()
            
            else:
                local_positions = self._table.get_remote_field().get_positions()
                remote_positions = self._table.get_local_field().get_positions()

            all_positions = local_positions + remote_positions

            move = {
                "card": [card.to_dict() for card in self._table.get_local_field().get_sacrifice_cards()],  # Convert cards to dict
                "position": [position.to_dict() for position in all_positions],  # Convert positions to dict
                "action": "invoke_card",  # Exemplo: ação realizada
                "match_status": self._table.get_match_status(),  # Adicionando o status da partida
                "turn_player_id" : self._table.get_turn_player().get_id()
            }

            print(move["position"])
            # Enviar a jogada para o DOG server
            self.dog_server_interface.proxy.send_move(move)

    ######### Logic for the player #########

    def invoke_card(self, selected_position, position_in_field, player, row=None):
        invoked_card = self._table.invoke_card(selected_position, player, row)

        # Update the field UI to reflect the invoked card
        game_page = self.get_frame("GamePage")
        if invoked_card:
            col = position_in_field
            card_data = {
                "id": invoked_card,
                "name": invoked_card.get_name(),
                "damage": invoked_card.get_damage(),
                "life": invoked_card.get_hp()
            }
            card_label = f"{str(card_data['id'])[-8:]} \n {card_data['name']} \n Damage: {card_data['damage']} \n Life: {card_data['life']}"

            # Update the field container with the card data
            container = game_page.cards_field_containers[row][col]
            container.config(bg="SystemButtonFace")  # Reset the background

            for widget in container.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(text=card_label)

            # Ensure the card is no longer in the hand
            print(f"Selected card: {game_page.selected_card}")
            if game_page.selected_card:
                hand_row, hand_col = game_page.selected_card
                # Reset the container in the hand to its original state
                container = game_page.cards_hand_containers[hand_row][hand_col]
                container.config(bg="SystemButtonFace")  # Reset the background
                
                # Update the tk.Label (textLabel) inside the container
                for widget in container.winfo_children():
                    if isinstance(widget, tk.Label):  # Check if the child is the textLabel
                        widget.config(text="Empty")
                
                game_page.selected_card = None

            # Remove sacrifice cards from the field
            sacrifice_cards = self._table.get_local_field().get_sacrifice_cards()
            print(f"Sacrifice cards: {sacrifice_cards} AQUII")

            for sacrifice_card in sacrifice_cards:
                is_deleted = False
                for row in range(3):
                    if is_deleted:
                        break
                    for col in range(4):
                        if is_deleted:
                            break

                        try:
                            container = game_page.cards_field_containers[row][col]
                        except:
                            break

                        for widget in container.winfo_children():
                            my_widget = widget.cget("text")
                            my_widget_name = my_widget.split()[0]
                            if my_widget_name == str(sacrifice_card)[-8:]:
                                print("AAAAA entrou")
                                is_deleted = True
                                widget.config(text=f"Item {col + 1}")

                                self._table.get_position_in_field(col).set_occupied(False)
                                self._table.get_position_in_field(col).set_card(None)
                                self._table.get_local_field().remove_card_from_field(sacrifice_card)
                                container.config(bg="SystemButtonFace")
                                continue

            self._table.get_local_field().clear_sacrifice_cards()


    def get_card_by_id(self, id):   
        return self.library.get_card(id)

    ######### Logic for the dog #########

    def start_match(self): 
        start_status = self.dog_server_interface.start_match(2)

        code = start_status.get_code()
        message = start_status.get_message()
        if code == "0" or code == "1":
            messagebox.showinfo(message=message)
        elif code == "2":
            players = start_status.get_players()
            self._players = players
            self._table.start_match(players)
            game_page = self.get_frame("GamePage")
            game_page.reset_page()
            self.show_frame("GamePage")
            

    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        if message == "Partida iniciada":
            players = start_status.get_players()
            self._players = players
            self._table.start_match(players)
            game_page = self.get_frame("GamePage")
            game_page.reset_page()
            self.show_frame("GamePage")

    def receive_withdrawal_notification(self):
        self.dog_server_interface.proxy.get_status()
        messagebox.showinfo(message="O oponente desistiu da partida")
        self.show_frame("StartPage")

    def make_withdrawal(self):
        self.dog_server_interface.make_withdrawal()
        self.show_frame("StartPage")

    def receive_move(self, move):
        self._table._local_player.pass_turn()
        self._table._remote_player.pass_turn()

        # Atualiza a interface gráfica
        self.update_gui(move)
        print("EXECUTEI RECEIVE_MOVE")