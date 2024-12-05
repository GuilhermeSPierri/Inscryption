from problem_domain.cards.card import Card

class SacrificeCard(Card):

    def __init__(self, name: str, life: int, damage: int, glyph: None, cost: int):
        super().__init__("Sacrifice", name, life, damage, glyph, cost)

    def attack(self, target):
        pass