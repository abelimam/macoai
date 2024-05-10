from collections import defaultdict
from typing import Iterable, List
from games.asmacag.asmacag_card import AsmacagCard
import random

class AsmacagCardCollection:
    """An ordered collection of `Card` that can be used to define a deck, hand, table..."""
    def __init__(self):
        self.cards: List['AsmacagCard'] = []

# region Methods
    def clear(self) -> None:
        """Empties the `CardCollection`."""
        self.cards.clear()

    def add_card(self, card: 'AsmacagCard') -> "None":
        """Adds a `Card` to the `CardCollection`."""
        self.cards.append(card)

    def add_cards(self, cards: Iterable['AsmacagCard']) -> "None":
        """Adds any iterable collection of `Card` to the `CardCollection`."""
        self.cards.extend(cards)

    def shuffle(self) -> None:
        """Shuffles the `CardCollection`."""
        random.shuffle(self.cards)

    def draw(self) -> 'AsmacagCard':
        """Removes and returns the first `Card` from the `CardCollection`."""
        card = self.cards[0]
        self.cards.pop(0)
        return card

    def remove(self, card: 'AsmacagCard') -> None:
        """Removes the fist occurrence of the specified `Card` from the `CardCollection`."""
        self.cards.remove(card)

    def clone(self) -> 'AsmacagCardCollection':
        """Creates a deep copy of the `CardCollection` and returns it."""
        new_card_collection = AsmacagCardCollection()

        for card in self.cards:
            new_card_collection.add_card(card.clone())

        return new_card_collection

    def copy_into(self, other: 'AsmacagCardCollection') -> None:
        """Deep copies the `CardCollection` contents into another one."""
        if len(self) >= len(other):
            for cardIndex in range(len(other)):
                self.get_card(cardIndex).copy_into(other.get_card(cardIndex))

            for card in range(len(other), len(self.cards)):
                other.add_card(self.cards[card].clone())

        else:
            del other.cards[len(self):]
            for cardIndex in range(len(self)):
                self.get_card(cardIndex).copy_into(other.get_card(cardIndex))
# endregion

# region Getters and setters
    def get_empty(self) -> bool:
        """Returns a bool stating whether the `CardCollection` is empty."""
        if self.cards:
            return False
        return True

    def get_cards(self) -> List['AsmacagCard']:
        """Returns the ordered list of `Card` contained in the `CardCollection`."""
        return self.cards

    def get_card(self, index: int) -> 'AsmacagCard':
        """Returns the `Card` contained in the `CardCollection` at the specified index."""
        return self.cards[index]
# endregion

# region Overrides
    def __str__(self):
        s = ""
        for card in self.cards:
            s += f"[{card!s}] "
        return s

    def __iter__(self):
        return self.cards.__iter__()

    def __len__(self):
        return len(self.cards)
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, AsmacagCardCollection):
            return False
        return self.cards == __o.cards
    
    def __hash__(self) -> int:
        if len(self.cards) == 0:
            return 0
        card_dict = defaultdict(int)
        for card in self.cards:
            card_dict[card] += 1
        hashed = "".join([str(card.__hash__()) + str(card_dict[card]) for card in card_dict])
        return int(hashed)
# endregion