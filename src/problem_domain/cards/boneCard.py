from problem_domain.cards.card import Card

class BoneCard(Card):
    
    def __init__(self, name: str, hp: int, damage: int, glyph: None, cost: int):
        super().__init__("Bone", name, hp, damage, glyph, cost)
        
    def attack(self, target):
        pass