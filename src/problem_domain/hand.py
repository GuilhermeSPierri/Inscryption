class Hand:
    def __init__(self, card_list, positions, invocation_card):
        self._card_list = card_list
        self._positions = positions
        self._invocation_card = invocation_card

    def get_position_in_hand(position_in_hand: int):
        pass

    def get_invocation_card(self):
        pass

    def set_invocation_card(self, selected_card):
        self._invocation_card = selected_card

    def clear_invocation_card(self):
        pass

    def remove_from_hand(self, card):
        pass