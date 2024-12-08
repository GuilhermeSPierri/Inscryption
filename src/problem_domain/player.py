from problem_domain.deck import Deck
from problem_domain.hand import Hand

class Player:
    def __init__(self):
        # Atributos privados
        self._bone = 0  # int
        self._hand = Hand()
        self._my_turn = False  # boolean
        self._id = ""  # string
        self._symbol = 0  # int
        self._my_deck = Deck()  # Deck
        #self._my_deck.generate_deck()
        self._name = ""  # string

    # Métodos
    def reset(self) -> None:
        """Reseta o jogador para o estado inicial."""
        self._bone = 0
        self._hand = Hand()
        self._my_turn = False
        self._id = ""
        self._symbol = 0
        self._name = ""

    def initialize(self, id: str = "") -> None:
        """Inicializa o jogador com os valores fornecidos."""
        #self._symbol = symbol
        self._id = id
        #self._name = name

    def toggle_turn(self) -> None:
        """Alterna o turno do jogador."""
        self._my_turn = not self._my_turn

    def get_deck(self) -> object:
        """Retorna o deck do jogador."""
        return self._my_deck

    def get_deck_length(self) -> int:
        """Retorna o tamanho do deck do jogador."""
        return len(self._my_deck) if self._my_deck else 0

    def add_card_to_deck(self, card_to_add: int) -> None:
        """Adiciona uma carta ao deck do jogador."""
        if self._my_deck is not None:
            self._my_deck.append(card_to_add)

    def set_deck(self, deck: object) -> None:
        """Define o deck do jogador."""
        self._my_deck = deck

    def remove_card_from_deck(self, card_to_remove: int) -> None:
        """Remove uma carta do deck do jogador."""
        if self._my_deck is not None and card_to_remove in self._my_deck:
            self._my_deck.remove(card_to_remove)

    def get_turn(self) -> bool:
        """Retorna se é o turno do jogador."""
        return self._my_turn

    def add_card_to_hand(self, card: object) -> None:
        if self._hand is not None:
            self._hand.add_card_to_hand(card)

    def add_buy_token(self, amount: int) -> None:
        """Adiciona fichas de compra ao jogador."""
        self._bone += amount

    def get_hand(self) -> object:
        return self._hand
    
    def initial_hand(self, deck):
        for _ in range(3):
            self.add_card_to_hand(deck.get_top_card())

    def pass_turn(self):
        self._my_turn = not self._my_turn
