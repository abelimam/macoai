from enum import Enum

class AsmacagCardType(Enum):
    """Enum that describes the different types of `Card`."""
    NUMBER = 1
    """A `Card` that contains a number."""
    MULT2 = 2
    """A `Card` that multiplies the resulting score of using the next `Action` by 2."""
    DIV2 = 3
    """A `Card` that divides the resulting score of using the next `Action` by 2."""