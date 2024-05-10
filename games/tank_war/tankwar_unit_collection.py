from collections import defaultdict
from typing import List, Tuple
from copy import deepcopy
from games.tank_war.tankwar_unit_type import TankWarUnitType
from games.tank_war.tankwar_unit import TankWarUnit

class TankWarUnitCollection:
    def __init__(self) -> None:
        """A collection of units the player will use during the game."""
        self.units: List['TankWarUnit'] = []

# region Methods
    def clone(self) -> 'TankWarUnitCollection':
        """Create new collection with the same units."""
        new_units_collection = TankWarUnitCollection()
        for unit in self.units:
            new_units_collection.add_unit(TankWarUnit(unit.unit_type, deepcopy(unit.pos)))
        return new_units_collection

    def add_unit(self, unit: 'TankWarUnit'):
        """Add a unit to the collection."""
        self.units.append(unit)

    def add_units(self, units: List['TankWarUnit']):
        """Add a list of units to the collection."""
        self.units.extend(units)

    def remove_unit(self, unit: 'TankWarUnit'):
        """Remove a unit from the collection."""
        self.units.remove(unit)

    def remove_units_in_position(self, pos: Tuple[int, int], count: int):
        """Remove a number of units in a position."""
        for _ in range(abs(count)):
            self.units.remove(self.get_unit_in_pos(pos))

    def remove_tanks_in_position(self, pos: Tuple[int, int], count: int):
        """Remove a number of tanks in a position."""
        for _ in range(abs(count)):
            self.units.remove(self.get_tank_in_position(pos))

    def remove_all_units_in_position(self, pos: Tuple[int, int]):
        """Remove all units in a position."""
        for unit in self.units:
            if unit.pos == pos:
                self.units.remove(unit)

    def get_units(self) -> List['TankWarUnit']:
        """Get all units from the collection."""
        return self.units

    def move_unit(self, unit: 'TankWarUnit', pos: Tuple[int, int]):
        """Move a unit to a new position."""
        unit.pos = deepcopy(pos)
# endregion

# region Units    
    def get_tank_and_available_tiles_units(self) -> List['TankWarUnit']:
        """Get all tanks and tiles from the collection."""
        return [unit for unit in self.units if unit.get_unit_type() == TankWarUnitType.TANK or \
                (unit.get_unit_type() == TankWarUnitType.TILE and unit.get_pos() not in self.get_recyclers_positions())]
    
    def get_tank_and_available_tiles_positions(self) -> List['TankWarUnit']:
        """Get all tanks and tiles from the collection."""
        positions = []
        for unit in self.units:
            if unit.get_unit_type() == TankWarUnitType.TANK or \
                (unit.get_unit_type() == TankWarUnitType.TILE and unit.get_pos() not in self.get_recyclers_positions()) \
                and unit.pos not in positions:
                positions.append(unit.pos)
        return positions
    
    def get_tank_units(self) -> List['TankWarUnit']:
        """Get all tanks and tiles from the collection."""
        return [unit for unit in self.units if unit.get_unit_type() == TankWarUnitType.TANK]

    def get_unit_in_pos(self, pos: Tuple[int, int]) -> 'TankWarUnit':
        """Get the unit in a position."""
        units = list(filter(lambda unit: unit.pos == pos, self.units))
        return units[0]

    def get_tank_in_position(self, pos: Tuple[int, int]) -> 'TankWarUnit':
        """Get the tank in a position."""
        tanks = list(filter(lambda unit: unit.pos == pos and unit.get_unit_type() == TankWarUnitType.TANK, self.units))
        if len(tanks) == 0:
            return None
        return tanks[0]

    def get_recycler_in_position(self, pos: Tuple[int, int]) -> 'TankWarUnit':
        """Get the unit in a position."""
        recyclers = list(filter(lambda unit: unit.pos == pos and unit.get_unit_type() == TankWarUnitType.RECYCLER, self.units))
        if len(recyclers) == 0:
            return None
        return recyclers[0]
        
    def get_count_tanks_in_position(self, pos: Tuple[int, int]) -> int:
        """Get the number of tanks in a position."""
        return len([unit for unit in self.units if unit.get_unit_type() == TankWarUnitType.TANK and unit.pos == pos])
# endregion

# region Positions
    def get_tiles_positions(self) -> List[Tuple[int, int]]:
        """Get all tiles positions not occupied by units."""
        return [unit.pos for unit in self.units if unit.get_unit_type() == TankWarUnitType.TILE]

    def get_tanks_positions(self) -> List[Tuple[int, int]]:
        """Get all tanks positions."""
        positions = []
        for unit in self.units:
            if unit.get_unit_type() == TankWarUnitType.TANK and unit.pos not in positions:
                positions.append(unit.pos)
        return positions

    def get_recyclers_positions(self) -> List[Tuple[int, int]]:
        """Get all recyclers positions."""
        return [unit.pos for unit in self.units if unit.get_unit_type() == TankWarUnitType.RECYCLER]
# endregion

# region Overrides
    def __str__(self) -> str:
        return f"Tanks: {self.get_tanks_positions()}, Recyclers: {self.get_recyclers_positions()}, Tiles: {self.get_tiles_positions()}"
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, TankWarUnitCollection):
            return False
        return self.units == __o.units
    
    def __hash__(self) -> int:
        if len(self.units) == 0:
            return 0
        unit_dict = defaultdict(int)
        for card in self.units:
            unit_dict[card] += 1
        hashed = "".join([str(unit.__hash__()) + str(unit_dict[unit]) for unit in unit_dict])
        return int(hashed)
# endregion)