from problem_domain.cards.card import Card

class SquirrelCard(Card):

    def __init__(self, name: str, hp: int, damage: int, glyph: None, cost = None):
        super().__init__("Squirrel", name, hp, damage, glyph, cost)

    def attack(self, target):
        pass