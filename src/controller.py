import tkinter as tk
from functools import partial
from tkinter import messagebox
from tkinter import simpledialog
from frames.startPage import StartPage  
from frames.gamePage import GamePage  
from frames.deckPage import DeckPage
from fonts.font import SMALL_FONT
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from problem_domain.library import Library
from problem_domain.table import Table
from problem_domain.position import Position
from problem_domain.cards.sacrificeCard import SacrificeCard
from problem_domain.cards.boneCard import BoneCard
from tkinter import PhotoImage, Label
from PIL import Image, ImageTk

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

    def _update_canvas_image(self, canvas, image_path, preserve_elements=False):
        """Atualiza um Canvas com uma imagem redimensionável preservando elementos se necessário"""
        try:
            if not preserve_elements:
                canvas.delete("all")
            else:
                # Mantém apenas elementos específicos
                canvas.delete("card_image")
                canvas.delete("text")

            current_width = canvas.winfo_width()
            current_height = canvas.winfo_height()
            image = Image.open(image_path)
            image = image.resize((current_width, current_height), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(image)
            
            canvas.image_ref = tk_image
            canvas.create_image(0, 0, anchor="nw", image=tk_image, tags="card_image")

            # Reaplica elementos visuais após redimensionamento
            if hasattr(canvas, 'saved_tags'):
                for tag in canvas.saved_tags:
                    if tag == "border":
                        canvas.create_rectangle(
                            2, 2, 
                            current_width-2, current_height-2,
                            outline="red" if "sacrifice" in tag else "yellow", 
                            width=3, 
                            tags="border"
                        )
                    elif tag == "sacrifice_text":
                        canvas.create_text(
                            current_width/2, current_height-20,
                            text="SACRIFÍCIO",
                            fill="red",
                            font=("Arial", 10, "bold"),
                            tags="sacrifice_text"
                        )

            canvas.event_generate("<Configure>")
        except Exception as e:
            print(f"Erro ao atualizar imagem: {e}")

        # Mantém registro dos elementos ativos
        canvas.saved_tags = []
        if "border" in canvas.gettags("all"):
            canvas.saved_tags.append("border")
        if "sacrifice_text" in canvas.gettags("all"):
            canvas.saved_tags.append("sacrifice_text")

        # Configura redimensionamento
        def resize(event):
            if event.width > 0 and event.height > 0:
                self._update_canvas_image(canvas, image_path, preserve_elements=True)

        canvas.bind("<Configure>", resize)
        canvas.event_generate("<Configure>")

    def create_container_grid(self, parent, text, padx, pady, row, col, textLabel):
        # Cria um Canvas como container
        container = tk.Canvas(
            parent,
            width=140,          # Largura mínima inicial
            height=190,         # Altura mínima inicial
            bg="white",
            highlightthickness=0,  # Remove borda do Canvas
            borderwidth=0           # Remove borda interna
        )
        container.grid(row=row, column=col, padx=padx, pady=pady, sticky="nsew")
        
        # Adiciona texto se necessário
        if textLabel:
            container.create_text(
                10, 
                10, 
                text=textLabel, 
                anchor="nw", 
                font=SMALL_FONT,  # Garanta que SMALL_FONT está importada
                tags="text"
            )
        
        return container
    
    def _update_field_section(self, game_page, field, positions, is_local):
        """Atualiza uma seção específica do campo (local ou remoto)"""
        for col in range(4):
            position_data = positions[col]
            posicao = Position.from_dict(position_data)
            field.set_position(col, posicao)

            # Determina a linha correta (0 para local, 2 para remoto)
            row = 0 if is_local else 2
            container = game_page.cards_field_containers[row][col]

            # Limpa o Canvas completamente
            container.delete("all")

            if position_data["occupied"]:
                card = SacrificeCard.from_dict(position_data["card"])
                # Atualiza a imagem
                self._update_canvas_image(container, card.get_image_path())

                # Obtém a largura e altura do card_container (Canvas)
                canvas_width = container.winfo_width()
                canvas_height = container.winfo_height()

                # Define posições relativas à largura e altura do canvas
                container.create_text(
                    canvas_width * 0.76, canvas_height * 0.67,  # Ajusta proporcionalmente
                    text=f"{card.get_hp()}",
                    anchor="nw",
                    font=("Arial", int(canvas_height * 0.05), "bold"),  # Fonte proporcional
                    tags="text"
                )

                container.create_text(
                    canvas_width * 0.205, canvas_height * 0.82,
                    text=f"{card.get_damage()}",
                    anchor="nw",
                    font=("Arial", int(canvas_height * 0.05), "bold"),
                    tags="text"
                )
            else:
                # Reseta para imagem vazia
                self._update_canvas_image(container, "assets/card.png")
    ######### Logic for the game page #########
    
    def create_hand_UI(self, page, container):
        if self._players:
            hand_dict = (
                self.get_local_hand() 
                if self._players[0][1] == self._table._local_player.get_id() 
                else self.get_remote_hand()
            )

            for row in range(3):
                for col in range(3):
                    index = row * 3 + col
                    
                    # Cria o Canvas para a carta
                    canvas_card = self.create_container_grid(
                        container, 
                        f"Container {row} {col}",
                        10, 10, row, col, ""
                    )
                    
                    # Força a atualização do layout para obter as dimensões corretas
                    canvas_card.update_idletasks()
                    
                    # Define o caminho da imagem
                    image_path = (
                        hand_dict[index].get_image_path() 
                        if index in hand_dict 
                        else "assets/card.png"
                    )
                    
                    # Atualiza o Canvas com a imagem
                    self._update_canvas_image(canvas_card, image_path)
                    
                    # Adiciona texto (se houver carta)
                    if index in hand_dict:
                        card = hand_dict[index]
                        canvas_card.create_text(
                            10, 10,
                            text=f"{card.get_name()}\nDamage: {card.get_damage()}",
                            anchor="nw",
                            font=SMALL_FONT,
                            tags="text"
                        )
                    
                    # Vincula o clique
                    canvas_card.bind(
                        "<Button-1>", 
                        lambda e, page=page, pos_in_hand=index: 
                            self.select_position(page, None, pos_in_hand, e)
                    )
                    
                    # Armazena referência
                    if len(page.cards_hand_containers) <= row:
                        page.cards_hand_containers.append([])
                    page.cards_hand_containers[row].append(canvas_card)

    def create_field_UI(self, page, container):
        for row in range(3):
            if row == 1:  # Ignora linha do meio
                page.cards_field_containers.append([])
                continue

            for col in range(4):
                canvas_card = self.create_container_grid(
                    container, 
                    f"Container {row} {col}",
                    10, 10, row, col, ""
                )
                
                # Força a atualização do layout
                canvas_card.update_idletasks()
                
                # Inicializa com imagem vazia
                self._update_canvas_image(canvas_card, "assets/card.png")
                
                # Vincula o clique
                canvas_card.bind(
                    "<Button-1>", 
                    lambda e, page=page, pos_in_field=col, r=row: 
                        self.select_position(page, pos_in_field, None, r, e)
                )
                
                # Armazena referência
                if len(page.cards_field_containers) <= row:
                    page.cards_field_containers.append([])
                page.cards_field_containers[row].append(canvas_card)
        
    def select_card(self, page, selected_position, position_in_hand, row=None):
        selected_card = self._table.select_card(selected_position)

        if not hasattr(page, 'selected_cards'):
            page.selected_cards = []

        if selected_position.get_origin() == "hand":
            # Desseleciona carta anterior na mão
            col = position_in_hand % 3
            row_hand = position_in_hand // 3

            # Clique na mesma carta
            if (row_hand, col) == getattr(page, 'selected_card', None):
                canvas = page.cards_hand_containers[row_hand][col]
                canvas.delete("border")
                canvas.config(bg="SystemButtonFace")
                page.selected_card = None
                return

            # Remove destaque anterior
            if page.selected_card:
                prev_row, prev_col = page.selected_card
                prev_canvas = page.cards_hand_containers[prev_row][prev_col]
                prev_canvas.delete("border")
                prev_canvas.config(bg="SystemButtonFace")

            # Adiciona novo destaque
            if selected_card is not None:
                canvas = page.cards_hand_containers[row_hand][col]
                canvas.delete("border")
                canvas.create_rectangle(
                    2, 2, 
                    canvas.winfo_width()-2, canvas.winfo_height()-2,
                    outline="yellow", width=3, tags="border"
                )
                canvas.config(bg="lightgray")
                page.selected_card = (row_hand, col)
            else:
                page.selected_card = None

        elif selected_position.get_origin() == "field":
            field = self._table.get_player_field()
            col = position_in_hand % 4

            # Desseleciona se clicar novamente
            if (row, col) in page.selected_cards:
                canvas = page.cards_field_containers[row][col]
                canvas.delete("border")
                canvas.delete("sacrifice_text")
                page.selected_cards.remove((row, col))
                field.remove_from_sacrifice_cards(selected_card)
                return

            # Adiciona novo sacrifício
            if selected_card is not None and selected_card.get_name() != "Empty":
                canvas = page.cards_field_containers[row][col]
                canvas.delete("border")
                canvas.delete("sacrifice_text")
                
                # Borda vermelha
                canvas.create_rectangle(
                    2, 2, 
                    canvas.winfo_width()-2, canvas.winfo_height()-2,
                    outline="red", width=3, tags="border"
                )
                
                # Texto de sacrifício
                canvas.create_text(
                    canvas.winfo_width()/2, canvas.winfo_height()-20,
                    text="SACRIFÍCIO", 
                    fill="red", 
                    font=("Arial", 10, "bold"),
                    tags="sacrifice_text"
                )
                
                page.selected_cards.append((row, col))
                field.append_to_sacrifice_cards(selected_card)
            else:
                page.selected_cards = []

    def select_position(self, page, position_in_field=None, position_in_hand=None, row=None,event=None):
        turn_player = self._table.get_turn_player()

        if turn_player.get_id() == self._table.get_local_player().get_id():
            if position_in_field is not None:
                if self._table._local_player.get_id() < self._table._remote_player.get_id():
                    if row == 0:
                        selected_position = self._table.get_local_field().get_position_in_field(position_in_field)
                    else:
                        messagebox.showinfo("Field incorreto", "Este não é o seu campo!")
                        return
                else:
                    if row == 2:
                        selected_position = self._table.get_remote_field().get_position_in_field(position_in_field)
                    else:
                        messagebox.showinfo("Field incorreto", "Este não é o seu campo!")
                        return
                selected_position.set_field(True)

            if position_in_hand is not None:
                selected_position = self._table.get_position_in_hand(position_in_hand)
                selected_position.set_hand(True)

            if turn_player.get_id() == self._table._local_player.get_id() and selected_position is not None:
                occupied = self._table.check_position(selected_position)

                if occupied:
                    if position_in_field is not None:
                        self.select_card(page, selected_position, position_in_field, row)
                    elif position_in_hand is not None:
                        self.select_card(page, selected_position, position_in_hand)

                if not occupied and selected_position._field:
                    self.invoke_card(selected_position, position_in_field, turn_player, row)

    ################### Logic for the deck page ###################

    def create_deck_page_UI(self, page):
        # Construir dicionários com ID baseado no objeto
        all_cards = list(self.get_all_cards().values())  # Lista de objetos Card
        
        all_cards_dict = {
            idx: {
                "id": str(card)[-8:],  # ID como string dos últimos 8 caracteres
                "name": card.get_name(),
                "damage": card.get_damage(),
                "life": card.get_hp(),
                "image": card.get_image_path()
            } for idx, card in enumerate(all_cards)
        }

        deck_cards = list(self.get_deck_info().values())  # Lista de objetos Card no deck
        deck_info_dict = {
            idx: {
                "id": str(card)[-8:],  # ID como string dos últimos 8 caracteres
                "name": card.get_name(),
                "damage": card.get_damage(),
                "life": card.get_hp(),
                "image": card.get_image_path()
            } for idx, card in enumerate(deck_cards)
        }

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
                card_container = self.create_container_grid(container, "", 10, 10, row, col, "")

                if index in card_data_dict:
                    card_data = card_data_dict[index]
                    self._update_canvas_image(card_container, card_data["image"])
                    # Obtém a largura e altura do card_container (Canvas)
                    canvas_width = card_container.winfo_width()
                    canvas_height = card_container.winfo_height()

                    print(canvas_height, canvas_width)
                        
                    # Define posições relativas à largura e altura do canvas
                    card_container.create_text(
                        canvas_width * 0.76, canvas_height * 0.67,  # Ajusta proporcionalmente
                        text=f"{card_data['life']}",
                        anchor="nw",
                        font=("Arial", int(canvas_height * 0.05), "bold"),  # Fonte proporcional
                        tags="text"
                    )

                    card_container.create_text(
                        canvas_width * 0.205, canvas_height * 0.82,
                        text=f"{card_data['damage']}",
                        anchor="nw",
                        font=("Arial", int(canvas_height * 0.05), "bold"),
                        tags="text"
                    )

                else:
                    self._update_canvas_image(card_container, "assets/card.png")


                card_container.bind("<Button-1>", lambda e, idx=index: on_click(card_data_dict.get(idx, {}), idx))
                
                if len(container_list) <= row:
                    container_list.append([])
                container_list[row].append(card_container)

   
    def add_card_to_deck_UI(self, card_data, index, page):
        # Procura por slots marcados como "Empty" nos dados
        for slot_index in range(20):
            if page.get_my_deck_data().get(slot_index, {}).get("name") == "Empty":
                row = slot_index // 4
                col = slot_index % 4
                
                # Atualiza dados
                page.get_my_deck_data()[slot_index] = card_data
                
                # Atualiza UI
                container = page.my_deck_containers[row][col]
                container.delete("all")
                self._update_canvas_image(container, card_data["image"])
                
                # Obtém a largura e altura do card_container (Canvas)
                canvas_width = container.winfo_width()
                canvas_height = container.winfo_height()

                # Define posições relativas à largura e altura do canvas
                container.create_text(
                    canvas_width * 0.76, canvas_height * 0.67,  # Ajusta proporcionalmente
                    text=f"{card_data['life']}",
                    anchor="nw",
                    font=("Arial", int(canvas_height * 0.05), "bold"),  # Fonte proporcional
                    tags="text"
                )

                container.create_text(
                    canvas_width * 0.205, canvas_height * 0.82,
                    text=f"{card_data['damage']}",
                    anchor="nw",
                    font=("Arial", int(canvas_height * 0.05), "bold"),
                    tags="text"
                )
                return
                
        messagebox.showinfo("Deck cheio", "Seu deck já possui o tamanho máximo")


    def remove_card_from_deck_UI(self, card_index, page):
        row = card_index // 4
        col = card_index % 4
        
        try:
            # Mantém a estrutura de 20 slots, marcando como vazio
            page.get_my_deck_data()[card_index] = {"name": "Empty"}
            
            # Atualiza o container
            container = page.my_deck_containers[row][col]
            container.delete("all")
            container.create_text(
                10, 10,
                text="Empty",
                anchor="nw",
                font=SMALL_FONT,
                tags="text"
            )
            self._update_canvas_image(container, "assets/card.png")
            
        except Exception as e:
            print(f"Erro ao remover carta: {str(e)}")

    def save_deck(self, deck_data_func):
        deck_data = deck_data_func()
        
        # Conta apenas cartas válidas (não "Empty")
        valid_cards = [card for card in deck_data.values() if card.get("name") != "Empty"]
        
        if len(valid_cards) == 20:
            self._table._local_deck.reset_deck()
            for card_dict in valid_cards:  # Ignora "Empty"
                card_object = self.library.get_card(card_dict["name"])
                self._table._local_deck.add_card_to_deck(card_object)
            messagebox.showinfo("Deck salvo", "Deck salvo com sucesso")
            self.show_frame("StartPage")
        else:
            messagebox.showerror("Erro", f"Deck precisa ter 20 cartas (atual: {len(valid_cards)})")

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

    def leave_game(self):
        quit()

    ######### Logic for the game page #########

    def buy_deck_card(self):
        # Get the top card from the deck
        turn_player = self._table.get_turn_player()
        if turn_player.get_id() == self._table._local_player.get_id():
            self._table.buy_deck_card()
            # Update the UI
            game_page = self.get_frame("GamePage")
            if game_page and self._table._buy_tokens == 0:
                self.update_hand_UI(game_page)
                messagebox.showinfo("Inscryption", "Você comprou uma carta do deck")
        else:
            messagebox.showinfo("Inscryption", "Não é o seu turno!")

    def update_hand_UI(self, game_page):
        hand_dict = {idx: card for idx, card in self.get_local_hand().items()}
        
        for row in range(3):
            for col in range(3):
                index = row * 3 + col
                canvas_card = game_page.cards_hand_containers[row][col]
                
                # Define o caminho da imagem
                if index in hand_dict:
                    card = hand_dict[index]
                    image_path = card.get_image_path()
                else:
                    image_path = "assets/card.png"
                
                # Atualiza o Canvas
                self._update_canvas_image(canvas_card, image_path)
                
                # Remove texto antigo e adiciona novo
                canvas_card.delete("text")
                if index in hand_dict:
                    # Obtém a largura e altura do card_container (Canvas)
                    canvas_width = canvas_card.winfo_width()
                    canvas_height = canvas_card.winfo_height()

                    # Define posições relativas à largura e altura do canvas
                    canvas_card.create_text(
                        canvas_width * 0.76, canvas_height * 0.67,  # Ajusta proporcionalmente
                        text=f"{card.get_hp()}",
                        anchor="nw",
                        font=("Arial", int(canvas_height * 0.05), "bold"),  # Fonte proporcional
                        tags="text"
                    )

                    canvas_card.create_text(
                        canvas_width * 0.205, canvas_height * 0.82,
                        text=f"{card.get_damage()}",
                        anchor="nw",
                        font=("Arial", int(canvas_height * 0.05), "bold"),
                        tags="text"
                    )

    def update_scale_UI(self, local_points, remote_points, game_page):
        game_page.scale_label.config(text=f"Your scale: {local_points} | Enemy scale: {remote_points}")
        
    def update_bones_UI(self, game_page, bones):
        game_page.bones_label.config(text=f"Bones: {bones}")

    def buy_squirrel_card(self):
        turn_player = self._table.get_turn_player()
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
            messagebox.showinfo("Inscryption", "Não é o seu turno!")


    def update_gui(self, move):
        # Atualiza a interface com base na jogada
        game_page = self.get_frame("GamePage")
        if game_page:
            # Atualiza o campo de batalha
            self.update_field_UI(game_page, move)

            # Atualiza a balança
            local_points = self._table._scale._local_player_points
            remote_points = self._table._scale._remote_player_points

            self.update_scale_UI(local_points, remote_points, game_page)


    def update_field_UI(self, game_page, move):
        # Atualiza o campo de batalha com base na jogada
        local_positions = move.get("local_positions", [])
        remote_positions = move.get("remote_positions", [])

        # Atualiza ambos os campos (local e remoto)
        self._update_field_section(game_page, self._table.get_local_field(), local_positions, is_local=True)
        self._update_field_section(game_page, self._table.get_remote_field(), remote_positions, is_local=False)


    def pass_turn(self, withdrawal=None):
        turn_player = self._table.get_turn_player()
        if (turn_player.get_id() == self._table._local_player.get_id() or withdrawal):
            if (self._table._buy_tokens == 1 and withdrawal==None):
                messagebox.showinfo("Inscryption", "Você deve comprar uma carta para passar turno!")
            else:   
                winner = self._table.pass_turn()

                # Criar um dicionário com a jogada atual
                local_positions = self._table.get_local_field().get_positions()
                remote_positions = self._table.get_remote_field().get_positions()

                move = {
                    "card": [card.to_dict() for card in self._table.get_local_field().get_sacrifice_cards()],  # Convert cards to dict
                    "local_positions": [position.to_dict() for position in local_positions],  # Convert local positions to dict
                    "remote_positions": [position.to_dict() for position in remote_positions], # Convert remote positions to dict
                    "action": "invoke_card", 
                    "match_status": self._table.get_match_status(),  # Adicionando o status da partida
                    "turn_player_id" : self._table.get_turn_player().get_id(),
                    "local_scale" : self._table._scale._local_player_points,
                    "remote_scale" : self._table._scale._remote_player_points,
                    "game_status" : "" # just for control the game logic
                }

                if winner != "":
                    if winner == "remote_player":
                        messagebox.showinfo("Jogo finalizado", "Você venceu")

                    elif winner == "local_player":
                        messagebox.showinfo("Jogo finalizado", "Você foi derrotado")
                    
                    self._table.set_match_status(2) # 2 = partida desconectada~
                    move["match_status"] = "finished"
                    move["game_status"] = "finished"
                    self.show_frame("StartPage")    
                
                self.update_gui(move)

                if withdrawal:
                    return move
                else:
                    self.dog_server_interface.proxy.send_move(move)
                    return move
        
        
    ######### Logic for the player #########

    def invoke_card(self, selected_position, position_in_field, player, row=None):
        if self._table.get_buy_tokens() == 0:
            invoked_card = self._table.invoke_card(selected_position, player)
            field = self._table.get_player_field()
            game_page = self.get_frame("GamePage")

            if isinstance(invoked_card, BoneCard):
                self.update_bones_UI(game_page, player.get_bones())

            if invoked_card:
                col = position_in_field
                container = game_page.cards_field_containers[row][col]
                
                # Atualiza com a imagem da carta invocada
                self._update_canvas_image(container, invoked_card.get_image_path())
                
                # Obtém a largura e altura do card_container (Canvas)
                canvas_width = container.winfo_width()
                canvas_height = container.winfo_height()

                # Define posições relativas à largura e altura do canvas
                container.create_text(
                    canvas_width * 0.76, canvas_height * 0.67,  # Ajusta proporcionalmente
                    text=f"{invoked_card.get_hp()}",
                    anchor="nw",
                    font=("Arial", int(canvas_height * 0.05), "bold"),  # Fonte proporcional
                    tags="text"
                )

                container.create_text(
                    canvas_width * 0.205, canvas_height * 0.82,
                    text=f"{invoked_card.get_damage()}",
                    anchor="nw",
                    font=("Arial", int(canvas_height * 0.05), "bold"),
                    tags="text"
                )


                # Remove carta da mão
                if game_page.selected_card:
                    hand_row, hand_col = game_page.selected_card
                    hand_container = game_page.cards_hand_containers[hand_row][hand_col]
                    self._update_canvas_image(hand_container, "assets/card.png")
                    game_page.selected_card = None

                # Processa sacrifícios
                if isinstance(invoked_card, SacrificeCard):
                    for sacrifice_card in field.get_sacrifice_cards():
                        for r in range(3):
                            if r == 1:
                                continue
                            for c in range(4):
                                try:
                                    target_container = game_page.cards_field_containers[r][c]
                                    text_items = target_container.find_withtag("text")
                                    
                                    if text_items:
                                        # Extrai o ID da carta do texto (primeira linha)
                                        text_content = target_container.itemcget(text_items[0], "text")
                                        card_id = text_content.split("\n")[0].strip()  # Pega a primeira linha
                                        print("CARD ID: ", card_id, "SACRIFICE CARD: ", sacrifice_card)

                                        # Compara com o ID da carta sacrificada (últimos 8 caracteres)
                                        if card_id == str(sacrifice_card)[-8:]:
                                            # Reseta para imagem vazia
                                            self._update_canvas_image(target_container, "assets/card.png", preserve_elements=False)
                                            field.get_position_in_field(c).set_card(None)
                                            field.get_position_in_field(c).set_occupied(False)
                                            print("SO PRA CONFERIR")
                                            player.increment_bones()
                                            
                                except (IndexError, AttributeError, KeyError) as e:
                                    print(f"Erro ao processar sacrifício: {e}")
                                    continue

                    field.clear_sacrifice_cards()
                    self.update_bones_UI(game_page, player.get_bones())
        else:
            messagebox.showinfo("Inscryption", "Você deve comprar uma carta antes de invocar")


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
            self.reset_game()
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
            self.reset_game()
            self._table.start_match(players)
            game_page = self.get_frame("GamePage")
            game_page.reset_page()
            self.show_frame("GamePage")

    def receive_withdrawal_notification(self):
        self.dog_server_interface.proxy.get_status()
        messagebox.showinfo(message="Você abandonou a partida")
        self._table.set_match_status(4) # 4 = desistencia
        move = self.pass_turn(True)
        move["match_status"] = "finished" # from the Dog
        move["game_status"] = "abandoned" # just for control the game logic

        self.dog_server_interface.proxy.send_move(move)
        self.show_frame("StartPage")
        self.reset_game()

    def receive_move(self, move):
        self._table._scale.set_local_player_points(move["remote_scale"])
        self._table._scale.set_remote_player_points(move["local_scale"])

        self._table._local_player.pass_turn()
        self._table._remote_player.pass_turn()

        # Atualiza a interface gráfica
        self.update_gui(move)

        if move["match_status"] == "finished" and move["game_status"] == "abandoned":
            messagebox.showinfo("Jogo finalizado", "O jogador inimigo abandonou a partida")
            self.show_frame("StartPage")


        elif move["match_status"] == "finished":
            messagebox.showinfo("Jogo finalizado", "O jogador inimigo venceu a partida")
            self.show_frame("StartPage")

    def reset_game(self):
        self._table.reset()
        self._table.set_match_status(2)
        self._table._local_player.reset()
        self._table._remote_player.reset()