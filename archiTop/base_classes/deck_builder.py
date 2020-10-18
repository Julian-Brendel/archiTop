"""Sourcefile containing base_class for TableTop deck construction"""
from abc import ABC, abstractmethod
from typing import List

from archiTop.config import load_config
from archiTop.scryfall.data_types import ScryfallCard

config = load_config()


class DeckBuilder(ABC):
    """Abstract baseclass to construct TableTop deck assets"""

    current_card_id = 100
    current_card_asset_id = 1

    def __init__(self,
                 cards: List[ScryfallCard],
                 hidden=True,
                 custom_back_url: str = None):
        """Initializes deck builder with list of cards.

        Args:
            cards:      Cards to include in deck of cards
            hidden:     Determines if deck of cards is facing back up
                        Defaults to true
        """
        self.cards = list(cards)
        self.hidden = hidden

        self.card_back_url = custom_back_url or config['DECK']['DEFAULT_CARDBACK_URL']

    @abstractmethod
    def create_deck(self) -> dict:
        """Abstractmethod to be implemented by child class.
        Create the json structure for the deck of cards.

        Returns:
            TableTop card deck json structure
        """
        raise NotImplemented
