from games.hero_academy.heroac_card_type import HeroAcademyCardType
from games.hero_academy.heroac_card_value import HeroAcademyCardValue

class HeroAcademyCard:
    def __init__(self, value: 'HeroAcademyCardValue', card_type: 'HeroAcademyCardType'):
        """Card is a base class for all cards that a player can use in the game."""
        self.value = value
        self.card_type = card_type

# region Methods
    def clone(self) -> 'HeroAcademyCard':
        """Create new card with the same info."""
        return HeroAcademyCard(self.value, self.card_type)

    def copy_into(self, other: 'HeroAcademyCard') -> None:
        """Copies the card contents into another one."""
        other.value = self.value
        other.card_type = self.card_type
# endregion

# region Getters
    def get_value(self) -> 'HeroAcademyCardValue':
        """Get value."""
        return self.value
    
    def get_card_type(self) -> 'HeroAcademyCardType':
        """Get card type."""
        return self.card_type
# endregion

# region Override
    def __str__(self) -> str:
        return f"Card[{self.value.name}]"
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, HeroAcademyCard):
            return False
        return self.value.value == __o.value.value and self.card_type.value == __o.card_type.value
    
    def __hash__(self) -> int:
        return int(str(self.value.value) + str(self.card_type.value))
# endregion