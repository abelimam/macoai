from games import Action
from games.asmacag.asmacag_card import AsmacagCard

class AsmacagAction(Action):
    """An `Action` describes the `Card` played and on what `Card` it has been played."""

    def __init__(self, played_card: 'AsmacagCard', board_card: 'AsmacagCard' = None):
        self.played_card = played_card
        self.board_card = board_card

# region Methods
    def clone(self) -> 'AsmacagAction':
        """Creates a deep copy of the `Action` and returns it."""
        new_action = AsmacagAction(self.played_card.clone(), self.board_card.clone() if self.board_card is not None else None)
        return new_action

    def copy_into(self, other: 'AsmacagAction') -> None:
        """Deep copies the `Action` contents into another one."""
        self.played_card.copy_into(other.played_card)
        if self.board_card is not None:
            if other.board_card is None:
                other.board_card = self.board_card.clone()
            else:
                self.board_card.copy_into(other.board_card)
        else:
            other.board_card = None
# endregion

# region Getters and setters
    def get_played_card(self) -> 'AsmacagCard':
        """Returns the `Card` played."""
        return self.played_card

    def get_board_card(self) -> 'AsmacagCard':
        """Returns the `Card` on which the `Action.get_played_card` has been played."""
        return self.board_card
# endregion

# region Overrides
    def __str__(self):
        return f"[{self.played_card!s}] on [{self.board_card if self.board_card is not None else 'nothing'!s}]"
# endregion