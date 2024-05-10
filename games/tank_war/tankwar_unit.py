from typing import List, Tuple
from copy import deepcopy
from games.tank_war.tankwar_unit_type import TankWarUnitType

class TankWarUnit:
    def __init__(self, unit_type: 'TankWarUnitType', pos: Tuple[int, int]) -> None:
        """Base class for all units that a player can use in the game."""
        self.unit_type = unit_type
        self.pos = pos

# region Methods
    def clone(self) -> 'TankWarUnit':
        """Create new unit with the same unit_type and pos."""
        return TankWarUnit(self.unit_type, deepcopy(self.pos))

    def copy_into(self, other: 'TankWarUnit') -> None:
        """Copies the unit contents into another one."""
        other.unit_type = self.unit_type
        other.pos = deepcopy(self.pos)
# endregion

# region Getters
    def get_unit_type(self) -> 'TankWarUnitType':
        """Get unit type."""
        return self.unit_type

    def get_pos(self) -> Tuple[int, int]:
        """Get unit position."""
        return self.pos
# endregion

# region Helpers
    def get_possible_moves(self, board_size: int, possible_moves: Tuple[int, int]) -> List[Tuple[int, int]]:
        moves = []
        for move in possible_moves:
            new_pos = (self.pos[0] + move[0], self.pos[1] + move[1])
            if 0 <= new_pos[0] < board_size and 0 <= new_pos[1] < board_size:
                moves.append(new_pos)
        return moves
# endregion

# region Overrides
    def __str__(self) -> str:
        return f"Unit[{self.unit_type.name}, {self.pos}]"
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, TankWarUnit):
            return False
        return self.unit_type == __o.unit_type and self.pos == __o.pos
    
    def __hash__(self) -> int:
        return int(str(self.unit_type.value) + str(self.pos[0]) + str(self.pos[1]))
# endregion