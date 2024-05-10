from games.asmacag.asmacag_card_type import AsmacagCardType

class AsmacagCard:
    """A `Card` has a `CardType`. It also has a number if it is a `CardType.NUMBER`."""

    def __init__(self, card_type: 'AsmacagCardType', number: int = None):
        self.card_type = card_type
        self.number = number

# region Methods
    def clone(self) -> 'AsmacagCard':
        """Creates a copy of the `Card` and returns it."""
        new_card = AsmacagCard(self.card_type, self.number)
        return new_card

    def copy_into(self, other: 'AsmacagCard') -> None:
        """Copies the `Card` contents into another one."""
        other.card_type = self.card_type
        other.number = self.number
# endregion

# region Getters and setters
    def get_type(self) -> 'AsmacagCardType':
        """Returns the type of the `Card` as a `CardType`."""
        return self.card_type

    def get_number(self) -> int:
        """Returns the number of the `Card`."""
        return self.number
# endregion

# region Overrides
    def __str__(self):
        return f"{self.card_type!s}{f' {self.number}' if self.card_type == AsmacagCardType.NUMBER else ''!s}"

    def __eq__(self, other):
        return isinstance(other, AsmacagCard) and self.card_type == other.card_type and self.number == other.number

    def __hash__(self):
        # note that this may not generate a unique hash for parameter sets that are not the default ones
        return self.number + 1 if self.card_type == AsmacagCardType.NUMBER else self.card_type.value - 2
# endregion