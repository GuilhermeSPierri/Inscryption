from abc import ABC, abstractmethod

class Card(ABC):

    def __init__(self, type: str, name: str, life: int, damage: int, glyph: None, cost: None):
        self._type = type
        self._name = name
        self._life = life
        self._damage = damage
        self._glyph = glyph
        self._cost = cost

    @abstractmethod
    def attack(self, target):
        pass

    def get_name(self):
        return self._name
    
    def get_damage(self):
        return self._damage
    
    def get_life(self):
        return self._life
