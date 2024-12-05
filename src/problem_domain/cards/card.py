from abc import ABC, abstractmethod

class Card(ABC):

    def __init__(self, type: str, name: str, life: int, damage: int, glyph: None, cost: None):
        self.type = type
        self.name = name
        self.life = life
        self.damage = damage
        self.glyph = glyph
        self.cost = cost

    @abstractmethod
    def attack(self, target):
        pass
