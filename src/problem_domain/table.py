from problem_domain.player import Player
from problem_domain.field import Field
from problem_domain.scale import Scale

class Table:
    def __init__(self):
        # Attributes
        self._local_player = Player()
        self._remote_player = Player()
        self._local_field = Field()
        self._remote_field = Field()
        self._match_status = 1  # int
        self._local_deck = self._local_player.get_deck()  # Deck object
        self._remote_deck = self._remote_player.get_deck()  # Deck object
        self._scale = Scale()
        self._squirrel_deck = None # TODO: Define the type of this attribute
        self._buy_tokens = 0  # int
        self._game_status = "waiting"  # string

    # Métodos existentes
    def get_match_status(self):
        return self._match_status

    def receive_move(self):
        pass

    def get_status(self):
        return {
            "local_player": self._local_player,
            "remote_player": self._remote_player,
            "match_status": self._match_status,
        }
    
    def get_turn_player(self):
        # Assuming the turn player logic
        return self._local_player if self.game_status == "local_turn" else self._remote_player

    def clear_table(self):
        pass

    def start_match(self, players: int, local_player_id: str):
        # Logic to initialize the match
        return players

    def get_number_cards_local_deck(self):
        return len(self._local_deck) if self._local_deck else 0

    def buy_squirrel_card(self):
        # Logic to buy a squirrel card
        pass

    def create_deck_buy_buttons(self):
        # Logic to create buttons for buying cards
        pass

    def create_deck_squirrel_button(self):
        pass

    def verify_card_cost(self, card: object) -> bool:
        # Logic to verify card cost
        return True

    def place_card(self, position: object, card: object) -> None:
        # Logic to place a card on the field
        pass

    def buy_deck_card(self):
        pass

    def get_local_hand(self) -> object:
        return self._local_player.get_hand()

    def check_deck_size(self):
        return len(self._local_deck) if self._local_deck else 0

    def decrement_buy_tokens(self):
        self._buy_tokens -= 1

    def get_buy_tokens(self):
        return self._buy_tokens
    
    def set_local_deck(self, deck: object) -> None:
        self._local_deck = deck

    def set_remote_deck(self, deck: object) -> None:
        self._remote_deck = deck

    def shuffle_deck(self, deck: object) -> object:
        # Logic to shuffle a deck
        return deck 

    def pass_turn(self):
        # Logic to pass the turn
        return "Turn passed"

    def check_for_winner(self):
        points_difference = self._scale.calcule_points_difference()
        
        if (points_difference <= -7):
            winner ="local"
        
        elif (points_difference >= 7):
            winner = "remote"

        else:
            winner = ""
        
        return winner
            


    # Novos métodos adicionados na ordem da imagem
    def select_position(self): 
        pass

    def verify_position(self, position): 
        pass

    def card_attack(self, card_id: int): 
        pass

    def card_attack_scale(self): 
        pass

    def position_contains_card(self, position): 
        pass

    def check_front_path(self, position): 
        pass

    def select_card(self, selected_position): 
        pass

    def check_position(self, selected_position): 
        pass

    def get_position_in_field(self, position_in_field: int): 
        pass

    def get_position_in_hand(self, position_in_hand: int): 
        pass

    def clear_selected_card(self): 
        pass

    def get_origin_of_card(self, selected_card): 
        pass

    def invoke_card(self, selected_position): 
        pass

    def clear_selected_position(self): 
        pass

    def get_field_in_field(self): 
        pass

    def get_remote_field(self): 
        pass

    def get_field_card(self, position): 
        pass

    def execute_attack(self, damage, hp): 
        pass

    def invoke_card_in_field(self, move): 
        pass

    def set_hp_card(self, card, hp): 
        pass

    def get_remote_field_card(self, position): 
        pass

    def get_remote_field_card_in_position(self, position): 
        pass

    def check_for_winner(self): 
        pass

    def update_local_field(self, a_move: dict): 
        pass

    def update_remote_field(self, a_move: dict): 
        pass

    def update_scale(self, a_move: dict): 
        pass

    def deal_damage(self, remote_card_hp: int, damage: int): 
        pass

    def activate_glyph(self, card): 
        pass
