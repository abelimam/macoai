from typing import Tuple
from copy import deepcopy
from games import Action
from games.tank_war.tankwar_unit import TankWarUnit

class TankWarAction(Action):
    def __init__(self, unit: 'TankWarUnit', pos: Tuple[int, int] = None):
        """Actions stand for every possible action that can be taken by a unit per turn."""
        self.unit = unit
        self.pos = pos

# region Methods
    def clone(self) -> 'TankWarAction':
        """Create new action with the same unit and pos."""
        return TankWarAction(self.unit.clone(), deepcopy(self.pos) if self.pos is not None else None)

    def copy_into(self, other: 'TankWarAction') -> None:
        """Deep copies the `Action` contents into another one."""
        self.unit.copy_into(other.unit)
        other.pos = deepcopy(self.pos) if self.pos is not None else None
# endregion

# region Getters
    def get_unit(self) -> 'TankWarUnit':
        """Return unit."""
        return self.unit

    def get_pos(self) -> Tuple[int, int]:
        """Return pos."""
        return self.pos
# endregion

# region Helpers
    def get_unit_movement(self) -> Tuple[int, int]:
        """Return unit movement."""
        if self.pos is None:
            return (0, 0)
        return (self.pos[0] - self.unit.get_pos()[0], self.pos[1] - self.unit.get_pos()[1])
# endregion

# region Override
    def __str__(self) -> str:
        """Return string representation of action."""
        return f"Action[{self.unit}, {self.pos if self.pos is not None else ''}]"
# endregion