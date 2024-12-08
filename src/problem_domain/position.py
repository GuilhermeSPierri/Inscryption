class Position:
    def __init__(self):
        # Indicates if the position is occupied
        self._occupied = False
        # Holds the card in this position
        self._card = None
        # Indicates if the position belongs to the hand
        self._hand = False
        # Indicates if the position belongs to the field
        self._field = False

    def get_card(self):
        """
        Get the card in this position.

        :return: Card object or None if the position is empty.
        """
        return self._card
    
    def set_hand(self):
        self._hand = True

    def set_field(self):
        self._field = True