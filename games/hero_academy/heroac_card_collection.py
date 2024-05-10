from collections import defaultdict
from typing import List
from games.hero_academy.heroac_card import HeroAcademyCard
from games.hero_academy.heroac_unit_collection import HeroAcademyUnitCollection

class HeroAcademyCardCollection:
    def __init__(self):
        self.cards: List['HeroAcademyCard'] = []

# region Methods
    def clone(self) -> 'HeroAcademyCardCollection':
        """Create new collection with the same cards."""
        new_card_collection = HeroAcademyCardCollection()
        for card in self.cards:
            new_card_collection.add_card(card.clone())
        return new_card_collection

    def add_card(self, card: 'HeroAcademyCard'):
        """Add a card to the collection."""
        self.cards.append(card)

    def add_cards(self, cards: List['HeroAcademyCard']):
        """Add a list of cards to the collection."""
        self.cards.extend(cards)

    def remove_card(self, card: 'HeroAcademyCard'):
        """Remove a card from the collection."""
        self.cards.remove(card)
# endregion

# region Getters
    def get_cards(self) -> List['HeroAcademyCard']:
        """Get all cards."""
        return self.cards
    
    def get_first_card(self) -> 'HeroAcademyCard':
        """Get the first card from the collection."""
        if len(self.cards) == 0:
            return None
        return self.cards.pop(0)
    
    def get_number_cards(self) -> bool:
        """Get the number of cards in the collection."""
        return len(self.cards)
    
    def get_playable_cards(self, units: 'HeroAcademyUnitCollection', enemies: 'HeroAcademyUnitCollection') -> List['HeroAcademyCard']:
        """Get all cards that can be played."""
        cards = []
        for card in self.cards:
            if units.is_card_playable(card) or enemies.is_card_playable(card, True):
                cards.append(card.clone())
        return cards
    
    def get_unit_cards(self) -> List['HeroAcademyCard']:
        """Get all unit cards."""
        return [card for card in self.cards if card.get_value().is_unit_value()]
# endregion

# region Helpers
    def is_empty(self) -> bool:
        """Check if the collection is empty."""
        return len(self.cards) == 0
# endregion

# region Override
    def __str__(self) -> str:
        cards_srt = ", ".join([str(card) for card in self.cards])
        return f"CardCollection(cards={cards_srt})"
    
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, HeroAcademyCardCollection):
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