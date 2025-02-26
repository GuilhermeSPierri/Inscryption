from problem_domain.cards.card import Card
from problem_domain.cards.squirrelCard import SquirrelCard
from problem_domain.cards.sacrificeCard import SacrificeCard

class Deck:
    def __init__(self):
        # Atributos privados
        self._card_list = []  # Lista de objetos do tipo Carta

    # Métodos
    def get_default_deck(self) -> 'Deck':
        """Retorna um deck padrão."""
        default_cards = []  
        self._card_list = default_cards
        return self

    def get_top_card(self) -> 'Card':
        """Retorna a carta do topo do deck, removendo-a."""
        if self._card_list:
            return self._card_list.pop(0)
        return None  # Retorna None se o deck estiver vazio

    def get_deck_size(self) -> int:
        """Retorna o tamanho do deck."""
        return len(self._card_list)

    def get_card_list(self) -> list:
        """Retorna a lista de cartas no deck."""
        return self._card_list
    
    def set_card_list(self, card_list: list) -> None:
        """Define a lista de cartas do deck."""
        self._card_list = card_list

    def add_card_to_deck(self, card: 'Card') -> None:
        """Adiciona uma carta ao deck."""
        self._card_list.append(card)

    def generate_deck(self) -> 'Deck':
        """Gera um deck com base em uma lista de cartas."""
        list_of_cards = []
        for _ in range(20):
            list_of_cards.append(SacrificeCard("Wolf", 3, 2, {"name": "Amplifier", "modifier": "life", "value": 1}, 1, "assets/Wolf.png"))
        self._card_list = list_of_cards
        return self

    def reset_deck(self) -> None:
        self._card_list = []
