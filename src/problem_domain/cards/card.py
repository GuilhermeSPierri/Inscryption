from abc import ABC, abstractmethod

class Card(ABC):

    def __init__(self, type: str, name: str, hp: int, damage: int, glyph: None, cost: None):
        self._damage = damage
        self._hp = hp
        self._cost = cost
        self._glyph = glyph
        self._name = name
        self._type = type
        self._already_selected = False

    @abstractmethod
    def attack(self, target):
        pass

    def get_damage(self):
        return self._damage
    
    def get_already_selected(self):
        return self._already_selected
    
    def set_already_selected(self):
        self._already_selected = True

    def clear_already_selected(self):
        self._already_selected = False

    def get_cost(self):
        return self._cost

    def get_hp(self):
        return self._hp
    
    def get_name(self):
        return self._name
    
    def set_hp(self, new_hp : int):
        self._hp = new_hp

    def get_glyph(self):
        return self._glyph

    def set_damage(self, damage: int):
        self._damage = damage
    
    def to_dict(self):
        return {
            "name": self._name,
            "damage": self._damage,
            "hp": self._hp,
            "glyph": self._glyph,
            "cost": self._cost
        }