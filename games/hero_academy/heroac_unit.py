from typing import Tuple, List
from copy import deepcopy
from games.hero_academy.heroac_card_value import HeroAcademyCardValue
from games.hero_academy.heroac_card import HeroAcademyCard

class HeroAcademyUnit:
    def __init__(
        self,
        card: 'HeroAcademyCard',
        hp: int,
        max_hp: int,
        speed: int,
        power: int,
        range: int,
        resistance: int,
        pos: Tuple[int, int],
        equipement: List['HeroAcademyCard']
    ) -> None:
        """Unit is a base class for all units that a player can use in the game."""
        self.card = card
        self.hp = hp
        self.max_hp = max_hp
        self.speed = speed
        self.power = power
        self.range = range
        self.resistance = resistance
        self.pos = pos
        self.equipement = equipement

# region Methods
    def clone(self) -> 'HeroAcademyUnit':
        """Create new unit with the same info."""
        return HeroAcademyUnit(
            self.card.clone(),
            self.hp,
            self.max_hp,
            self.speed,
            self.power,
            self.range,
            self.resistance,
            deepcopy(self.pos),
            deepcopy(self.equipement)
        )

    def copy_into(self, other: 'HeroAcademyUnit') -> None:
        """Copies the unit contents into another one."""
        other.card = self.card.clone()
        other.hp = self.hp
        other.max_hp = self.max_hp
        other.speed = self.speed
        other.power = self.power
        other.range = self.range
        other.resistance = self.resistance   
        other.pos = deepcopy(self.pos)
        other.equipement = deepcopy(self.equipement)
# endregion

# region Getters
    def get_card(self) -> 'HeroAcademyCard':
        """Get unit card."""
        return self.card

    def get_pos(self) -> Tuple[int, int]:
        """Get unit position."""
        return self.pos

    def get_hp(self) -> int:
        """Get unit hp."""
        return self.hp

    def get_max_hp(self) -> int:
        """Get unit max hp."""
        return self.max_hp

    def get_speed(self) -> int:
        """Get unit speed."""
        return self.speed

    def get_power(self) -> int:
        """Get unit power."""
        return self.power
    
    def get_range(self) -> int:
        """Get unit range."""
        return self.range

    def get_resistance(self) -> int:
        """Get unit resistance."""
        return self.resistance
    
    def get_equipement(self) -> List['HeroAcademyCard']:
        """Get unit equipement."""
        return self.equipement
    
    def get_attack_equipement(self) -> List['HeroAcademyCard']:
        """Get unit attack equipement."""
        return [card for card in self.equipement if card.get_value() == HeroAcademyCardValue.RUNEMETAL and card.get_card_type() == HeroAcademyCardValue.SCROLL]
    
    def get_defense_equipement(self) -> List['HeroAcademyCard']:
        """Get unit defense equipement."""
        return [card for card in self.equipement if card.get_value() == HeroAcademyCardValue.DRAGONSCALE and card.get_card_type() == HeroAcademyCardValue.SHINING_HELM]
    
    def get_unique_equipement(self) -> List['HeroAcademyCard']:
        """Get unit unique equipement."""
        equipement = []
        [equipement.append(card) for card in self.equipement if card not in equipement]
        return equipement
    
    def get_bonus_attack(self, is_on_attack_tile = False) -> int:
        dmg = self.power
        if self.card.get_value() == HeroAcademyCardValue.CLERIC:
            dmg = 0.5 * self.power
        for card in self.get_attack_equipement():
            if card.get_card_type() == HeroAcademyCardValue.SCROLL:
                dmg += 0.1 * self.power
            else:
                dmg += 0.2 * self.power
        if is_on_attack_tile:
            dmg += 0.15 * self.power
        return dmg
# endregion

# region Setters
    def set_hp(self, hp: int) -> None:
        """Set unit hp."""
        self.hp = min(hp, self.max_hp)

    def set_pos(self, pos: Tuple[int, int]) -> None:
        """Set unit position."""
        self.pos = deepcopy(pos)
# endregion

# region Helpers
    def possible_moves(self, board_size: Tuple[int, int], is_on_speed_tile = False, taken_positions: List[Tuple[int, int]] = []) -> List[Tuple[int, int]]:
        """Return a list of possible moves for the unit."""
        moves = []
        speed = self.speed if not is_on_speed_tile else self.speed + 1
        for x in range(self.pos[0] - speed, self.pos[0] + speed + 1):
            for y in range(self.pos[1] - speed, self.pos[1] + speed + 1):
                if x >= 0 and x < board_size[0] and y >= 0 and y < board_size[1] and (x, y) != self.pos and (x, y) not in taken_positions:
                    moves.append((x, y))
        return moves
    
    def is_in_range(self, other: 'HeroAcademyUnit') -> bool:
        """Check if the unit is in range of the other unit."""
        return other.get_range() >= abs(self.pos[0] - other.pos[0]) + abs(self.pos[1] - other.pos[1])
    
    def attack_unit(self, other: 'HeroAcademyUnit', is_on_attack_tile = False) -> None:
        """Attack other unit."""
        dmg = self.get_bonus_attack(is_on_attack_tile)
        res = other.resistance
        for card in other.get_defense_equipement():
            res += 0.1 * other.resistance if card.get_card_type() == HeroAcademyCardValue.SHINING_HELM else res + 0.2 * other.resistance
        intake = int(dmg * (100 - res) / 100)
        other.set_hp(other.get_hp() - intake)
# endregion

# region Static
    @staticmethod
    def create(card: 'HeroAcademyCard', position: Tuple[int, int]) -> 'HeroAcademyUnit':
        if card.get_value() == HeroAcademyCardValue.ARCHER:
            return HeroAcademyUnit(card.clone(), 700, 700, 2, 200, 4, 5, deepcopy(position), [])
        elif card.get_value() == HeroAcademyCardValue.KNIGHT:
            return HeroAcademyUnit(card.clone(), 1000, 1000, 1, 250, 1, 20, deepcopy(position), [])
        elif card.get_value() == HeroAcademyCardValue.CLERIC:
            return HeroAcademyUnit(card.clone(), 600, 600, 1, 200, 2, 0, deepcopy(position), [])
        elif card.get_value() == HeroAcademyCardValue.WIZARD:
            return HeroAcademyUnit(card.clone(), 800, 800, 2, 200, 2, 10, deepcopy(position), [])
        elif card.get_value() == HeroAcademyCardValue.NINJA:
            return HeroAcademyUnit(card.clone(), 700, 700, 3, 200, 1, 5, deepcopy(position), [])
        elif card.get_value() == HeroAcademyCardValue.CRYSTAL:
            return HeroAcademyUnit(card.clone(), 4500, 4500, 0, 0, 0, 30, deepcopy(position), [])
        else:
            return None
# endregion

# region Override
    def __str__(self) -> str:
        return (
            f"Unit[{self.card.get_value().name}, HP: {self.hp} / {self.max_hp}, POS: {self.pos}]"
            #f"Speed: {self.speed}\n"
            #f"Power: {self.power}\n"
            #f"{self.card}\n"
            #f"{self.resistance}\n"
            #f"Pos: {self.pos}\n"
            #f"Equipement: {self.equipement}"
        )
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, HeroAcademyUnit):
            return False
        return self.card == __o.card and self.hp == __o.hp and self.pos == __o.pos and self.equipement == __o.equipement
    
    def __hash__(self) -> int:
        hashed = f"{self.card.__hash__()}{self.hp}{self.pos[0]}{self.pos[1]}"
        hashed += "".join([str(card.__hash__()) for card in self.equipement])
        return int(hashed)
# endregion