from problem_domain.cards.card import Card

class BoneCard(Card):
    
    def __init__(self, name: str, life: int, damage: int, glyph: None, cost: int, image: str):
        super().__init__("Bone", name, life, damage, glyph, cost, image)
        