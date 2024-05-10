from typing import Any, Dict, Tuple
from games import GameState
from games.hero_academy.heroac_tile_type import HeroAcademyTileType
from games.hero_academy.heroac_card_type import HeroAcademyCardType
from games.hero_academy.heroac_card_value import HeroAcademyCardValue
from games.hero_academy.heroac_card import HeroAcademyCard
from games.hero_academy.heroac_unit import HeroAcademyUnit
from games.hero_academy.heroac_unit_collection import HeroAcademyUnitCollection
from games.hero_academy.heroac_card_collection import HeroAcademyCardCollection
from games.hero_academy.heroac_game_parameters import HeroAcademyGameParameters
from games.hero_academy.heroac_observation import HeroAcademyObservation
import random

class HeroAcademyGameState(GameState):
    """GameState class represents the state of the game."""

    def __init__(self, game_parameters: 'HeroAcademyGameParameters') -> None:
        self.game_parameters = game_parameters
        self.current_turn = 0
        self.player_0_score = 0
        self.player_1_score = 0
        self.action_points_left = 0
        self.board = self.initiliaze_board_dict()
        self.player_0_deck: 'HeroAcademyCardCollection' = self.initiliaze_deck()
        self.player_1_deck: 'HeroAcademyCardCollection' = self.initiliaze_deck()
        self.player_0_cards: 'HeroAcademyCardCollection' = self.initiliaze_cards(self.player_0_deck)
        self.player_1_cards: 'HeroAcademyCardCollection' = self.initiliaze_cards(self.player_1_deck)
        self.player_0_units: 'HeroAcademyUnitCollection' = self.initiliaze_units()
        self.player_1_units: 'HeroAcademyUnitCollection' = self.initiliaze_units(False)

# region Methods
    def get_observation(self) -> 'HeroAcademyObservation':
        """Return the observation of the game state."""
        return HeroAcademyObservation(self.get_state_info(), False)

    def reset(self) -> None:
        """Reset the game state."""
        self.current_turn = 0
        self.player_0_score = 0
        self.player_1_score = 0
        self.action_points_left = self.game_parameters.action_points_per_turn
        self.board = self.initiliaze_board_dict()
        self.player_0_deck = self.initiliaze_deck()
        self.player_1_deck = self.initiliaze_deck()
        self.player_0_cards: 'HeroAcademyCardCollection' = self.initiliaze_cards(self.player_0_deck)
        self.player_1_cards: 'HeroAcademyCardCollection' = self.initiliaze_cards(self.player_1_deck)
        self.player_0_units = self.initiliaze_units()
        self.player_1_units = self.initiliaze_units(False)
#endregion

#region Helpers
    def initiliaze_board_dict(self) -> Dict[Tuple[int, int], 'HeroAcademyTileType']:
        """Initialize the board of the game."""
        board_size = self.game_parameters.board_size
        board = {(i, j): HeroAcademyTileType.EMPTY for i in range(board_size[0]) for j in range(board_size[1])}
        for attack in self.game_parameters.attack_positions:
            board[attack] = HeroAcademyTileType.ATTACK
            board[(attack[0], board_size[1] - attack[1] - 1)] = HeroAcademyTileType.ATTACK
        for speed in self.game_parameters.speed_positions:
            board[speed] = HeroAcademyTileType.SPEED
            board[(speed[0], board_size[1] - speed[1] - 1)] = HeroAcademyTileType.SPEED
        return board

    def initiliaze_cards(self, deck: 'HeroAcademyCardCollection') -> 'HeroAcademyCardCollection':
        """Initialize the cards of the game."""
        cards = HeroAcademyCardCollection()
        for _ in range(self.game_parameters.cards_on_hand):
            cards.add_card(deck.get_first_card())
        return cards

    def initiliaze_deck(self) -> 'HeroAcademyCardCollection':
        """Initialize the deck of the game."""
        deck = HeroAcademyCardCollection()
        for value in HeroAcademyCardValue:
            if value is not HeroAcademyCardValue.CRYSTAL:
                deck.add_card(HeroAcademyCard(value, value.get_card_type()))
                deck.add_card(HeroAcademyCard(value, value.get_card_type()))
                deck.add_card(HeroAcademyCard(value, value.get_card_type()))
                if value.is_spell_value() or value.is_item_value():
                    deck.add_card(HeroAcademyCard(value, value.get_card_type()))
                    deck.add_card(HeroAcademyCard(value, value.get_card_type()))
        random.shuffle(deck.cards)
        return deck

    def initiliaze_units(self, player_1 = True) -> 'HeroAcademyUnitCollection':
        """Initialize the units of the game."""
        units = HeroAcademyUnitCollection()
        for crystal in self.game_parameters.crystal_positions:
            position = (crystal[0], crystal[1]) if player_1 else (crystal[0], self.game_parameters.board_size[1] - crystal[1] - 1)
            card = HeroAcademyCard(HeroAcademyCardValue.CRYSTAL, HeroAcademyCardType.UNIT)
            units.add_unit(HeroAcademyUnit.create(card, position))
        return units
#endregion

# region Setters
    def set_current_player_score(self, score: int):
        if self.current_turn == 0:
            self.player_0_score = score
        else:
            self.player_1_score = score

    def set_enemy_player_score(self, score: int):
        if self.current_turn == 0:
            self.player_1_score = score
        else:
            self.player_0_score = score

    def get_current_player_units(self) -> 'HeroAcademyUnitCollection':
        if self.current_turn == 0:
            return self.player_0_units
        else:
            return self.player_1_units
        
    def get_enemy_player_units(self) -> 'HeroAcademyUnitCollection':
        if self.current_turn == 0:
            return self.player_1_units
        else:
            return self.player_0_units
# endregion

#region Override
    def get_current_turn(self) -> int:
        return self.current_turn
    
    def get_action_points_left(self) -> int:
        return self.action_points_left
    
    def get_game_parameters(self) -> 'HeroAcademyGameParameters':
        return self.game_parameters
    
    def get_player_0_score(self) -> int:
        return self.player_0_score
    
    def get_player_1_score(self) -> int:
        return self.player_1_score
    
    def get_state_info(self) -> Dict[str, Any]:
        return {
            "current_turn": self.current_turn,
            "board": self.board.copy(),
            "player_0_score": self.player_0_score,
            "player_0_cards": self.player_0_cards.clone(),
            "player_0_deck": self.player_0_deck.clone(),
            "player_0_units": self.player_0_units.clone(),
            "player_1_score": self.player_1_score,
            "player_1_cards": self.player_1_cards.clone(),
            "player_1_deck": self.player_1_deck.clone(),
            "player_1_units": self.player_1_units.clone(),
            "action_points_left": self.action_points_left,
            "game_parameters": self.game_parameters
        }
    
    def __str__(self):
        return (f"TURN: {self.current_turn!s}\n"
                #f"BOARD: {self.board!s}\n"
                f"SCORE P1: {self.player_0_score!s}\n"
                f"CARDS P1: {self.player_0_cards!s}\n"
                f"UNITS P1: {self.player_0_units!s}\n"
                f"SCORE P2: {self.player_1_score!s}\n"
                f"CARDS P2: {self.player_1_cards!s}\n"
                f"UNITS P2: {self.player_1_units!s}\n"
                f"ACTION POINTS LEFT: {self.action_points_left!s}")
#endregion