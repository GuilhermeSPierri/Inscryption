from abc import ABC, abstractmethod

class Card(ABC):

    def __init__(self, type: str, name: str, life: int, damage: int, glyph: None, cost: None):
        self._damage = damage
        self._life = life
        self._cost = cost
        self._glyph = glyph
        self._name = name
        self._type = type

    @abstractmethod
    def attack(self, target):
        pass

    def get_damage(self):
        return self._damage
    
    def get_already_selected(self):
        pass

    def clear_already_selected(self):
        pass

    def get_cost(self):
        pass

    def get_life(self):
        return self._life
    
    def get_name(self):
        return self._name
    
    def set_hp(self, new_hp : int):
        self._hp = new_hp

    def get_glyph(self):
        return self._glyph

    def set_damage(self, damage: int):
        self._damage = damage
    
