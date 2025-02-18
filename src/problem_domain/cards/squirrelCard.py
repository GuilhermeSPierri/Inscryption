from problem_domain.cards.card import Card

class SquirrelCard(Card):

    def __init__(self, name: str, life: int, damage: int, glyph: None, cost = None):
        super().__init__("Squirrel", name, life, damage, glyph, cost)
