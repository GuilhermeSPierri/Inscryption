from problem_domain.position import Position

class Field:
    def __init__(self):
        # Initialize an array of 4 Position objects
        self._positions = [Position() for _ in range(4)]
        # Initialize a list to hold sacrificed cards
        self._sacrifice_cards = []

    def get_position_in_field(self, position_in_field: int) -> Position:
        
        if 0 <= position_in_field < len(self._positions):
            return self._positions[position_in_field]
        raise IndexError("Position index out of range")

    def append_to_sacrifice_cards(self, selected_card):
        """
        Add a card to the sacrifice cards list.

        :param selected_card: Card object to be added.
        """
        self._sacrifice_cards.append(selected_card)

    def clear_sacrifice_cards(self):
        """
        Remove all cards from the sacrifice cards list.
        """
        self._sacrifice_cards.clear()

    def remove_from_sacrifice_cards(self, selected_card):
        """
        Remove a specific card from the sacrifice cards list.

        :param selected_card: Card object to be removed.
        """
        if selected_card in self._sacrifice_cards:
            self._sacrifice_cards.remove(selected_card)

    def get_sacrifice_cards(self):
        """
        Get a list of all sacrifice cards.

        :return: List of Card objects.
        """
        return self._sacrifice_cards

    def remove_card_from_field(self, card):
        """
        Remove a card from its position in the field.

        :param card: Card object to be removed.
        """
        for position in self._positions:
            if position.card == card:
                position.card = None
                return
        raise ValueError("Card not found in field")

    def invoke_card_in_position(self, card, selected_position):
        """
        Place a card in the specified position on the field.

        :param card: Card object to be placed.
        :param selected_position: Position object where the card will be placed.
        """
        if selected_position in self._positions:
            selected_position.card = card
        else:
            raise ValueError("Invalid position")

    def get_card_in_position(self, position):
        """
        Get the card in the specified position.

        :param position: Position object to check.
        :return: Card object or None if the position is empty.
        """
        if position in self._positions:
            return position.card
        raise ValueError("Invalid position")