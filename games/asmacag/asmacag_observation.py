from typing import Any, Dict, List
from games import Observation
from games.asmacag.asmacag_card_type import AsmacagCardType
from games.asmacag.asmacag_card_collection import AsmacagCardCollection
from games.asmacag.asmacag_action import AsmacagAction
from games.asmacag.asmacag_game_parameters import AsmacagGameParameters
import random

class AsmacagObservation(Observation):
    """A `GameState` view for a particular `Player` where the non-observable parts have been randomized."""
    def __init__(self, game_state_info: Dict[str, Any], randomise_hidden_info: bool = True):
        if game_state_info is not None:
            self.game_parameters: 'AsmacagGameParameters' = game_state_info['game_parameters']
            self.current_turn = game_state_info['current_turn']
            self.player_0_hand: 'AsmacagCardCollection' = game_state_info['player_0_hand']
            self.player_1_hand: 'AsmacagCardCollection' = game_state_info['player_1_hand']
            self.board: 'AsmacagCardCollection' = game_state_info['board']
            self.main_deck: 'AsmacagCardCollection' = game_state_info['main_deck']
            self.discard_deck: 'AsmacagCardCollection' = game_state_info['discard_deck']
            self.player_0_score = game_state_info['player_0_score']
            self.player_1_score = game_state_info['player_1_score']
            self.factor = game_state_info['factor']
            self.action_points_left = game_state_info['action_points_left']
            if randomise_hidden_info:
                self.randomise()

# region Methods
    def clone(self) -> 'AsmacagObservation':
        """Creates a deep copy of the `Observation` and returns it."""
        new_observation = AsmacagObservation(None)
        new_observation.game_parameters = self.game_parameters
        new_observation.current_turn = self.current_turn
        new_observation.player_0_hand = self.player_0_hand.clone()
        new_observation.player_1_hand = self.player_1_hand.clone()
        new_observation.board = self.board.clone()
        new_observation.main_deck = self.main_deck.clone()
        new_observation.discard_deck = self.discard_deck.clone()
        new_observation.player_0_score = self.player_0_score
        new_observation.player_1_score = self.player_1_score
        new_observation.factor = self.factor
        new_observation.action_points_left = self.action_points_left 
        return new_observation

    def copy_into(self, other: 'AsmacagObservation') -> None:
        """Deep copies the `Observation` contents into another one."""
        other.game_parameters = self.game_parameters
        other.current_turn = self.current_turn
        self.player_0_hand.copy_into(other.player_0_hand)
        self.player_1_hand.copy_into(other.player_1_hand)
        self.board.copy_into(other.board)
        self.main_deck.copy_into(other.main_deck)
        self.discard_deck.copy_into(other.discard_deck)
        other.player_0_score = self.player_0_score
        other.player_1_score = self.player_1_score
        other.factor = self.factor
        other.action_points_left = self.action_points_left

    def randomise(self) -> None:
        """Randomises the `Observation` to get a new possible state of the `Game`."""
        # shuffle together all non-visible cards in the main deck
        self.main_deck.add_cards(self.player_1_hand if self.current_turn == 0 else self.player_0_hand)
        self.main_deck.shuffle()

        # draw cards to opponent hand
        if self.current_turn == 0:
            for _ in range(self.game_parameters.amount_cards_on_hand):
                self.player_1_hand.add_card(self.main_deck.draw())
        else:
            for _ in range(self.game_parameters.amount_cards_on_hand):
                self.player_0_hand.add_card(self.main_deck.draw())

    def is_action_valid(self, action: 'AsmacagAction') -> bool:
        """Checks if the given `Action` is currently valid."""
        hand = self.player_0_hand if self.current_turn == 0 else self.player_1_hand
        if action.get_played_card().get_type() == AsmacagCardType.NUMBER:
            return action.get_played_card() in hand.get_cards() and action.get_board_card() in self.board.get_cards()
        else:
            return action.get_played_card() in hand.get_cards()
# endregion

# region Getters and Setters
    def get_actions(self) -> List['AsmacagAction']:
        """Gets a list of the currently possible `Action`."""
        actions = []
        hand = self.player_0_hand if self.current_turn == 0 else self.player_1_hand
        
        for card in set(hand.get_cards()):
            if card.get_type() == AsmacagCardType.NUMBER:
                for board_card in set(self.board.get_cards()):
                    actions.append(AsmacagAction(card.clone(), board_card.clone()))
            else:
                actions.append(AsmacagAction(card.clone()))
        return actions

    def get_random_action(self) -> 'AsmacagAction':
        """Gets a random `Action` that is currently valid."""
        hand = self.player_0_hand if self.current_turn == 0 else self.player_1_hand

        hand_card = random.choice(hand.get_cards())
        if hand_card.get_type() == AsmacagCardType.NUMBER:
            return AsmacagAction(hand_card.clone(), random.choice(self.board.get_cards()).clone())
        else:
            return AsmacagAction(hand_card.clone())
# endregion

# region Overrides
    def get_game_parameters(self) -> 'AsmacagGameParameters':
        return self.game_parameters
    
    def get_action_points_left(self) -> int:
        return self.action_points_left
    
    def get_current_turn(self) -> int:
        return self.current_turn
    
    def get_player_0_score(self) -> int:
        return self.player_0_score
    
    def get_player_1_score(self) -> int:
        return self.player_1_score

    def __str__(self):
        return (f"TURN: {self.current_turn!s}\n"
                f"BOARD: {self.board!s}\n"
                f"HAND P1: {self.player_0_hand!s}\n"
                f"SCORE P1: {self.player_0_score!s}\n"
                f"HAND P2: {self.player_1_hand!s}\n"
                f"SCORE P2: {self.player_1_score!s}\n"
                f"FACTOR: {self.factor!s}\n"
                f"ACTION POINTS LEFT: {self.action_points_left!s}")
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, AsmacagObservation):
            return False
        return (self.game_parameters == __o.game_parameters and
                self.current_turn == __o.current_turn and
                self.player_0_hand == __o.player_0_hand and
                self.player_1_hand == __o.player_1_hand and
                self.board == __o.board and
                self.main_deck == __o.main_deck and
                self.discard_deck == __o.discard_deck and
                self.player_0_score == __o.player_0_score and
                self.player_1_score == __o.player_1_score and
                self.factor == __o.factor and
                self.action_points_left == __o.action_points_left)
    
    def __hash__(self) -> int:
        hashed = f"{self.current_turn}{self.action_points_left}{self.player_0_score}{self.player_1_score}{self.factor}"
        hashed += f"{self.player_0_hand.__hash__()}{self.player_1_hand.__hash__()}{self.board.__hash__()}{self.main_deck.__hash__()}"
        return hash(hashed)
# endregion