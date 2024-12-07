from problem_domain.cards.card import Card

class BoneCard(Card):
    
    def __init__(self, name: str, life: int, damage: int, glyph: None, cost: int):
        super().__init__("Bone", name, life, damage, glyph, cost)
        
    def attack(self, target):
        pass