from problem_domain.position import Position

class Hand:
    def __init__(self):
        self._card_list = []
        self._positions = []
        self._invocation_card = None
        for _ in range(9):
            position = Position()
            position.set_hand(True)
            self._positions.append(position)

    def get_position_in_hand(self, position_in_hand: int):
        return self._positions[position_in_hand]
    
    def add_card_to_hand(self, card):
        self._card_list.append(card)
        self._positions[len(self._card_list) - 1].set_card(card)

    def get_invocation_card(self):
        return self._invocation_card

    def set_invocation_card(self, selected_card):
        self._invocation_card = selected_card

    def clear_invocation_card(self):
        self._invocation_card = None

    def get_card_list(self):
        return self._card_list

    def set_card_list(self, card_list):
        self._card_list = card_list

    def remove_from_hand(self, card):
        if card in self._card_list:
            self._card_list.remove(card)
            for position in self._positions:
                if position.get_card() == card:
                    position.set_card(None)
                    position.set_occupied(False)
                    break
        else:
            raise ValueError("Card not found in hand")