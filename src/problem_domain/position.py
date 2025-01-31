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
        return self._card
    
    def set_card(self, card):
        self._card = card
        self._occupied = True
    
    def set_hand(self, boolean):
        self._hand = boolean

    def set_field(self, boolean):
        self._field = boolean

    def get_occupied(self):
        return self._occupied
    
    def set_occupied(self, boolean):
        self._occupied = boolean

    def get_origin(self):
        if self._hand:
            return "hand"
        elif self._field:
            return "field"
        
    def to_dict(self):
        return {
            "occupied": self._occupied,
            "card": self._card.to_dict() if self._card else None,  # Convert card to dict if it exists
            "hand": self._hand,
            "field": self._field
        }