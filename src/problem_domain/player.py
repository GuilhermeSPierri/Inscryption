from problem_domain.deck import Deck

class Player:
    def __init__(self):
        # Atributos privados
        self._bone = 0  # int
        self._hand = None  # Hand (assume que Hand é uma classe)
        self._my_turn = False  # boolean
        self._identifier = ""  # string
        self._symbol = 0  # int
        self._my_deck = Deck()  # Deck
        self._my_deck.generate_deck()
        self._name = ""  # string

    # Métodos
    def reset(self) -> None:
        """Reseta o jogador para o estado inicial."""
        self._bone = 0
        self._hand = None
        self._my_turn = False
        self._identifier = ""
        self._symbol = 0
        self._my_deck = None
        self._name = ""

    def initialize(self, symbol: int, identifier: str, name: str) -> None:
        """Inicializa o jogador com os valores fornecidos."""
        self._symbol = symbol
        self._identifier = identifier
        self._name = name

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
        """Adiciona uma carta à mão do jogador."""
        if self._hand is not None:
            self._hand.add(card)

    def add_buy_token(self, amount: int) -> None:
        """Adiciona fichas de compra ao jogador."""
        self._bone += amount
