from enum import Enum

class MacoPieceType(Enum):
    """Enum that describes the different types of pieces in Maco."""
    REGULAR = 1
    """A regular piece used for creating lines."""
    EXPLODE = 2
    """A special piece that removes adjacent pieces."""
    BLOCK = 3
    """A special piece that blocks a line for the opponent for one turn."""
