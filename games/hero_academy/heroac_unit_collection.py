from typing import Dict, List, Tuple
from copy import deepcopy
from games.hero_academy.heroac_card_value import HeroAcademyCardValue
from games.hero_academy.heroac_card import HeroAcademyCard
from games.hero_academy.heroac_tile_type import HeroAcademyTileType
from games.hero_academy.heroac_unit import HeroAcademyUnit

class HeroAcademyUnitCollection:
    """A collection of units the player will use during the game."""

    def __init__(self) -> None:
        self.units: List['HeroAcademyUnit'] = []

# region Methods
    def clone(self) -> 'HeroAcademyUnitCollection':
        """Create new collection with the same units."""
        new_units_collection = HeroAcademyUnitCollection()
        for unit in self.units:
            new_units_collection.add_unit(unit.clone())
        return new_units_collection

    def add_unit(self, unit: 'HeroAcademyUnit'):
        """Add a unit to the collection."""
        self.units.append(unit)

    def add_units(self, units: List['HeroAcademyUnit']):
        """Add a list of units to the collection."""
        self.units.extend(units)

    def remove_unit(self, unit: 'HeroAcademyUnit'):
        """Remove a unit from the collection."""
        self.units.remove(unit)

    def move_unit(self, unit: 'HeroAcademyUnit', pos: Tuple[int, int]):
        """Move a unit to a new position."""
        unit.pos = deepcopy(pos)
# endregion

# region Getters
    def get_units(self) -> List['HeroAcademyUnit']:
        """Get all units."""
        return self.units
    
    def get_crystals(self) -> List['HeroAcademyUnit']:
        """Get all crystals."""
        return [unit for unit in self.units if unit is not None and unit.get_card().get_value().is_crystal_value() and unit.hp > 0]
    
    def get_unit_positions(self) -> List[Tuple[int, int]]:
        """Get all unit positions."""
        return [unit.pos for unit in self.units]

    def get_available_units(self) -> List['HeroAcademyUnit']:
        """Get all units that are not dead."""
        return [unit for unit in self.units if unit.get_card().get_value().is_unit_value()]
    
    def get_playable_units(self, units: 'HeroAcademyUnitCollection', enemies: 'HeroAcademyUnitCollection', board_size: Tuple[int, int], board: Dict[Tuple[int, int], 'HeroAcademyTileType'])\
        -> List[Tuple['HeroAcademyUnit', List[Tuple[int, int]], bool, bool]]:
        """Get all units that can be played."""
        playable_units = []
        for unit in self.units:
            positions = units.get_unit_positions()
            positions.extend(enemies.get_unit_positions())
            moves = unit.possible_moves(board_size, board[unit.get_pos()] == HeroAcademyTileType.SPEED, positions)
            attack = enemies.can_be_attacked(unit)
            heal = units.can_be_healed(unit)
            if unit.get_card().get_value().is_unit_value() and (attack or heal or len(moves) > 0):
                playable_units.append((unit.clone(), moves, attack, heal))
        return playable_units
        
    def get_units_in_range(self, other: 'HeroAcademyUnit') -> List['HeroAcademyUnit']:
        """Return a list of units in range of the unit."""
        return [unit for unit in self.units if unit.is_in_range(other)]
    
    def get_avalible_positions_for_spawn(self, player_1 = False, board_size: Tuple[int, int] = None, taken_positions: List[Tuple[int, int]] = []) -> List[Tuple[int, int]]:
        """Return a list of positions where a unit can be spawned."""
        taken_positions.extend(self.get_unit_positions())
        if player_1 and board_size is not None:
            return [(x, y) for x in range(5) for y in range(board_size[1] - 4, board_size[1]) if (x, y) not in taken_positions]
        return [(x, y) for x in range(5) for y in range(4) if (x, y) not in taken_positions]
    
    def get_unit_in_position(self, pos: Tuple[int, int]) -> 'HeroAcademyUnit':
        """Return the unit in the given position."""
        return next((unit for unit in self.units if unit.pos == pos), None)
    
    def get_units_alive(self) -> int:
        """Return the number of all units that are not dead."""
        return len(self.get_available_units())
    
    def get_units_equipement_count(self) -> int:
        """Return the total number of equipement on all units."""
        return sum([len(unit.get_unique_equipement()) for unit in self.units])
# endregion

# region Helpers
    def crystals_alive(self) -> bool:
        """Return True if there are crystals alive."""
        return len(self.get_crystals()) > 0
    
    def is_card_playable(self, card: 'HeroAcademyCard', is_enemy = False) -> bool:
        """Check if card is playable."""
        is_playable = card.value.is_unit_value()
        if is_enemy:
            is_playable = is_playable or (card.value.is_spell_value() and len(self.get_units()) > 0)
        else:
            is_playable = is_playable or (card.value.is_item_value() and len(self.get_available_units()) > 0)
        return is_playable

    def can_be_attacked(self, unit: 'HeroAcademyUnit') -> bool:
        """Check if unit can be attacked."""
        return len(self.get_units_in_range(unit)) > 0
    
    def can_be_healed(self, unit: 'HeroAcademyUnit') -> bool:
        """Check if unit can be healed."""
        return len(self.get_units_in_range(unit)) > 0 and unit.get_card().get_value() == HeroAcademyCardValue.CLERIC

# endregion

# region Override
    def __str__(self) -> str:
        units_str = ", ".join([str(unit) for unit in self.units])
        return f"UnitsCollection(units={units_str})"
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, HeroAcademyUnitCollection):
            return False
        return self.units == __o.units
    
    def __hash__(self) -> int:
        if len(self.units) == 0:
            return 0
        return int("".join([str(unit.__hash__()) for unit in self.units]))
# endregion