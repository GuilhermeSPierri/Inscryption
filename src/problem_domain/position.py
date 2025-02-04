from problem_domain.cards.sacrificeCard import SacrificeCard
from problem_domain.cards.squirrelCard import SquirrelCard


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
    
    def get_hand(self):
        return self._hand
    
    def get_field(self):
        return self._field
    
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
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Reconstrói uma instância de Position a partir de um dicionário.
        Caso haja uma carta associada, utiliza SacrificeCard.from_dict para recriá-la.
        """
        position = cls()
        position._occupied = data["occupied"]
        position._hand = data["hand"]
        position._field = data["field"]
        
        # Reconstruindo a carta, se presente
        if data["card"] is not None:
            position._card = SacrificeCard.from_dict(data["card"])

        
        return position