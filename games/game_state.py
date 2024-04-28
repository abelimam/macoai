from abc import ABC, abstractmethod
from typing import Any, Dict
from games.game_parameters import GameParameters
from games.observation import Observation

class GameState(ABC):
    """Abstract class that will define the state of the game"""

    @abstractmethod
    def get_game_parameters(self) -> 'GameParameters':
        """Returns the parameters of the game"""
        pass

    @abstractmethod
    def get_action_points_left(self) -> int:
        """Returns the number of action points left"""
        pass

    @abstractmethod
    def get_current_turn(self) -> int:
        """Returns the current turn"""
        pass

    @abstractmethod
    def get_player_0_score(self) -> int:
        """Returns the score of player 0"""
        pass

    @abstractmethod
    def get_player_1_score(self) -> int:
        """Returns the score of player 1"""
        pass

    @abstractmethod
    def get_observation(self) -> 'Observation':
        """Returns the observation of the game state"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Resets the game state"""
        pass

    @abstractmethod
    def get_state_info(self) -> Dict[str, Any]:
        """Returns the information of the game state"""
        pass