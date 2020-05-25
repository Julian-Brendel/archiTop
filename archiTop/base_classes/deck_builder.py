"""Sourcefile containing base_class for TableTop deck construction"""
from abc import ABC, abstractmethod
from typing import List

from data_types import Card


class DeckBuilder(ABC):
    """Abstract baseclass to construct TableTop deck assets"""

    current_card_id = 100
    current_card_asset_id = 1

    card_back_url = 'https://www.frogtown.me/images/gatherer/CardBack.jpg'

    def __init__(self, cards: List[Card], hidden=True):
        """Initializes deck builder with list of cards.

        Args:
            cards:      Cards to include in deck of cards
            hidden:     Determines if deck of cards is facing back up
                        Defaults to true
        """
        self.cards = cards
        self.hidden = hidden

    @abstractmethod
    def create_deck(self) -> dict:
        """Abstractmethod to be implemented by child class.
        Create the json structure for the deck of cards.

        Returns:
            TableTop card deck json structure
        """
        raise NotImplemented
