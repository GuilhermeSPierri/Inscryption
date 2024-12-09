from problem_domain.position import Position

class Field:
    def __init__(self):
        self._positions = []
        self._sacrifice_cards = []
        for _ in range(4):
            position = Position()
            position.set_field(True)
            self._positions.append(position)

    def get_position_in_field(self, position_in_field: int) -> Position:
        return self._positions[position_in_field]

    def append_to_sacrifice_cards(self, selected_card):
        self._sacrifice_cards.append(selected_card)

    def clear_sacrifice_cards(self):
        self._sacrifice_cards.clear()

    def remove_from_sacrifice_cards(self, selected_card):
        if selected_card in self._sacrifice_cards:
            self._sacrifice_cards.remove(selected_card)

    def get_sacrifice_cards(self):
        return self._sacrifice_cards

    def remove_card_from_field(self, card):
        for position in self._positions:
            if position.get_card() == card:
                position.set_card(None)
                return
        raise ValueError("Card not found in field")

    def invoke_card_in_position(self, card, selected_position):
        if selected_position in self._positions:
            selected_position.set_card(card)
            print("Card ", card,  " invoked in position ", selected_position)
        else:
            raise ValueError("Invalid position")

    def get_card_in_position(self, position):
        if position in self._positions:
            return position.get_card()