from enum import Enum

class TankWarUnitType(Enum):
    """UnitType enum represents the type of the unit."""
    TANK = 1
    """Tank unit able to fight."""
    RECYCLER = 2
    """Recycler unit able to collect trash."""
    TILE = 3
    """Tile unit able to build a recycler."""