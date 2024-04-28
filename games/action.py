from abc import ABC, abstractmethod

class Action(ABC):
    """Abstract class that will define an action of the game"""

    @abstractmethod
    def clone(self) -> 'Action':
        """Return a copy of the action"""
        pass
    
    @abstractmethod
    def copy_into(self, other: 'Action') -> None:
        """Copy the action into another action"""
        pass