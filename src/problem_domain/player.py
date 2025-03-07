from problem_domain.deck import Deck
from problem_domain.hand import Hand

class Player:
    def __init__(self):
        # Atributos privados
        self._bones = 0  # int
        self._hand = Hand()
        self._my_turn = False  # boolean
        self._id = ""  # string
        self._symbol = 0  # int
        self._my_deck = Deck()  # Deck
        self._my_deck.generate_deck()
        self._name = ""  # string

    def set_name(self, name):
        self._name = name
        
    def get_bones(self):
        return self._bones

    def get_deck(self) -> object:
        """Retorna o deck do jogador."""
        return self._my_deck

    def get_deck_length(self) -> int:
        """Retorna o tamanho do deck do jogador."""
        return len(self._my_deck) if self._my_deck else 0

    def get_turn(self) -> bool:
        """Retorna se é o turno do jogador."""
        return self._my_turn
    
    def get_id(self) -> str:
        return self._id

    def get_hand(self) -> object:
        return self._hand

    def set_deck(self, deck: object) -> None:
        """Define o deck do jogador."""
        self._my_deck = deck

    # Métodos
    def reset(self) -> None:
        """Reseta o jogador para o estado inicial."""
        self._bones = 0  # int
        self._hand = Hand()
        self._my_turn = False  # boolean
        self._id = ""  # string
        self._symbol = 0  # int
        self._name = ""  # string

    def initialize(self, id: str = "") -> None:
        """Inicializa o jogador com os valores fornecidos."""
        self._id = id

    def add_card_to_hand(self, card: object) -> None:
        if self._hand is not None:
            self._hand.add_card_to_hand(card)
    
    def initial_hand(self, deck):
        for _ in range(3):
            self.add_card_to_hand(deck.get_top_card())

    def pass_turn(self):
        self._my_turn = not self._my_turn
    
    def increment_bones(self):
        self._bones += 1

    def decrement_bones(self, value):
        self._bones -= value