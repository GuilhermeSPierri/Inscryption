import copy
from problem_domain.cards.card import Card
from problem_domain.cards.boneCard import BoneCard
from problem_domain.cards.sacrificeCard import SacrificeCard
from problem_domain.cards.squirrelCard import SquirrelCard

class Library():

    def __init__(self):
        self._cards_model = dict()
        self._pointer_id = 0
        
        self.add_card(SacrificeCard("Bear", 5, 3, {"name": "Guardian", "modifier": "damage", "value": 1}, 2, "assets/Bear.png"))
        self.add_card(SquirrelCard("Squirrel", 1, 0, None, 0, "assets/Squirrel.png"))
        self.add_card(SacrificeCard("Wolf", 3, 2, {"name": "'Amplifier", "modifier": "life", "value": 1}, 1, "assets/Wolf.png"))
        self.add_card(BoneCard("Vulture", 1, 2, None, 1, "assets/Vulture.png"))


    def add_card(self, card: Card):
        try:
            self._cards_model[self._pointer_id] = card
            self._pointer_id += 1
        except Exception as e:
            print(f"Error: {e}")

    def remove_card(self, id: int):
        try:
            del self._cards_model[id]
            self._pointer_id -= 1
        except Exception as e:
            print(f"Error: {e}")

    def get_all_cards(self):
        try:
            return self._cards_model
        except Exception as e:
            print(f"Error: {e}")

    def show_cards(self):
        try:
            for key, value in self._cards_model.items():
                print(f"ID: {key} - {value.name}")
        except Exception as e:
            print(f"Error: {e}")

    def get_card(self, name: str):
        try:
            for key, value in self._cards_model.items():
                if value.get_name() == name:
                    new_card = copy.deepcopy(value)
                    return new_card
        except Exception as e:
            print(f"Error: {e}")
        
        

    