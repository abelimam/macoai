from enum import Enum
from games.hero_academy.heroac_card_type import HeroAcademyCardType

class HeroAcademyCardValue(Enum):
    """`CardValue` enum represents the value of the card."""
    KNIGHT =  1
    ARCHER =  2
    CLERIC =  3
    WIZARD =  4
    NINJA = 5
    INFERNO = 6  
    HEAL_POTION = 7 
    RUNEMETAL =  8
    SCROLL =  9
    DRAGONSCALE = 10
    SHINING_HELM = 11
    CRYSTAL = 12

    def is_unit_value(self) -> bool:
        """Return True if the card value is a unit value."""
        return self.value < 6

    def is_spell_value(self) -> bool:
        """Return True if the card value is a spell value."""
        return self.value == 6

    def is_item_value(self) -> bool:
        """Return True if the card value is an item value."""
        return self.value > 6 and self.value < 12

    def is_crystal_value(self) -> bool:
        """Return True if the card value is a crystal value."""
        return self.value == 12

    def get_card_type(self) -> 'HeroAcademyCardType':
        """Return the card type of the card value."""
        if self.is_unit_value():
            return HeroAcademyCardType.UNIT
        if self.is_spell_value():
            return HeroAcademyCardType.SPELL
        if self.is_item_value():
            return HeroAcademyCardType.ITEM