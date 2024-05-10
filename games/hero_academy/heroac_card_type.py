from enum import Enum

class HeroAcademyCardType(Enum):
    """UnitType enum represents the type of the card."""
    UNIT = 1
    """Unit card able to fight."""
    SPELL = 2
    """Card able to cast a spell."""
    ITEM = 3
    """Card able to use an item."""