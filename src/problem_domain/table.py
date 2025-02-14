from problem_domain.player import Player
from problem_domain.field import Field
from problem_domain.scale import Scale
from problem_domain.deck import Deck
from problem_domain.cards.sacrificeCard import SacrificeCard
from problem_domain.cards.squirrelCard import SquirrelCard
import random

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
        self._buy_tokens = 1  # int
        self._game_status = "waiting"  # string

    # Métodos existentes
    def get_match_status(self):
        if self._match_status == 4:
            return "interrupted"
        elif self._match_status == 2:
            return "finished"
        elif self._match_status == 1:
            return "next"
    
    def set_match_status(self, status: int):
        self._match_status = status

    def get_status(self):
        return {
            "local_player": self._local_player,
            "remote_player": self._remote_player,
            "match_status": self._match_status,
        }

    def get_turn_player(self):
        if self._remote_player.get_turn():
            return self._remote_player
        elif self._local_player.get_turn():
            return self._local_player

    def get_number_cards_local_deck(self):
        return len(self._local_deck) if self._local_deck else 0
    
    def get_local_hand(self) -> object:
        return self._local_player.get_hand()
    
    def get_local_player(self):
        return self._local_player

    def get_remote_player(self):
        return self._remote_player

    def get_remote_hand(self) -> object:
        return self._remote_player.get_hand()
    
    def get_local_deck(self) -> object:
        return self._local_deck

    def get_buy_tokens(self):
        return self._buy_tokens

    def get_position_in_hand(self, position_in_hand: int): 
        return self._local_player.get_hand().get_position_in_hand(position_in_hand)
    
    def get_origin_of_card(self, selected_card): 
        pass

    def get_local_field(self):
        return self._local_field

    def get_field_in_field(self): 
        pass

    def get_remote_field(self): 
        return self._remote_field

    def get_field_card(self, position): 
        pass

    def get_remote_field_card(self, position): 
        pass

    def get_remote_field_card_in_position(self, position): 
        self._remote_field.get_card_in_position(position)

    def get_field_card_in_position(self, position, field):
        return field.get_card_in_position(position)
    
    def get_damage(self, card):
        return card.get_damage()

    def get_hp(self, card):
        return card.get_hp()

    def set_local_deck(self, deck: object) -> None:
        self._local_deck = deck

    def set_remote_deck(self, deck: object) -> None:
        self._remote_deck = deck

    def set_life_card(self, card, life): 
        pass

    def receive_move(self):
        pass

    def clear_table(self):
        pass

    def start_match(self, players: str):
        # Logic to initialize the match
        self._local_player.reset()
        self._remote_player.reset()
        self._local_player.initialize(players[0][1])
        self._remote_player.initialize(players[1][1])
        self._local_deck = self._local_player.get_deck()
        self._remote_deck = self._remote_player.get_deck()
        self._squirrel_deck = SquirrelCard("Squirrel", 1, 0, None, 0)
        self._local_deck = self.shuffle_deck(self._local_deck)
        #self._remote_deck = self.shuffle_deck(self._remote_deck)
        self._local_player.initial_hand(self._local_deck)
        self._remote_player.initial_hand(self._remote_deck)
        if int(players[0][2]) == 1:
            self._local_player.pass_turn()
        else:
            self._remote_player.pass_turn()
        return players

    def buy_squirrel_card(self):
        if (self._buy_tokens == 1): 
            print("meus tokens")
            squirrel = self._squirrel_deck
            self._squirrel_deck = SquirrelCard("Squirrel", 1, 0, None, 0)
            self._local_player.get_hand().add_card_to_hand(squirrel)
            self.decrement_buy_tokens()
            return squirrel


    def create_deck_buy_buttons(self):
        # Logic to create buttons for buying cards
        pass

    def create_deck_squirrel_button(self):
        pass

    def place_card(self, position: object, card: object) -> None:
        # Logic to place a card on the field
        pass

    def buy_deck_card(self):
        if (self._buy_tokens == 1):
            top_card = self.get_local_deck().get_top_card()
            self.get_local_hand().add_card_to_hand(top_card)
            self.decrement_buy_tokens()
            return top_card

    def check_deck_size(self):
        return len(self._local_deck) if self._local_deck else 0

    def decrement_buy_tokens(self):
        self._buy_tokens = 1

    def shuffle_deck(self, deck: object) -> object:
        positions = []

        for i in range(20):
            positions.append(i)

        random.shuffle(positions)
        shuffled_deck = Deck()

        shuffled_deck_cards = []
        deck_cards = deck.get_card_list()
        for j in range(len(positions)):
            shuffled_deck_cards.insert(positions[j], deck_cards[j])

        shuffled_deck.set_card_list(shuffled_deck_cards)

        return shuffled_deck

    def check_for_winner(self):
        points_difference = self._scale.calcule_points_difference()
        
        if (points_difference <= -7):
            winner = "local_player"
        
        elif (points_difference >= 7):
            winner = "remote_player"

        else:
            winner = ""
            self._match_status = 3
        
        return winner

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
        turn_player = self.get_turn_player()
        selected_card = None
        if turn_player:
            selected_card = selected_position.get_card()
            print("A CARTA SELECIONADA É", selected_card)
            
            if selected_card == None:
                return
            else:
                already_selected = selected_card.get_already_selected()
                hand = turn_player.get_hand()
                invocation_card = hand.get_invocation_card()

                if turn_player:
                    field = self.get_player_field()

                if already_selected:
                    origin = selected_position.get_origin()

                    if origin == "field":
                        field.remove_from_sacrifice_cards(selected_card)
                        print("Sacrifice cardaaa", field.get_sacrifice_cards())
                        selected_card.clear_already_selected()
                        self.clear_selected_card()

                    elif origin == "hand":
                        hand.clear_invocation_card()
                        selected_card.clear_already_selected()
                else:
                    if selected_card in hand.get_card_list() and invocation_card == None:
                        hand.set_invocation_card(selected_card)
                        selected_card.set_already_selected()
                    
                    elif selected_card == field.get_card_in_position(selected_position):
                        #field.append_to_sacrifice_cards(selected_card)
                        selected_card.set_already_selected()
                        print("Sacrifice carda", field.get_sacrifice_cards())   
                    
                    else:
                        field.clear_sacrifice_cards()
                        hand.clear_invocation_card()

                return selected_card

    def check_position(self, selected_position): 
        return selected_position.get_occupied()
    
    def set_position(self, selected_position, boolean): 
        selected_position.set_occupied(boolean)

    def clear_selected_card(self): 
        pass

    def get_player_field(self):
        if self._local_player.get_id() < self._remote_player.get_id():
            field = self._local_field
        else:
            field = self._remote_field

        return field

    def invoke_card(self, selected_position, player, row=None): 
        hand = player.get_hand()
        field = self.get_player_field()

        invocation_card = hand.get_invocation_card()
        if invocation_card != None:
            cost_invocation = invocation_card.get_cost()
            sacrifice_cards = field.get_sacrifice_cards()

            if cost_invocation == len(sacrifice_cards):
                for card in sacrifice_cards:
                    field.remove_card_from_field(card)

                for card in hand.get_card_list():
                    if card == invocation_card:
                        hand.remove_from_hand(card)
                        break

                field.invoke_card_in_position(invocation_card, selected_position)
                hand.clear_invocation_card()
                self.clear_selected_position()
                return invocation_card

    def clear_selected_position(self): 
        pass

    def execute_attack(self, damage, life, remote_card): 
        remaing_hp, is_alive = self.deal_damage(life, damage)

        if is_alive:
            remote_card.set_hp(remaing_hp)

        else:
            field = self.get_player_field()

            if field == self._local_field:
                self._remote_field.remove_card_from_field(remote_card)
            else:
                self._local_field.remove_card_from_field(remote_card)
        

    def invoke_card_in_field(self, move): 
        pass

    def update_local_field(self, a_move: dict): 
        pass

    def update_remote_field(self, a_move: dict): 
        pass

    def update_scale(self, a_move: dict): 
        pass

    def deal_damage(self, remote_card_life: int, damage: int): 
        remaing_hp = remote_card_life - damage
        
        if remaing_hp <= 0:
            is_alive = False

        else:
            is_alive = True

        return remaing_hp, is_alive

    def activate_glyph(self, card): 
        glyph = card.get_glyph()

        if glyph != None:
            modifier = glyph["modifier"]
            value = glyph["value"]

            if modifier == "life":
                life = card.get_hp()
                life = life + value
                card.set_hp(life)

            elif modifier == "damage":
                damage = card.get_damage()
                damage = damage + value
                card.set_damage(damage)


    def update_local_deck(self, deck_data: dict):
        for _, card_name in deck_data.item():
            card_object = self.library.get_card(card_name)
            self._local_deck.add_card_to_deck(card_object)
        list_of_cards = []
        self._local_deck.set_card_list(list_of_cards)
        self._local_player.set_deck(self._local_deck)

    
    def pass_turn(self):
        for i in range(4):
            field = self.get_player_field()
            local_card = self.get_field_card_in_position(i, field)

            if local_card != None:
                if field == self._local_field:
                    field = self._remote_field
                else:
                    field = self._local_field

                remote_card = field.get_card_in_position(i)

                damage = self.get_damage(local_card)

                if remote_card != None:
                    remote_card_hp = remote_card.get_hp()
                    self.execute_attack(damage, remote_card_hp, remote_card)
                
                else:
                    if self._local_player.get_id() < self._remote_player.get_id():
                        player_field = "local"
                    else:
                        player_field = "remote"
                    self._scale.add_points(damage, player_field)
                    print("points local scale: ", self._scale._local_player_points, "points remote scale: ", self._scale._remote_player_points)

                self.activate_glyph(local_card) # Activates the glyph card after attack
    

        self._local_player.pass_turn()
        self._remote_player.pass_turn()
        self._local_player.add_buy_token(1)
        self._remote_player.add_buy_token(1)
        winner = self.check_for_winner()
        return winner