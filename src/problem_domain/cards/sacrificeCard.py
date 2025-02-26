from problem_domain.cards.card import Card

class SacrificeCard(Card):

    def __init__(self, name: str, life: int, damage: int, glyph: None, cost: int, image: str):
        super().__init__("Sacrifice", name, life, damage, glyph, cost, image)

    @classmethod
    def from_dict(cls, data: dict):
        """
        Reconstrói um objeto SacrificeCard a partir de um dicionário.
        Note que usamos 'life' para o parâmetro 'hp' (conforme o to_dict da classe Card)
        """
        return cls(
            name=data["name"],
            life=data["hp"],
            damage=data["damage"],
            glyph=data["glyph"],
            cost=data["cost"],
            image=data["image"]
        )