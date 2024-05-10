from enum import Enum

class HeroAcademyTileType(Enum):
    """TileTipe enum represents the type of the square of the board."""
    EMPTY = 0
    """Empty tile."""
    ATTACK = 1
    """Attack tile."""
    SPEED = 2
    """Speed tile."""