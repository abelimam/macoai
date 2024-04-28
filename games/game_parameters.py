from abc import ABC, abstractmethod
from typing import Optional

class GameParameters(ABC):
    """Abstract class that will define the parameters of the game"""

    @abstractmethod
    def get_action_points_per_turn(self) -> int:
        """Returns the amount of action points per turn"""
        pass

    @abstractmethod
    def get_seed(self) -> Optional[int]:
        """Returns the seed of the game"""
        pass